// ORBITAL SOLVER — GLOBAL CONSTANTS

export const SITE = {
  name: "Orbital",
  orgName: "Orbital",
  domain: "orbitalsolver.io",
  url: "https://orbitalsolver.io",
  
  title: "Orbital — Type a problem. Get a video.",
  description: "AI-powered math video tutorials. Type any problem and watch a step-by-step video walkthrough in seconds.",
  
  tagline: "Type a problem. Get a video.",
  taglineSecondary: "AI-powered math tutorials, generated in seconds.",
  
  footer: "© 2026 Orbital. All rights reserved.",
  supportEmail: "hello@orbitalsolver.io",
};

// Simplified nav for focused product
export const NAV_LINKS = [
  { href: "/", label: "Solve" },
  { href: "#pricing", label: "Pricing" },
  { href: "#how-it-works", label: "How It Works" },
] as const;

export const SOCIAL_LINKS = {
  twitter: "https://twitter.com/orbitalsolver",
  tiktok: "https://tiktok.com/@orbitalsolver",
  discord: "https://discord.gg/orbital",
} as const;

// Pricing tiers — Minutes-based token system
// Cost breakdown: ~$0.016/min (OpenAI TTS + DeepSeek)
// UX: User enters problem → see preview → "This will use X minutes" → accept/deny
export const PRICING = {
  starter: {
    name: "Starter",
    price: 2,
    minutes: 10,
    pricePerMin: "$0.20",
    features: ["10 minutes of video", "All problem types", "HD quality", "Download videos"],
  },
  standard: {
    name: "Standard",
    price: 8,
    minutes: 50,
    pricePerMin: "$0.16",
    badge: "Best Value",
    features: ["50 minutes of video", "All problem types", "HD quality", "Download videos", "Priority generation"],
  },
  pro: {
    name: "Pro",
    price: 15,
    minutes: 120,
    pricePerMin: "$0.125",
    badge: "20 min FREE",
    features: ["120 minutes of video", "All problem types", "HD quality", "Download videos", "Priority generation", "No watermark"],
  },
} as const;
