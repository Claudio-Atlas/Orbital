'use client';

import { useEffect, useState, useCallback } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { createClient } from '@/lib/supabase';

const pricingTiers = [
  {
    id: 'starter',
    name: 'Starter',
    minutes: 10,
    price: 2,
    priceId: process.env.NEXT_PUBLIC_STRIPE_PRICE_STARTER || 'price_starter',
  },
  {
    id: 'standard',
    name: 'Standard',
    minutes: 50,
    price: 8,
    priceId: process.env.NEXT_PUBLIC_STRIPE_PRICE_STANDARD || 'price_standard',
    popular: true,
  },
  {
    id: 'pro',
    name: 'Pro',
    minutes: 120,
    price: 15,
    priceId: process.env.NEXT_PUBLIC_STRIPE_PRICE_PRO || 'price_pro',
  },
];

export default function AccountPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [minutesBalance, setMinutesBalance] = useState(0);
  const [selectedTier, setSelectedTier] = useState('standard');
  const [isCheckingOut, setIsCheckingOut] = useState(false);

  // Fetch user's minute balance from Supabase
  const fetchBalance = useCallback(async (userId: string) => {
    const supabase = createClient();
    const { data } = await supabase
      .from('profiles')
      .select('minutes_balance')
      .eq('id', userId)
      .single();

    if (data) {
      setMinutesBalance(data.minutes_balance || 0);
    }
  }, []);

  // Authenticate user via token (from iOS app) or existing session
  const authenticateUser = useCallback(async (token: string | null) => {
    const supabase = createClient();

    if (token) {
      // Token-based auth from iOS app
      const { data, error } = await supabase.auth.setSession({
        access_token: token,
        refresh_token: '', // We only have access token from iOS
      });

      if (error) {
        console.error('Token auth failed:', error);
        // Try getting existing session
        const { data: sessionData } = await supabase.auth.getSession();
        if (sessionData.session) {
          setIsAuthenticated(true);
          setUserEmail(sessionData.session.user.email || '');
          await fetchBalance(sessionData.session.user.id);
        } else {
          router.push('/login');
          return;
        }
      } else if (data.session) {
        setIsAuthenticated(true);
        setUserEmail(data.session.user.email || '');
        await fetchBalance(data.session.user.id);
      }
    } else {
      // Check existing session
      const { data: sessionData } = await supabase.auth.getSession();
      if (sessionData.session) {
        setIsAuthenticated(true);
        setUserEmail(sessionData.session.user.email || '');
        await fetchBalance(sessionData.session.user.id);
      } else {
        router.push('/login');
        return;
      }
    }

    setIsLoading(false);
  }, [router, fetchBalance]);

  // Run authentication on mount
  useEffect(() => {
    const token = searchParams.get('token');
    authenticateUser(token);
  }, [searchParams, authenticateUser]);

  async function handleCheckout() {
    setIsCheckingOut(true);
    const tier = pricingTiers.find((t) => t.id === selectedTier);
    if (!tier) return;

    try {
      const response = await fetch('/api/payments/create-checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          priceId: tier.priceId,
          minutes: tier.minutes,
          mode: 'payment',
        }),
      });

      const data = await response.json();

      if (data.url) {
        window.location.href = data.url;
      } else {
        console.error('No checkout URL returned');
        setIsCheckingOut(false);
      }
    } catch (error) {
      console.error('Checkout error:', error);
      setIsCheckingOut(false);
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0a0a14] to-black text-white">
      <div className="max-w-lg mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2">Manage Minutes</h1>
          <p className="text-gray-400">{userEmail}</p>
        </div>

        {/* Current Balance */}
        <div className="bg-white/5 border border-white/10 rounded-2xl p-6 mb-8">
          <p className="text-gray-400 text-sm mb-1">Current Balance</p>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-bold">{minutesBalance.toFixed(1)}</span>
            <span className="text-gray-400">minutes</span>
          </div>
        </div>

        {/* Pricing Tiers */}
        <div className="space-y-3 mb-8">
          <p className="text-sm text-gray-400 mb-4">Select a package:</p>
          
          {pricingTiers.map((tier) => (
            <button
              key={tier.id}
              onClick={() => setSelectedTier(tier.id)}
              className={`w-full p-4 rounded-xl border transition-all ${
                selectedTier === tier.id
                  ? 'border-purple-500 bg-purple-500/10'
                  : 'border-white/10 bg-white/5 hover:border-white/20'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                      selectedTier === tier.id
                        ? 'border-purple-500'
                        : 'border-gray-500'
                    }`}
                  >
                    {selectedTier === tier.id && (
                      <div className="w-2.5 h-2.5 rounded-full bg-purple-500" />
                    )}
                  </div>
                  <div className="text-left">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold">{tier.name}</span>
                      {tier.popular && (
                        <span className="text-xs bg-purple-500 px-2 py-0.5 rounded-full">
                          Best Value
                        </span>
                      )}
                    </div>
                    <span className="text-sm text-gray-400">
                      {tier.minutes} minutes
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xl font-bold">${tier.price}</span>
                  <p className="text-xs text-gray-500">
                    ${(tier.price / tier.minutes).toFixed(2)}/min
                  </p>
                </div>
              </div>
            </button>
          ))}
        </div>

        {/* Checkout Button */}
        <button
          onClick={handleCheckout}
          disabled={isCheckingOut}
          className="w-full py-4 bg-gradient-to-r from-purple-400 to-purple-600 rounded-xl font-semibold text-lg shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50 transition-all disabled:opacity-50"
        >
          {isCheckingOut ? (
            <span className="flex items-center justify-center gap-2">
              <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
              Processing...
            </span>
          ) : (
            `Continue to Checkout`
          )}
        </button>

        <p className="text-center text-xs text-gray-500 mt-4">
          Secure payment powered by Stripe
        </p>

        {/* Back to App hint */}
        <p className="text-center text-sm text-gray-400 mt-8">
          After purchase, your minutes will be available in the app instantly.
        </p>
      </div>
    </div>
  );
}
