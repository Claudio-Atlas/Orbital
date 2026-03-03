"use client";

import { MathRenderer } from "./MathRenderer";

export interface ScriptStep {
  step_number: number;
  type: "text" | "math" | "mixed" | "transform" | "box" | "graph";
  narration: string;
  display_latex?: string;
  from_latex?: string;
  to_latex?: string;
  graph_kind?: string;
  functions?: string[];
}

interface StepPreviewProps {
  step: ScriptStep;
  totalSteps: number;
}

export function StepPreview({ step, totalSteps }: StepPreviewProps) {
  return (
    <div className="aspect-video bg-black rounded-xl border border-white/[0.06] flex flex-col items-center justify-center p-8 relative overflow-hidden">
      {/* Step counter */}
      <div className="absolute top-3 right-3 text-xs text-gray-600">
        Step {step.step_number} / {totalSteps}
      </div>

      {/* Badge area */}
      <div className="absolute top-3 left-3">
        <span className="text-[10px] text-violet-400 bg-violet-500/10 px-2 py-0.5 rounded-full">
          {step.type}
        </span>
      </div>

      {/* Content */}
      <div className="flex flex-col items-center gap-4 max-w-[90%]">
        {/* Text or mixed: show narration prominently */}
        {(step.type === "text" || step.type === "mixed") && (
          <p className="text-white/90 text-sm text-center leading-relaxed">
            {step.narration}
          </p>
        )}

        {/* Math display */}
        {step.type === "math" && step.display_latex && (
          <div className="text-white">
            <MathRenderer latex={step.display_latex} display={true} className="text-xl" />
          </div>
        )}

        {step.type === "mixed" && step.display_latex && (
          <div className="text-white">
            <MathRenderer latex={step.display_latex} display={true} />
          </div>
        )}

        {/* Transform: from → to */}
        {step.type === "transform" && (
          <div className="flex flex-col items-center gap-3">
            {step.from_latex && (
              <div className="text-white/60">
                <MathRenderer latex={step.from_latex} display={true} />
              </div>
            )}
            <svg className="w-4 h-4 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3" />
            </svg>
            {step.to_latex && (
              <div className="text-white">
                <MathRenderer latex={step.to_latex} display={true} />
              </div>
            )}
          </div>
        )}

        {/* Box (final answer) */}
        {step.type === "box" && step.display_latex && (
          <div className="border-2 border-[#39FF14] rounded-lg px-6 py-3">
            <div className="text-white">
              <MathRenderer latex={step.display_latex} display={true} />
            </div>
          </div>
        )}

        {/* Graph placeholder */}
        {step.type === "graph" && (
          <div className="w-full h-32 border border-white/[0.1] rounded-lg flex items-center justify-center">
            <span className="text-gray-500 text-xs">
              📊 Graph: {step.graph_kind || "function_plot"}
              {step.functions && ` — ${step.functions.join(", ")}`}
            </span>
          </div>
        )}

        {/* Narration for non-text types (shown as subtitle) */}
        {step.type !== "text" && step.type !== "mixed" && (
          <p className="text-white/50 text-xs text-center italic mt-2 max-w-[80%]">
            &ldquo;{step.narration}&rdquo;
          </p>
        )}
      </div>
    </div>
  );
}
