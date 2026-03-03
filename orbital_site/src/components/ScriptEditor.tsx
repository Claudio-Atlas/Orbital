"use client";

import { useState, useCallback } from "react";
import { StepPreview, type ScriptStep } from "./StepPreview";
export type { ScriptStep } from "./StepPreview";
import { MathRenderer } from "./MathRenderer";

interface ScriptEditorProps {
  steps: ScriptStep[];
  onStepsChange: (steps: ScriptStep[]) => void;
  onApprove: (steps: ScriptStep[]) => void;
  onBack: () => void;
  problem: string;
  badge: "lean4_verified" | "ai_verified" | "teacher_verified";
}

const STEP_TYPES: { value: ScriptStep["type"]; label: string; icon: string }[] = [
  { value: "text", label: "Text", icon: "📝" },
  { value: "math", label: "Math", icon: "🔢" },
  { value: "mixed", label: "Mixed", icon: "📐" },
  { value: "transform", label: "Transform", icon: "🔄" },
  { value: "box", label: "Box (Answer)", icon: "✅" },
  { value: "graph", label: "Graph", icon: "📊" },
];

function StepCard({
  step,
  index,
  totalSteps,
  onUpdate,
  onDelete,
  onMoveUp,
  onMoveDown,
  isSelected,
  onSelect,
}: {
  step: ScriptStep;
  index: number;
  totalSteps: number;
  onUpdate: (updated: ScriptStep) => void;
  onDelete: () => void;
  onMoveUp: () => void;
  onMoveDown: () => void;
  isSelected: boolean;
  onSelect: () => void;
}) {
  const [latexMode, setLatexMode] = useState(false);

  return (
    <div
      onClick={onSelect}
      className={`border rounded-xl p-4 transition-all cursor-pointer ${
        isSelected
          ? "border-violet-500/50 bg-violet-500/5"
          : "border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.03]"
      }`}
    >
      {/* Step header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500 font-mono">#{step.step_number}</span>
          <select
            value={step.type}
            onChange={(e) =>
              onUpdate({ ...step, type: e.target.value as ScriptStep["type"] })
            }
            className="text-xs bg-white/[0.06] border border-white/[0.1] rounded-md px-2 py-1 text-gray-300 focus:outline-none focus:border-violet-500/50"
          >
            {STEP_TYPES.map((t) => (
              <option key={t.value} value={t.value}>
                {t.icon} {t.label}
              </option>
            ))}
          </select>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={(e) => { e.stopPropagation(); onMoveUp(); }}
            disabled={index === 0}
            className="p-1 text-gray-600 hover:text-gray-300 disabled:opacity-20 transition-colors"
            title="Move up"
          >
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5" />
            </svg>
          </button>
          <button
            onClick={(e) => { e.stopPropagation(); onMoveDown(); }}
            disabled={index === totalSteps - 1}
            className="p-1 text-gray-600 hover:text-gray-300 disabled:opacity-20 transition-colors"
            title="Move down"
          >
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
            </svg>
          </button>
          <button
            onClick={(e) => { e.stopPropagation(); onDelete(); }}
            className="p-1 text-gray-600 hover:text-red-400 transition-colors ml-1"
            title="Delete step"
          >
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Narration */}
      <div className="mb-3">
        <label className="block text-[10px] uppercase tracking-widest text-gray-600 mb-1">
          Narration
        </label>
        <textarea
          value={step.narration}
          onChange={(e) => onUpdate({ ...step, narration: e.target.value })}
          onClick={(e) => e.stopPropagation()}
          rows={2}
          className="w-full px-3 py-2 rounded-lg bg-black/40 text-white/90 text-sm border border-white/[0.08] focus:border-violet-500/50 focus:outline-none resize-none"
          placeholder="What the narrator will say..."
        />
      </div>

      {/* Math fields based on type */}
      {(step.type === "math" || step.type === "mixed" || step.type === "box") && (
        <div className="mb-2">
          <div className="flex items-center justify-between mb-1">
            <label className="text-[10px] uppercase tracking-widest text-gray-600">
              Math Display
            </label>
            <button
              onClick={(e) => { e.stopPropagation(); setLatexMode(!latexMode); }}
              className="text-[10px] text-violet-400 hover:text-violet-300 transition-colors"
            >
              {latexMode ? "Preview" : "LaTeX"}
            </button>
          </div>
          {latexMode ? (
            <textarea
              value={step.display_latex || ""}
              onChange={(e) => onUpdate({ ...step, display_latex: e.target.value })}
              onClick={(e) => e.stopPropagation()}
              rows={1}
              className="w-full px-3 py-2 rounded-lg bg-black/40 text-green-400 text-sm font-mono border border-white/[0.08] focus:border-violet-500/50 focus:outline-none resize-none"
              placeholder="LaTeX expression..."
            />
          ) : (
            <div
              onClick={(e) => { e.stopPropagation(); setLatexMode(true); }}
              className="w-full px-3 py-2 rounded-lg bg-black/40 border border-white/[0.08] min-h-[36px] flex items-center cursor-text hover:border-violet-500/30 transition-colors"
            >
              {step.display_latex ? (
                <MathRenderer latex={step.display_latex} display={false} />
              ) : (
                <span className="text-gray-600 text-sm">Click to add math...</span>
              )}
            </div>
          )}
        </div>
      )}

      {step.type === "transform" && (
        <div className="space-y-2 mb-2">
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="text-[10px] uppercase tracking-widest text-gray-600">From</label>
            </div>
            <textarea
              value={step.from_latex || ""}
              onChange={(e) => onUpdate({ ...step, from_latex: e.target.value })}
              onClick={(e) => e.stopPropagation()}
              rows={1}
              className="w-full px-3 py-2 rounded-lg bg-black/40 text-green-400 text-sm font-mono border border-white/[0.08] focus:border-violet-500/50 focus:outline-none resize-none"
              placeholder="Starting expression (LaTeX)..."
            />
            {step.from_latex && (
              <div className="mt-1 px-3 py-1 rounded bg-black/20">
                <MathRenderer latex={step.from_latex} display={false} />
              </div>
            )}
          </div>
          <div>
            <label className="text-[10px] uppercase tracking-widest text-gray-600 mb-1 block">To</label>
            <textarea
              value={step.to_latex || ""}
              onChange={(e) => onUpdate({ ...step, to_latex: e.target.value })}
              onClick={(e) => e.stopPropagation()}
              rows={1}
              className="w-full px-3 py-2 rounded-lg bg-black/40 text-green-400 text-sm font-mono border border-white/[0.08] focus:border-violet-500/50 focus:outline-none resize-none"
              placeholder="Result expression (LaTeX)..."
            />
            {step.to_latex && (
              <div className="mt-1 px-3 py-1 rounded bg-black/20">
                <MathRenderer latex={step.to_latex} display={false} />
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export function ScriptEditor({
  steps: initialSteps,
  onStepsChange,
  onApprove,
  onBack,
  problem,
  badge,
}: ScriptEditorProps) {
  const [steps, setSteps] = useState<ScriptStep[]>(initialSteps);
  const [selectedIndex, setSelectedIndex] = useState(0);

  const updateSteps = useCallback(
    (newSteps: ScriptStep[]) => {
      // Renumber steps
      const renumbered = newSteps.map((s, i) => ({ ...s, step_number: i + 1 }));
      setSteps(renumbered);
      onStepsChange(renumbered);
    },
    [onStepsChange]
  );

  const updateStep = (index: number, updated: ScriptStep) => {
    const newSteps = [...steps];
    newSteps[index] = updated;
    updateSteps(newSteps);
  };

  const deleteStep = (index: number) => {
    if (steps.length <= 1) return;
    const newSteps = steps.filter((_, i) => i !== index);
    updateSteps(newSteps);
    if (selectedIndex >= newSteps.length) setSelectedIndex(newSteps.length - 1);
  };

  const moveStep = (index: number, direction: -1 | 1) => {
    const newIndex = index + direction;
    if (newIndex < 0 || newIndex >= steps.length) return;
    const newSteps = [...steps];
    [newSteps[index], newSteps[newIndex]] = [newSteps[newIndex], newSteps[index]];
    updateSteps(newSteps);
    setSelectedIndex(newIndex);
  };

  const addStep = (afterIndex: number) => {
    const newStep: ScriptStep = {
      step_number: afterIndex + 2,
      type: "text",
      narration: "",
    };
    const newSteps = [...steps];
    newSteps.splice(afterIndex + 1, 0, newStep);
    updateSteps(newSteps);
    setSelectedIndex(afterIndex + 1);
  };

  const selectedStep = steps[selectedIndex] || steps[0];

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <button
            onClick={onBack}
            className="text-sm text-gray-500 hover:text-gray-300 transition-colors mb-2 flex items-center gap-1"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
            Back
          </button>
          <h2 className="text-lg font-semibold text-white">Edit Script</h2>
          <p className="text-sm text-gray-500 mt-0.5 max-w-xl truncate">{problem}</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs text-gray-500">{steps.length} steps</span>
          <span className="text-xs px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400">
            👨‍🏫 Teacher Verified
          </span>
        </div>
      </div>

      {/* Split view */}
      <div className="grid grid-cols-2 gap-6 min-h-[600px]">
        {/* Left: Editor */}
        <div className="space-y-3 overflow-y-auto max-h-[700px] pr-2 scrollbar-thin">
          {steps.map((step, i) => (
            <div key={`step-${i}`}>
              <StepCard
                step={step}
                index={i}
                totalSteps={steps.length}
                onUpdate={(updated) => updateStep(i, updated)}
                onDelete={() => deleteStep(i)}
                onMoveUp={() => moveStep(i, -1)}
                onMoveDown={() => moveStep(i, 1)}
                isSelected={selectedIndex === i}
                onSelect={() => setSelectedIndex(i)}
              />
              {/* Add step button between cards */}
              <div className="flex justify-center my-1">
                <button
                  onClick={() => addStep(i)}
                  className="text-[10px] text-gray-600 hover:text-violet-400 transition-colors px-2 py-0.5 rounded hover:bg-violet-500/5"
                >
                  + Add step
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Right: Preview */}
        <div className="space-y-4">
          <div className="sticky top-0">
            <label className="block text-[10px] uppercase tracking-widest text-gray-600 mb-2">
              Preview
            </label>
            <StepPreview step={selectedStep} totalSteps={steps.length} />

            {/* Step navigation */}
            <div className="flex items-center justify-center gap-4 mt-3">
              <button
                onClick={() => setSelectedIndex(Math.max(0, selectedIndex - 1))}
                disabled={selectedIndex === 0}
                className="p-2 text-gray-500 hover:text-white disabled:opacity-20 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
                </svg>
              </button>
              <div className="flex gap-1.5">
                {steps.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setSelectedIndex(i)}
                    className={`w-2 h-2 rounded-full transition-all ${
                      i === selectedIndex ? "bg-violet-500 scale-125" : "bg-white/[0.15] hover:bg-white/[0.3]"
                    }`}
                  />
                ))}
              </div>
              <button
                onClick={() => setSelectedIndex(Math.min(steps.length - 1, selectedIndex + 1))}
                disabled={selectedIndex === steps.length - 1}
                className="p-2 text-gray-500 hover:text-white disabled:opacity-20 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                </svg>
              </button>
            </div>

            <p className="text-[10px] text-gray-600 text-center mt-2">
              ⚠️ Preview is approximate. Final video may differ slightly in layout and animation.
            </p>

            {/* Approve button */}
            <button
              onClick={() => onApprove(steps)}
              className="w-full mt-6 flex items-center justify-center gap-2 px-6 py-4 rounded-xl bg-green-600 hover:bg-green-500 text-white font-semibold transition-all"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Approve &amp; Generate Video
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
