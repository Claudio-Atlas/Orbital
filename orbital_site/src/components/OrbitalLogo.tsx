"use client";

import { useTheme } from "@/lib/theme-context";

interface OrbitalLogoProps {
  className?: string;
  accentColor?: string; // Optional override
}

export function OrbitalLogo({ className = "h-8 w-8", accentColor }: OrbitalLogoProps) {
  // Try to get accent from context, fall back to default
  let accent = "#8B5CF6";
  try {
    const theme = useTheme();
    accent = theme.accent.main;
  } catch {
    // Not in ThemeProvider context, use default or override
  }
  
  const color = accentColor || accent;
  
  return (
    <svg
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Main O circle */}
      <circle
        cx="50"
        cy="50"
        r="30"
        stroke="currentColor"
        strokeWidth="4"
        fill="none"
      />
      
      {/* Orbital ring (ellipse tilted) */}
      <ellipse
        cx="50"
        cy="50"
        rx="45"
        ry="15"
        stroke="currentColor"
        strokeWidth="2.5"
        fill="none"
        transform="rotate(-30 50 50)"
      />
      
      {/* Glowing dot on the orbital path */}
      <circle
        cx="85"
        cy="28"
        r="5"
        fill={color}
      >
        <animate
          attributeName="opacity"
          values="0.7;1;0.7"
          dur="2s"
          repeatCount="indefinite"
        />
      </circle>
      
      {/* Glow effect for the dot */}
      <circle
        cx="85"
        cy="28"
        r="8"
        fill={color}
        opacity="0.3"
      >
        <animate
          attributeName="r"
          values="8;12;8"
          dur="2s"
          repeatCount="indefinite"
        />
        <animate
          attributeName="opacity"
          values="0.3;0.1;0.3"
          dur="2s"
          repeatCount="indefinite"
        />
      </circle>
    </svg>
  );
}

/**
 * Breathing logo variant for larger displays (like settings preview)
 */
export function BreathingLogo({ className = "h-20 w-20" }: { className?: string }) {
  let accent = "#8B5CF6";
  let accentLight = "#A78BFA";
  try {
    const theme = useTheme();
    accent = theme.accent.main;
    accentLight = theme.accent.light;
  } catch {
    // Not in context
  }

  return (
    <div className="relative flex items-center justify-center">
      {/* Breathing glow */}
      <div 
        className="absolute rounded-full animate-breathing"
        style={{
          width: "150%",
          height: "150%",
          background: `radial-gradient(circle, ${accent}30 0%, transparent 70%)`,
        }}
      />
      
      {/* Main logo */}
      <svg
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={`relative ${className}`}
      >
        {/* Main O circle with gradient stroke */}
        <defs>
          <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={accentLight} />
            <stop offset="100%" stopColor={accent} />
          </linearGradient>
        </defs>
        
        <circle
          cx="50"
          cy="50"
          r="30"
          stroke="url(#logoGradient)"
          strokeWidth="4"
          fill="none"
        />
        
        {/* Orbital ring */}
        <ellipse
          cx="50"
          cy="50"
          rx="45"
          ry="15"
          stroke="currentColor"
          strokeWidth="2.5"
          fill="none"
          transform="rotate(-30 50 50)"
          opacity="0.6"
        />
        
        {/* Glowing dot */}
        <circle cx="85" cy="28" r="6" fill={accent}>
          <animate
            attributeName="opacity"
            values="0.8;1;0.8"
            dur="2s"
            repeatCount="indefinite"
          />
        </circle>
        
        {/* Dot glow */}
        <circle cx="85" cy="28" r="10" fill={accent} opacity="0.3">
          <animate attributeName="r" values="10;14;10" dur="2s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.3;0.1;0.3" dur="2s" repeatCount="indefinite" />
        </circle>
      </svg>
    </div>
  );
}
