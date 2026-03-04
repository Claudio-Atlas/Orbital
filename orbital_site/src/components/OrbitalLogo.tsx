"use client";

import { useTheme } from "@/lib/theme-context";

interface OrbitalLogoProps {
  className?: string;
  accentColor?: string;
}

export function OrbitalLogo({ className = "h-8 w-8", accentColor }: OrbitalLogoProps) {
  const color = accentColor || "#00E5FF";
  
  // 3:2 Lissajous curve: x = sin(3t), y = sin(2t)
  // Generate SVG path points
  const points: string[] = [];
  for (let i = 0; i <= 200; i++) {
    const t = (i / 200) * Math.PI * 2;
    const x = 50 + 35 * Math.sin(3 * t);
    const y = 50 - 28 * Math.sin(2 * t);
    points.push(`${x.toFixed(2)},${y.toFixed(2)}`);
  }
  const pathD = `M${points.join("L")}Z`;
  
  return (
    <svg
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      style={{ transform: "rotate(180deg)" }}
    >
      {/* Glow layer */}
      <path
        d={pathD}
        stroke={color}
        strokeWidth="5"
        strokeOpacity="0.2"
        fill="none"
      />
      {/* Core line */}
      <path
        d={pathD}
        stroke={color}
        strokeWidth="2"
        strokeOpacity="1"
        fill="none"
      />
    </svg>
  );
}

/**
 * Breathing logo variant for larger displays
 */
export function BreathingLogo({ className = "h-20 w-20" }: { className?: string }) {
  const color = "#00E5FF";

  const points: string[] = [];
  for (let i = 0; i <= 200; i++) {
    const t = (i / 200) * Math.PI * 2;
    const x = 50 + 35 * Math.sin(3 * t);
    const y = 50 - 28 * Math.sin(2 * t);
    points.push(`${x.toFixed(2)},${y.toFixed(2)}`);
  }
  const pathD = `M${points.join("L")}Z`;

  return (
    <div className="relative flex items-center justify-center">
      <div 
        className="absolute rounded-full animate-breathing"
        style={{
          width: "150%",
          height: "150%",
          background: `radial-gradient(circle, ${color}30 0%, transparent 70%)`,
        }}
      />
      <svg
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={`relative ${className}`}
        style={{ transform: "rotate(180deg)" }}
      >
        <path d={pathD} stroke={color} strokeWidth="6" strokeOpacity="0.15" fill="none" />
        <path d={pathD} stroke={color} strokeWidth="2.5" strokeOpacity="1" fill="none" />
      </svg>
    </div>
  );
}
