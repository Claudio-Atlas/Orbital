import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // These reference CSS variables set by ThemeProvider
        accent: {
          DEFAULT: "var(--accent)",
          light: "var(--accent-light)",
        },
        themed: {
          bg: "var(--background)",
          "bg-elevated": "var(--background-elevated)",
          fg: "var(--foreground)",
          card: "var(--card)",
          "card-border": "var(--card-border)",
          primary: "var(--text-primary)",
          secondary: "var(--text-secondary)",
          muted: "var(--text-muted)",
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
        glow: "0 0 20px rgba(var(--accent-rgb), 0.3)",
        "glow-sm": "0 0 10px rgba(var(--accent-rgb), 0.2)",
        "glow-lg": "0 0 40px rgba(var(--accent-rgb), 0.4), 0 0 80px rgba(var(--accent-rgb), 0.2)",
      },
      animation: {
        "glow-pulse": "glow-pulse 2s ease-in-out infinite",
        "breathing": "breathing 3s ease-in-out infinite",
      },
      keyframes: {
        "glow-pulse": {
          "0%, 100%": { boxShadow: "0 0 20px rgba(var(--accent-rgb), 0.3)" },
          "50%": { boxShadow: "0 0 30px rgba(var(--accent-rgb), 0.5)" },
        },
        "breathing": {
          "0%, 100%": { opacity: "0.6", transform: "scale(1)" },
          "50%": { opacity: "1", transform: "scale(1.02)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
