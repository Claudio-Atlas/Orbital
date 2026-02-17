"use client";

import { useTheme, ACCENT_PRESETS, AccentPreset } from "@/lib/theme-context";

const Icons = {
  check: (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
    </svg>
  ),
};

const PRESET_ORDER: AccentPreset[] = [
  "nebulaPurple",
  "oceanBlue",
  "cardinalRed",
  "forestGreen",
  "sunsetOrange",
  "electricPink",
  "cyberCyan",
];

/**
 * Horizontal row of accent color swatches - matches iOS AccentColorPicker
 */
export function AccentColorPicker() {
  const { accentPreset, setAccentPreset, isDark } = useTheme();

  return (
    <div className="flex items-center gap-3">
      {PRESET_ORDER.map((preset) => {
        const { colors } = ACCENT_PRESETS[preset];
        const isSelected = accentPreset === preset;

        return (
          <button
            key={preset}
            onClick={() => setAccentPreset(preset)}
            className="relative group"
            title={ACCENT_PRESETS[preset].name}
          >
            {/* Outer glow ring when selected */}
            <div
              className={`absolute inset-0 rounded-full transition-all duration-300 ${
                isSelected ? "scale-125 opacity-100" : "scale-100 opacity-0"
              }`}
              style={{
                background: `${colors.main}30`,
              }}
            />

            {/* Main color circle with gradient */}
            <div
              className={`relative w-9 h-9 rounded-full flex items-center justify-center transition-all duration-200 ${
                isSelected ? "scale-100" : "scale-90 hover:scale-100"
              }`}
              style={{
                background: `linear-gradient(135deg, ${colors.light} 0%, ${colors.main} 100%)`,
                boxShadow: isSelected
                  ? `0 0 20px ${colors.main}60, 0 4px 12px ${colors.main}40`
                  : `0 2px 8px ${colors.main}30`,
              }}
            >
              {/* Checkmark when selected */}
              {isSelected && (
                <span className="text-white drop-shadow-md">{Icons.check}</span>
              )}
            </div>
          </button>
        );
      })}
    </div>
  );
}

/**
 * Grid-style accent picker with labels - for settings sheet
 */
export function AccentColorPickerGrid() {
  const { accentPreset, setAccentPreset, isDark } = useTheme();

  return (
    <div className="grid grid-cols-4 sm:grid-cols-7 gap-3">
      {PRESET_ORDER.map((preset) => {
        const { name, colors } = ACCENT_PRESETS[preset];
        const isSelected = accentPreset === preset;

        return (
          <button
            key={preset}
            onClick={() => setAccentPreset(preset)}
            className={`flex flex-col items-center gap-2 p-3 rounded-xl transition-all ${
              isSelected
                ? isDark
                  ? "bg-white/10"
                  : "bg-gray-100"
                : isDark
                ? "hover:bg-white/5"
                : "hover:bg-gray-50"
            }`}
          >
            {/* Color swatch */}
            <div className="relative">
              <div
                className={`w-10 h-10 rounded-full transition-transform ${
                  isSelected ? "scale-100" : "scale-90"
                }`}
                style={{
                  background: `linear-gradient(135deg, ${colors.light} 0%, ${colors.main} 100%)`,
                  boxShadow: isSelected
                    ? `0 0 24px ${colors.main}50, 0 4px 12px ${colors.main}40`
                    : `0 2px 8px ${colors.main}25`,
                }}
              >
                {isSelected && (
                  <div className="absolute inset-0 flex items-center justify-center text-white">
                    {Icons.check}
                  </div>
                )}
              </div>

              {/* Glow ring */}
              {isSelected && (
                <div
                  className="absolute -inset-1.5 rounded-full animate-pulse"
                  style={{
                    background: `radial-gradient(circle, ${colors.main}30 0%, transparent 70%)`,
                  }}
                />
              )}
            </div>

            {/* Label */}
            <span
              className={`text-xs font-medium truncate max-w-full ${
                isDark ? "text-gray-400" : "text-gray-600"
              } ${isSelected ? "!text-[var(--accent)]" : ""}`}
            >
              {name.split(" ")[0]}
            </span>
          </button>
        );
      })}
    </div>
  );
}

/**
 * Single accent swatch for minimal UIs
 */
export function AccentSwatch({ preset, size = "md" }: { preset: AccentPreset; size?: "sm" | "md" | "lg" }) {
  const { colors } = ACCENT_PRESETS[preset];
  const sizeClasses = {
    sm: "w-5 h-5",
    md: "w-8 h-8",
    lg: "w-12 h-12",
  };

  return (
    <div
      className={`${sizeClasses[size]} rounded-full`}
      style={{
        background: `linear-gradient(135deg, ${colors.light} 0%, ${colors.main} 100%)`,
        boxShadow: `0 2px 8px ${colors.main}30`,
      }}
    />
  );
}
