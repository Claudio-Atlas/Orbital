interface OrbitalLogoProps {
  className?: string;
}

export function OrbitalLogo({ className = "h-8 w-8" }: OrbitalLogoProps) {
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
        stroke="white"
        strokeWidth="4"
        fill="none"
      />
      
      {/* Orbital ring (ellipse tilted) */}
      <ellipse
        cx="50"
        cy="50"
        rx="45"
        ry="15"
        stroke="white"
        strokeWidth="2.5"
        fill="none"
        transform="rotate(-30 50 50)"
      />
      
      {/* Glowing dot on the orbital path */}
      <circle
        cx="85"
        cy="28"
        r="5"
        fill="#8B5CF6"
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
        fill="#8B5CF6"
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
