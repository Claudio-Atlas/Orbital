"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";

// Match iOS AccentPreset exactly
export type AccentPreset = 
  | "nebulaPurple"
  | "oceanBlue"
  | "cardinalRed"
  | "forestGreen"
  | "sunsetOrange"
  | "electricPink"
  | "cyberCyan";

export type Theme = "dark" | "light";

interface AccentColors {
  main: string;
  light: string;
  rgb: string; // For rgba() usage
  rgbLight: string;
}

// Color definitions matching iOS AccentTheme.swift
export const ACCENT_PRESETS: Record<AccentPreset, { name: string; colors: AccentColors }> = {
  nebulaPurple: {
    name: "Nebula Purple",
    colors: {
      main: "#8B5CF6",
      light: "#A78BFA",
      rgb: "139, 92, 246",
      rgbLight: "167, 139, 250",
    },
  },
  oceanBlue: {
    name: "Ocean Blue",
    colors: {
      main: "#3B82F6",
      light: "#60A5FA",
      rgb: "59, 130, 246",
      rgbLight: "96, 165, 250",
    },
  },
  cardinalRed: {
    name: "Cardinal Red",
    colors: {
      main: "#EF4444",
      light: "#FC8181",
      rgb: "239, 68, 68",
      rgbLight: "252, 129, 129",
    },
  },
  forestGreen: {
    name: "Forest Green",
    colors: {
      main: "#22C55E",
      light: "#4ADE80",
      rgb: "34, 197, 94",
      rgbLight: "74, 222, 128",
    },
  },
  sunsetOrange: {
    name: "Sunset Orange",
    colors: {
      main: "#F97316",
      light: "#FDBA74",
      rgb: "249, 115, 22",
      rgbLight: "253, 186, 116",
    },
  },
  electricPink: {
    name: "Electric Pink",
    colors: {
      main: "#EC4899",
      light: "#F472B6",
      rgb: "236, 72, 153",
      rgbLight: "244, 114, 182",
    },
  },
  cyberCyan: {
    name: "Cyber Cyan",
    colors: {
      main: "#06B6D4",
      light: "#67E8F9",
      rgb: "6, 182, 212",
      rgbLight: "103, 232, 249",
    },
  },
};

interface ThemeContextValue {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
  accentPreset: AccentPreset;
  setAccentPreset: (preset: AccentPreset) => void;
  accent: AccentColors;
  isDark: boolean;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

function applyThemeToDOM(theme: Theme, accentPreset: AccentPreset) {
  const root = document.documentElement;
  const colors = ACCENT_PRESETS[accentPreset].colors;

  // Theme class
  root.classList.remove("light", "dark");
  root.classList.add(theme);

  // CSS custom properties for accent
  root.style.setProperty("--accent", colors.main);
  root.style.setProperty("--accent-light", colors.light);
  root.style.setProperty("--accent-rgb", colors.rgb);
  root.style.setProperty("--accent-rgb-light", colors.rgbLight);

  // Theme-specific colors
  if (theme === "dark") {
    root.style.setProperty("--background", "#000000");
    root.style.setProperty("--background-elevated", "#0a0a0a");
    root.style.setProperty("--foreground", "#ffffff");
    root.style.setProperty("--card", "rgba(255, 255, 255, 0.05)");
    root.style.setProperty("--card-border", "rgba(255, 255, 255, 0.1)");
    root.style.setProperty("--card-border-hover", "rgba(255, 255, 255, 0.15)");
    root.style.setProperty("--text-primary", "#ffffff");
    root.style.setProperty("--text-secondary", "rgba(255, 255, 255, 0.55)");
    root.style.setProperty("--text-muted", "rgba(255, 255, 255, 0.35)");
  } else {
    root.style.setProperty("--background", "#f9fafb");
    root.style.setProperty("--background-elevated", "#ffffff");
    root.style.setProperty("--foreground", "#111827");
    root.style.setProperty("--card", "#ffffff");
    root.style.setProperty("--card-border", "rgba(0, 0, 0, 0.1)");
    root.style.setProperty("--card-border-hover", "rgba(0, 0, 0, 0.15)");
    root.style.setProperty("--text-primary", "#111827");
    root.style.setProperty("--text-secondary", "rgba(0, 0, 0, 0.55)");
    root.style.setProperty("--text-muted", "rgba(0, 0, 0, 0.35)");
  }
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<Theme>("dark");
  const [accentPreset, setAccentPresetState] = useState<AccentPreset>("nebulaPurple");
  const [mounted, setMounted] = useState(false);

  // Initialize from localStorage
  useEffect(() => {
    const storedTheme = localStorage.getItem("orbital-theme") as Theme | null;
    const storedAccent = localStorage.getItem("orbital-accent") as AccentPreset | null;

    if (storedTheme && (storedTheme === "dark" || storedTheme === "light")) {
      setThemeState(storedTheme);
    }
    if (storedAccent && storedAccent in ACCENT_PRESETS) {
      setAccentPresetState(storedAccent);
    }

    setMounted(true);
  }, []);

  // Apply theme to DOM whenever it changes
  useEffect(() => {
    if (mounted) {
      applyThemeToDOM(theme, accentPreset);
    }
  }, [theme, accentPreset, mounted]);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
    localStorage.setItem("orbital-theme", newTheme);
  };

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
  };

  const setAccentPreset = (preset: AccentPreset) => {
    setAccentPresetState(preset);
    localStorage.setItem("orbital-accent", preset);
  };

  const value: ThemeContextValue = {
    theme,
    setTheme,
    toggleTheme,
    accentPreset,
    setAccentPreset,
    accent: ACCENT_PRESETS[accentPreset].colors,
    isDark: theme === "dark",
  };

  // Prevent flash of wrong theme
  if (!mounted) {
    return null;
  }

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
}
