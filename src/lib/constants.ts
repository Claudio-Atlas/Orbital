// ORBITAL SOLVER — GLOBAL CONSTANTS

export const SITE = {
  name: "Orbital",
  orgName: "Orbital",
  domain: "orbital-solver.io",
  url: "https://orbital-solver.io",
  
  title: "Orbital — Type a problem. Get a video.",
  description: "AI-powered math video tutorials. Type any problem and watch a step-by-step video walkthrough in seconds.",
  
  tagline: "Type a problem. Get a video.",
  taglineSecondary: "AI-powered math tutorials, generated in seconds.",
  
  footer: "© 2026 Orbital. All rights reserved.",
  supportEmail: "hello@orbital-solver.io",
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

// Pricing tiers
export const PRICING = {
  free: {
    name: "Free",
    price: 0,
    solves: "3/day",
    features: ["Video walkthroughs", "Voice narration", "All problem types"],
  },
  student: {
    name: "Student",
    price: 9,
    solves: "Unlimited",
    features: ["Everything in Free", "Unlimited problems", "Priority generation", "Download videos"],
  },
  pro: {
    name: "Pro",
    price: 19,
    solves: "Unlimited+",
    features: ["Everything in Student", "No watermark", "API access", "Bulk generation"],
  },
} as const;
