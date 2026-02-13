"use client";

import { MathRenderer } from "./MathRenderer";

interface Step {
  narration: string;
  latex: string;
}

interface SolutionStepsProps {
  steps: Step[];
  isDark: boolean;
}

export function SolutionSteps({ steps, isDark }: SolutionStepsProps) {
  if (!steps || steps.length === 0) return null;

  return (
    <div className={`mt-8 rounded-2xl overflow-hidden ${
      isDark 
        ? "bg-white/[0.02] border border-white/[0.08]" 
        : "bg-gray-50 border border-gray-200"
    }`}>
      {/* Header */}
      <div className={`px-6 py-4 border-b ${
        isDark ? "border-white/[0.05]" : "border-gray-200"
      }`}>
        <h3 className={`text-lg font-semibold ${isDark ? "text-white" : "text-gray-900"}`}>
          Step-by-Step Solution
        </h3>
        <p className={`text-sm mt-1 ${isDark ? "text-gray-500" : "text-gray-600"}`}>
          {steps.length} steps • Scroll down for full solution
        </p>
      </div>

      {/* Steps List */}
      <div className="divide-y divide-white/[0.05]">
        {steps.map((step, i) => (
          <div 
            key={i} 
            className={`px-6 py-5 ${
              isDark ? "hover:bg-white/[0.02]" : "hover:bg-gray-100"
            } transition-colors`}
          >
            <div className="flex gap-4">
              {/* Step Number */}
              <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-sm font-semibold ${
                isDark 
                  ? "bg-violet-500/20 text-violet-400" 
                  : "bg-violet-100 text-violet-600"
              }`}>
                {i + 1}
              </div>

              {/* Step Content */}
              <div className="flex-1 min-w-0">
                {/* Narration */}
                <p className={`text-base leading-relaxed mb-3 ${
                  isDark ? "text-gray-300" : "text-gray-700"
                }`}>
                  {step.narration}
                </p>

                {/* Math (if present) */}
                {step.latex && (
                  <div className={`p-4 rounded-xl overflow-x-auto ${
                    isDark 
                      ? "bg-black/30 border border-white/[0.05]" 
                      : "bg-white border border-gray-200"
                  }`}>
                    <div className={isDark ? "text-white" : "text-gray-900"}>
                      <MathRenderer latex={step.latex} display={true} />
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className={`px-6 py-4 border-t text-center ${
        isDark ? "border-white/[0.05]" : "border-gray-200"
      }`}>
        <p className={`text-sm ${isDark ? "text-gray-600" : "text-gray-500"}`}>
          ✓ Solution complete
        </p>
      </div>
    </div>
  );
}
