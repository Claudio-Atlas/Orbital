"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { getSupabase } from "@/lib/supabase";
import { OrbitalLogo } from "@/components/OrbitalLogo";

type Theme = "dark" | "light";

interface Purchase {
  id: string;
  minutes: number;
  amount_cents: number;
  tier: string;
  created_at: string;
  stripe_payment_id: string | null;
}

const Icons = {
  arrowLeft: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
    </svg>
  ),
  receipt: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 14.25l6-6m4.5-3.493V21.75l-3.75-1.5-3.75 1.5-3.75-1.5-3.75 1.5V4.757c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0c1.1.128 1.907 1.077 1.907 2.185zM9.75 9h.008v.008H9.75V9zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm4.125 4.5h.008v.008h-.008V13.5zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
    </svg>
  ),
  clock: (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
};

const TIER_LABELS: Record<string, string> = {
  starter: "Starter Pack",
  standard: "Standard Pack",
  pro: "Pro Pack",
  bonus: "Bonus Minutes",
};

export default function ClientComponent() {
  const [theme, setTheme] = useState<Theme>("dark");
  const [purchases, setPurchases] = useState<Purchase[]>([]);
  const [loading, setLoading] = useState(true);

  const router = useRouter();
  const { user, profile, loading: authLoading } = useAuth();
  const supabase = getSupabase();

  // Redirect if not logged in
  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    const stored = localStorage.getItem("orbital-theme") as Theme | null;
    if (stored) setTheme(stored);
  }, []);

  // Fetch purchases
  useEffect(() => {
    async function fetchPurchases() {
      if (!user) return;

      try {
        const { data, error } = await supabase
          .from("purchases")
          .select("*")
          .eq("user_id", user.id)
          .order("created_at", { ascending: false });

        if (data) {
          setPurchases(data);
        }
      } catch (err) {
        console.error("Error fetching purchases:", err);
      } finally {
        setLoading(false);
      }
    }

    if (user) {
      fetchPurchases();
    }
  }, [user]);

  const isDark = theme === "dark";

  // Show loading while checking auth
  if (authLoading) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-black">
        <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  // If not logged in, show loading spinner
  // Navigation is handled by: middleware (server-side) or signOut handler (client-side)
  if (!user) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-black">
        <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
    });
  };

  const formatCurrency = (cents: number) => {
    return `$${(cents / 100).toFixed(2)}`;
  };

  // Calculate totals
  const totalSpent = purchases.reduce((acc, p) => acc + p.amount_cents, 0);
  const totalMinutes = purchases.reduce((acc, p) => acc + p.minutes, 0);

  return (
    <div className={`min-h-screen w-full transition-colors duration-300 ${
      isDark ? "bg-black text-white" : "bg-gray-50 text-gray-900"
    }`}>
      {/* Header */}
      <header className={`sticky top-0 z-50 border-b backdrop-blur-xl ${
        isDark ? "bg-black/80 border-white/10" : "bg-white/80 border-gray-200"
      }`}>
        <div className="max-w-3xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link 
              href="/dashboard" 
              className={`p-2 rounded-lg transition-colors ${
                isDark ? "hover:bg-white/10" : "hover:bg-gray-100"
              }`}
            >
              {Icons.arrowLeft}
            </Link>
            <h1 className="text-lg font-semibold">Purchase History</h1>
          </div>

          <Link href="/" className="flex items-center gap-2">
            <OrbitalLogo className="w-8 h-8" />
          </Link>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-3xl mx-auto px-6 py-8">
        
        {/* Summary Cards */}
        <div className="grid grid-cols-2 gap-4 mb-8">
          <div className={`rounded-2xl p-5 ${
            isDark ? "bg-white/5 border border-white/10" : "bg-white border border-gray-200"
          }`}>
            <p className={`text-sm ${isDark ? "text-gray-400" : "text-gray-500"}`}>Total Spent</p>
            <p className="text-2xl font-bold mt-1">{formatCurrency(totalSpent)}</p>
          </div>
          <div className={`rounded-2xl p-5 ${
            isDark ? "bg-white/5 border border-white/10" : "bg-white border border-gray-200"
          }`}>
            <p className={`text-sm ${isDark ? "text-gray-400" : "text-gray-500"}`}>Minutes Purchased</p>
            <p className="text-2xl font-bold mt-1 text-violet-500">{totalMinutes}</p>
          </div>
        </div>

        {/* Purchases List */}
        <div className={`rounded-2xl overflow-hidden ${
          isDark ? "bg-white/5 border border-white/10" : "bg-white border border-gray-200"
        }`}>
          <div className={`px-6 py-4 border-b ${
            isDark ? "border-white/10" : "border-gray-100"
          }`}>
            <div className="flex items-center gap-2">
              {Icons.receipt}
              <h2 className="font-semibold">Transactions</h2>
            </div>
          </div>

          {loading ? (
            <div className="p-12 text-center">
              <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin mx-auto" />
            </div>
          ) : purchases.length === 0 ? (
            <div className="p-12 text-center">
              <div className={`w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center ${
                isDark ? "bg-white/5" : "bg-gray-100"
              }`}>
                {Icons.receipt}
              </div>
              <p className={`font-medium mb-2`}>No purchases yet</p>
              <p className={`text-sm mb-6 ${isDark ? "text-gray-500" : "text-gray-400"}`}>
                Buy minutes to start creating videos
              </p>
              <Link
                href="/dashboard"
                className="inline-block px-6 py-3 rounded-xl font-medium bg-violet-600 text-white hover:bg-violet-500 transition-colors"
              >
                Go to Dashboard
              </Link>
            </div>
          ) : (
            <div className="divide-y divide-white/10">
              {purchases.map((purchase) => (
                <div 
                  key={purchase.id} 
                  className={`px-6 py-4 flex items-center justify-between ${
                    isDark ? "hover:bg-white/[0.02]" : "hover:bg-gray-50"
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                      isDark ? "bg-violet-500/20" : "bg-violet-100"
                    }`}>
                      <span className="text-violet-500 font-bold text-sm">+{purchase.minutes}</span>
                    </div>
                    <div>
                      <p className="font-medium">
                        {TIER_LABELS[purchase.tier] || purchase.tier}
                      </p>
                      <p className={`text-sm flex items-center gap-1 ${
                        isDark ? "text-gray-500" : "text-gray-400"
                      }`}>
                        {Icons.clock}
                        {formatDate(purchase.created_at)}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold">{formatCurrency(purchase.amount_cents)}</p>
                    <p className={`text-sm ${isDark ? "text-gray-500" : "text-gray-400"}`}>
                      {purchase.minutes} min
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Current Balance */}
        <div className={`mt-6 rounded-2xl p-5 text-center ${
          isDark ? "bg-violet-500/10 border border-violet-500/20" : "bg-violet-50 border border-violet-100"
        }`}>
          <p className={`text-sm ${isDark ? "text-gray-400" : "text-gray-600"}`}>Current Balance</p>
          <p className="text-3xl font-bold text-violet-500 mt-1">{profile?.minutes_balance ?? 0} minutes</p>
        </div>

      </main>
    </div>
  );
}
