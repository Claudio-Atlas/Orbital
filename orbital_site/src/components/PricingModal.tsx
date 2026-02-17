"use client";

import { useState, useEffect } from "react";
import { getSupabase } from "@/lib/supabase";
import { useTheme } from "@/lib/theme-context";

interface PricingModalProps {
  isOpen: boolean;
  onClose: () => void;
  isDark?: boolean; // Optional now, we'll use context
}

type Tier = {
  name: string;
  minutes: number;
  oneTime: { price: number; priceId: string };
  subscription: { price: number; priceId: string };
  badge?: string;
};

const TIERS: Record<string, Tier> = {
  starter: {
    name: "Starter",
    minutes: 10,
    oneTime: { price: 2, priceId: "price_1SzmKKBDEgxKWlDL2k0V7nYG" },
    subscription: { price: 1.5, priceId: "price_1SzmKmBDEgxKWlDLlvmHBMPb" },
  },
  standard: {
    name: "Standard",
    minutes: 50,
    oneTime: { price: 8, priceId: "price_1SzmMWBDEgxKWlDLwy7yInQv" },
    subscription: { price: 6, priceId: "price_1SzmNOBDEgxKWlDLgRje5FeR" },
    badge: "Best Value",
  },
  pro: {
    name: "Pro",
    minutes: 120,
    oneTime: { price: 15, priceId: "price_1SzmQpBDEgxKWlDLJnvwG9e1" },
    subscription: { price: 12, priceId: "price_1SzmRWBDEgxKWlDLiUwiNxPQ" },
    badge: "20 min FREE",
  },
};

export function PricingModal({ isOpen, onClose, isDark: isDarkProp }: PricingModalProps) {
  const theme = useTheme();
  const isDark = isDarkProp ?? theme.isDark;
  const accent = theme.accent;
  
  const [billingMode, setBillingMode] = useState<"one_time" | "subscription">("one_time");
  const [loading, setLoading] = useState<string | null>(null);
  const [needsRefresh, setNeedsRefresh] = useState(false);
  const supabase = getSupabase();

  // Detect Safari back-button (bfcache restore) and show refresh message
  useEffect(() => {
    const handlePageShow = (e: PageTransitionEvent) => {
      if (e.persisted) {
        setNeedsRefresh(true);
        setLoading(null);
      }
    };
    window.addEventListener("pageshow", handlePageShow);
    return () => window.removeEventListener("pageshow", handlePageShow);
  }, []);

  if (!isOpen) return null;

  const handleCheckout = async (tier: string) => {
    if (needsRefresh) {
      window.location.reload();
      return;
    }
    
    setLoading(tier);

    try {
      console.log("[Checkout] Getting session...");
      const { data: { session }, error: sessionError } = await supabase.auth.getSession();
      console.log("[Checkout] Session result:", { hasSession: !!session, error: sessionError?.message });
      
      if (!session) {
        alert("Please log in to purchase");
        setLoading(null);
        return;
      }

      console.log("[Checkout] Calling API...");
      const response = await fetch(`/api/payments/create-checkout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${session.access_token}`,
        },
        body: JSON.stringify({
          tier,
          mode: billingMode === "subscription" ? "subscription" : "payment",
          success_url: `${window.location.origin}/dashboard?success=true`,
          cancel_url: `${window.location.origin}/dashboard?canceled=true`,
        }),
      });
      
      console.log("[Checkout] Response status:", response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.log("[Checkout] Error response:", errorText);
        alert(`Checkout failed: ${response.status} - ${errorText}`);
        setLoading(null);
        return;
      }

      const data = await response.json();
      console.log("[Checkout] Success data:", data);

      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        alert(data.detail || "Failed to create checkout - no URL returned");
        setLoading(null);
      }
    } catch (error) {
      console.error("Checkout error:", error);
      alert(`Failed to start checkout: ${error}`);
      setLoading(null);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className={`relative w-full max-w-3xl rounded-3xl p-8 ${
        isDark 
          ? "bg-zinc-900 border border-white/10" 
          : "bg-white border border-gray-200"
      }`}>
        {/* Close button */}
        <button
          onClick={onClose}
          className={`absolute top-4 right-4 p-2 rounded-full transition-colors ${
            isDark ? "hover:bg-white/10 text-gray-400" : "hover:bg-gray-100 text-gray-500"
          }`}
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Header */}
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold mb-2">Buy Minutes</h2>
          <p className="text-themed-secondary">
            Choose a pack to start creating videos
          </p>
        </div>

        {/* Refresh notice (shows after browser back button) */}
        {needsRefresh && (
          <div 
            onClick={() => window.location.reload()}
            className={`mb-6 p-3 rounded-xl text-center cursor-pointer transition-colors ${
              isDark 
                ? "bg-amber-500/10 border border-amber-500/20 text-amber-400 hover:bg-amber-500/20" 
                : "bg-amber-50 border border-amber-200 text-amber-700 hover:bg-amber-100"
            }`}
          >
            Page needs refresh — <span className="underline">click here</span> or select a package to continue
          </div>
        )}

        {/* Billing Toggle */}
        <div className="flex justify-center mb-8">
          <div className={`inline-flex p-1 rounded-xl ${
            isDark ? "bg-white/5" : "bg-gray-100"
          }`}>
            <button
              onClick={() => setBillingMode("one_time")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                billingMode === "one_time"
                  ? isDark
                    ? "bg-white text-black"
                    : "bg-white text-gray-900 shadow"
                  : isDark
                  ? "text-gray-400 hover:text-white"
                  : "text-gray-500 hover:text-gray-900"
              }`}
            >
              One-time
            </button>
            <button
              onClick={() => setBillingMode("subscription")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                billingMode === "subscription"
                  ? isDark
                    ? "bg-white text-black"
                    : "bg-white text-gray-900 shadow"
                  : isDark
                  ? "text-gray-400 hover:text-white"
                  : "text-gray-500 hover:text-gray-900"
              }`}
            >
              Monthly
              <span className={`ml-1.5 text-xs px-1.5 py-0.5 rounded ${
                isDark ? "bg-green-500/20 text-green-400" : "bg-green-100 text-green-600"
              }`}>
                Save 20%+
              </span>
            </button>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-3 gap-4">
          {Object.entries(TIERS).map(([key, tier]) => {
            const price = billingMode === "subscription" ? tier.subscription.price : tier.oneTime.price;
            const isPopular = key === "standard";

            return (
              <div
                key={key}
                className={`relative rounded-2xl p-5 transition-all ${
                  isPopular
                    ? "border-2"
                    : isDark
                    ? "bg-white/5 border border-white/10 hover:border-white/20"
                    : "bg-gray-50 border border-gray-200 hover:border-gray-300"
                }`}
                style={isPopular ? {
                  borderColor: accent.main,
                  background: `rgba(${accent.rgb}, 0.1)`
                } : undefined}
              >
                {/* Badge */}
                {tier.badge && (
                  <div 
                    className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full text-xs font-semibold text-white"
                    style={{ background: accent.main }}
                  >
                    {tier.badge}
                  </div>
                )}

                <div className="text-center">
                  <h3 className="font-semibold text-lg mb-1">{tier.name}</h3>
                  <p className="text-sm mb-4 text-themed-secondary">
                    {tier.minutes} minutes
                  </p>

                  <div className="mb-4">
                    <span className="text-3xl font-bold">${price.toFixed(2)}</span>
                    {billingMode === "subscription" && (
                      <span className="text-sm text-themed-secondary">/mo</span>
                    )}
                  </div>

                  <p className="text-xs mb-4 text-themed-muted">
                    ${(price / tier.minutes).toFixed(2)}/min
                  </p>

                  <button
                    onClick={() => handleCheckout(key)}
                    disabled={loading !== null}
                    className={`w-full py-2.5 rounded-xl font-medium transition-all disabled:opacity-50 ${
                      isPopular
                        ? "text-white btn-glow"
                        : isDark
                        ? "bg-white text-black hover:bg-gray-100"
                        : "bg-gray-900 text-white hover:bg-gray-800"
                    }`}
                    style={isPopular ? { 
                      background: accent.main,
                      boxShadow: `0 4px 20px rgba(${accent.rgb}, 0.35)`
                    } : undefined}
                  >
                    {loading === key ? (
                      <span className="flex items-center justify-center gap-2">
                        <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                        </svg>
                        Loading...
                      </span>
                    ) : (
                      "Buy Now"
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer note */}
        <p className="text-center text-xs mt-6 text-themed-muted">
          {billingMode === "subscription" 
            ? "Cancel anytime. Minutes refresh monthly."
            : "One-time purchase. Minutes never expire."}
        </p>
      </div>
    </div>
  );
}
