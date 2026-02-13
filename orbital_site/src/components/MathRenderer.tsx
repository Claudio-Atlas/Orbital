"use client";

import { useEffect, useRef } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";

interface MathRendererProps {
  latex: string;
  display?: boolean; // true for block mode, false for inline
  className?: string;
}

export function MathRenderer({ latex, display = true, className = "" }: MathRendererProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current && latex) {
      try {
        katex.render(latex, containerRef.current, {
          displayMode: display,
          throwOnError: false,
          trust: true,
        });
      } catch (e) {
        // If KaTeX fails, just show the raw latex
        containerRef.current.textContent = latex;
      }
    }
  }, [latex, display]);

  return <div ref={containerRef} className={className} />;
}

interface StepDisplayProps {
  stepNumber: number;
  narration: string;
  latex: string;
  isDark: boolean;
}

export function StepDisplay({ stepNumber, narration, latex, isDark }: StepDisplayProps) {
  return (
    <div className={`p-4 rounded-xl ${isDark ? "bg-white/[0.03]" : "bg-gray-50"}`}>
      <div className="flex items-start gap-4">
        <span className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-sm font-semibold ${
          isDark ? "bg-violet-500/20 text-violet-400" : "bg-violet-100 text-violet-600"
        }`}>
          {stepNumber}
        </span>
        <div className="flex-1 min-w-0">
          <p className={`text-sm mb-2 ${isDark ? "text-gray-300" : "text-gray-700"}`}>
            {narration}
          </p>
          {latex && (
            <div className={`overflow-x-auto ${isDark ? "text-white" : "text-gray-900"}`}>
              <MathRenderer latex={latex} display={true} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
