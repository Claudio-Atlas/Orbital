import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { createAdminClient } from '@/lib/supabase/admin';

// Lazy init Stripe
function getStripe() {
  if (!process.env.STRIPE_SECRET_KEY) {
    throw new Error('STRIPE_SECRET_KEY not configured');
  }
  return new Stripe(process.env.STRIPE_SECRET_KEY);
}

// Subscription tier minutes (must match create-checkout)
const SUBSCRIPTION_TIERS: Record<string, number> = {
  starter: 10,
  standard: 50,
  pro: 120,
};

export async function POST(request: NextRequest) {
  const payload = await request.text();
  const signature = request.headers.get('stripe-signature');

  // SECURITY: Webhook signature verification is REQUIRED
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!webhookSecret) {
    console.error('❌ STRIPE_WEBHOOK_SECRET not configured');
    return NextResponse.json(
      { error: 'Webhook secret not configured. Cannot process webhooks securely.' },
      { status: 500 }
    );
  }

  if (!signature) {
    return NextResponse.json(
      { error: 'Missing stripe-signature header' },
      { status: 400 }
    );
  }

  let event: Stripe.Event;
  const stripe = getStripe();

  try {
    event = stripe.webhooks.constructEvent(payload, signature, webhookSecret);
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    console.error(`❌ Webhook signature verification failed: ${message}`);
    return NextResponse.json(
      { error: `Webhook Error: ${message}` },
      { status: 400 }
    );
  }

  const supabase = createAdminClient();

  try {
    switch (event.type) {
      // Handle checkout completion (both one-time and first subscription payment)
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session;
        await handleCheckoutComplete(supabase, session);
        break;
      }

      // Handle subscription renewal (recurring payments)
      case 'invoice.paid': {
        const invoice = event.data.object as Stripe.Invoice;
        await handleInvoicePaid(supabase, invoice);
        break;
      }

      // Handle subscription cancellation
      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;
        await handleSubscriptionDeleted(supabase, subscription);
        break;
      }

      default:
        console.log(`ℹ️ Unhandled event type: ${event.type}`);
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    console.error('❌ Webhook handler error:', error);
    // Return 200 anyway to prevent Stripe from retrying
    // (we've logged the error for investigation)
    return NextResponse.json({ received: true, error: 'Handler failed' });
  }
}

/**
 * Handle checkout.session.completed
 * Credits minutes to user's balance for both one-time and first subscription payments
 */
async function handleCheckoutComplete(
  supabase: ReturnType<typeof createAdminClient>,
  session: Stripe.Checkout.Session
) {
  const userId = session.client_reference_id || session.metadata?.user_id;
  const tierName = session.metadata?.tier;
  const minutes = parseFloat(session.metadata?.minutes || '0');
  const mode = session.metadata?.mode || 'payment';
  const amountCents = session.amount_total || 0;

  if (!userId) {
    console.error('❌ Checkout session missing user_id');
    return;
  }

  if (minutes <= 0) {
    console.error('❌ Checkout session missing minutes');
    return;
  }

  // Add minutes using the RPC function
  const { error: rpcError } = await supabase.rpc('add_minutes', {
    p_user_id: userId,
    p_minutes: minutes,
    p_amount_cents: amountCents,
    p_tier: tierName,
    p_stripe_session_id: session.id,
  });

  if (rpcError) {
    console.error(`❌ Failed to add minutes: ${rpcError.message}`);
    throw rpcError;
  }

  console.log(`✅ Added ${minutes} minutes to user ${userId}`);

  // If subscription, store the subscription info on the profile
  if (mode === 'subscription' && session.subscription) {
    const { error: updateError } = await supabase
      .from('profiles')
      .update({
        stripe_customer_id: session.customer as string,
        stripe_subscription_id: session.subscription as string,
        subscription_tier: tierName,
      })
      .eq('id', userId);

    if (updateError) {
      console.error(`❌ Failed to update subscription info: ${updateError.message}`);
    } else {
      console.log(`✅ Updated subscription info for user ${userId}`);
    }
  }
}

/**
 * Handle invoice.paid
 * Credits minutes for subscription renewals (not the initial payment)
 */
async function handleInvoicePaid(
  supabase: ReturnType<typeof createAdminClient>,
  invoice: Stripe.Invoice
) {
  // Skip if this is the first invoice (already handled by checkout.session.completed)
  if (invoice.billing_reason === 'subscription_create') {
    console.log('ℹ️ Skipping initial subscription invoice (handled by checkout)');
    return;
  }

  // In Stripe v20+, subscription is accessed via parent.subscription_details
  const subscriptionDetails = invoice.parent?.subscription_details;
  const subscriptionId = typeof subscriptionDetails?.subscription === 'string' 
    ? subscriptionDetails.subscription 
    : subscriptionDetails?.subscription?.id;
    
  if (!subscriptionId) {
    console.log('ℹ️ Invoice has no subscription, skipping');
    return;
  }

  // Find user by subscription ID
  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select('id, subscription_tier')
    .eq('stripe_subscription_id', subscriptionId)
    .single();

  if (profileError || !profile) {
    console.error(`❌ Could not find user for subscription ${subscriptionId}`);
    return;
  }

  const userId = profile.id;
  const tierName = profile.subscription_tier || 'starter';
  const minutes = SUBSCRIPTION_TIERS[tierName] || SUBSCRIPTION_TIERS.starter;
  const amountCents = invoice.amount_paid || 0;

  // Add monthly minutes
  const { error: rpcError } = await supabase.rpc('add_minutes', {
    p_user_id: userId,
    p_minutes: minutes,
    p_amount_cents: amountCents,
    p_tier: tierName,
    p_stripe_session_id: invoice.id,
  });

  if (rpcError) {
    console.error(`❌ Failed to add renewal minutes: ${rpcError.message}`);
    throw rpcError;
  }

  console.log(`✅ Monthly renewal: Added ${minutes} minutes to user ${userId}`);
}

/**
 * Handle customer.subscription.deleted
 * Clears subscription info from the user's profile
 */
async function handleSubscriptionDeleted(
  supabase: ReturnType<typeof createAdminClient>,
  subscription: Stripe.Subscription
) {
  const subscriptionId = subscription.id;

  const { error } = await supabase
    .from('profiles')
    .update({
      stripe_subscription_id: null,
      subscription_tier: null,
    })
    .eq('stripe_subscription_id', subscriptionId);

  if (error) {
    console.error(`❌ Failed to clear subscription info: ${error.message}`);
    throw error;
  }

  console.log(`✅ Subscription ${subscriptionId} cancelled and cleared from profile`);
}
