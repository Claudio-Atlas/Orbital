import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Orbital Core Colors
        orbital: {
          black: "#000000",
          "near-black": "#05060A",
          white: "#FFFFFF",
        },
        // Text colors
        gray: {
          1: "#B6BCC6",
          2: "#8E97A6",
        },
        // Accent colors (use sparingly)
        accent: {
          violet: "#8B5CF6",
          "violet-hover": "#A78BFA",
          cyan: "#22D3EE",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        display: ["var(--font-space-grotesk)", "system-ui", "sans-serif"],
      },
      borderRadius: {
        orbital: "16px",
      },
      boxShadow: {
        glow: "0 0 20px rgba(139, 92, 246, 0.3)",
        "glow-sm": "0 0 10px rgba(139, 92, 246, 0.2)",
      },
      animation: {
        "glow-pulse": "glow-pulse 2s ease-in-out infinite",
      },
      keyframes: {
        "glow-pulse": {
          "0%, 100%": { boxShadow: "0 0 20px rgba(139, 92, 246, 0.3)" },
          "50%": { boxShadow: "0 0 30px rgba(139, 92, 246, 0.5)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
