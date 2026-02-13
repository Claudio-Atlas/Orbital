import { createClient } from '@supabase/supabase-js';

/**
 * Creates a Supabase admin client with the service role key.
 * Use this for server-side operations that need elevated permissions
 * (like webhooks, background jobs, etc.)
 * 
 * NEVER expose this client to the browser!
 */
export function createAdminClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const serviceKey = process.env.SUPABASE_SERVICE_KEY;

  if (!url || !serviceKey) {
    throw new Error('Supabase admin client requires NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_KEY');
  }

  return createClient(url, serviceKey, {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  });
}
