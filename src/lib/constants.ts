// ORBITAL LEARNING — GLOBAL CONSTANTS

export const SITE = {
  name: "Orbital",
  orgName: "Orbital Learning",
  domain: "orbitallearning.org",
  url: "https://orbitallearning.org",
  
  title: "Orbital — Precision Prep for STEM",
  description: "Course-specific STEM exam prep with step-by-step walkthroughs, free videos, and $2 study guides.",
  
  tagline: "Precision prep for STEM.",
  taglineSecondary: "Course-specific walkthroughs. Free videos. $2 guides.",
  
  footer: "© Orbital Learning. All rights reserved.",
  supportEmail: "support@orbitallearning.org",
};

export const PRODUCT_FAMILIES = {
  // Free tier
  core: {
    name: "Orbital Core Module",
    price: 0,
    description: "Free foundational content",
  },
  // Micro products ($2)
  mini: {
    name: "Orbital Mini",
    price: 2,
    description: "Focused exam prep guide",
  },
  review: {
    name: "Orbital Review",
    price: 2,
    description: "Topic review with practice",
  },
  drill: {
    name: "Orbital Drill",
    price: 2,
    description: "Intensive problem practice",
  },
  // Bundles ($9)
  examPack: {
    name: "Orbital Exam Pack",
    price: 9,
    description: "Complete exam preparation",
  },
  finalSprint: {
    name: "Orbital Final Sprint",
    price: 9,
    description: "Final exam intensive review",
  },
  // Subscription
  vault: {
    name: "Orbital Vault",
    price: 19, // per month
    description: "Unlimited access library",
  },
} as const;

export const UNIVERSITIES = {
  asu: {
    id: "asu",
    name: "Arizona State University",
    shortName: "ASU",
  },
  gcu: {
    id: "gcu",
    name: "Grand Canyon University",
    shortName: "GCU",
  },
} as const;

export const NAV_LINKS = [
  { href: "/courses", label: "Courses" },
  { href: "/videos", label: "Videos" },
  { href: "/store", label: "Store" },
  { href: "/about", label: "About" },
] as const;

export const SOCIAL_LINKS = {
  twitter: "https://twitter.com/orbitallearning",
  youtube: "https://youtube.com/@orbitallearning",
  discord: "https://discord.gg/orbital",
} as const;
