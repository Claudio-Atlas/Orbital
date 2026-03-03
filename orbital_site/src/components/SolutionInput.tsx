"use client";

import { useState, useRef } from "react";

export interface SolutionStep {
  description: string;
  math: string;
}

interface SolutionInputProps {
  onSubmit: (steps: SolutionStep[], images: File[]) => void;
  onBack: () => void;
  problem: string;
  isProcessing: boolean;
}

export function SolutionInput({ onSubmit, onBack, problem, isProcessing }: SolutionInputProps) {
  const [steps, setSteps] = useState<SolutionStep[]>([
    { description: "", math: "" },
  ]);
  const [images, setImages] = useState<File[]>([]);
  const [imagePreviews, setImagePreviews] = useState<string[]>([]);
  const [mode, setMode] = useState<"type" | "photo">("type");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const updateStep = (index: number, field: keyof SolutionStep, value: string) => {
    const newSteps = [...steps];
    newSteps[index] = { ...newSteps[index], [field]: value };
    setSteps(newSteps);
  };

  const addStep = () => {
    setSteps([...steps, { description: "", math: "" }]);
  };

  const removeStep = (index: number) => {
    if (steps.length <= 1) return;
    setSteps(steps.filter((_, i) => i !== index));
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;
    setImages((prev) => [...prev, ...files]);

    // Generate previews
    files.forEach((file) => {
      const reader = new FileReader();
      reader.onload = (ev) => {
        setImagePreviews((prev) => [...prev, ev.target?.result as string]);
      };
      reader.readAsDataURL(file);
    });
  };

  const removeImage = (index: number) => {
    setImages((prev) => prev.filter((_, i) => i !== index));
    setImagePreviews((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = () => {
    if (mode === "type") {
      const filledSteps = steps.filter((s) => s.description.trim() || s.math.trim());
      if (filledSteps.length === 0) return;
      onSubmit(filledSteps, []);
    } else {
      if (images.length === 0) return;
      onSubmit([], images);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
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
        <h2 className="text-lg font-semibold text-white">Provide Your Solution</h2>
        <p className="text-sm text-gray-500 mt-0.5">{problem}</p>
      </div>

      {/* Mode toggle */}
      <div className="flex gap-2">
        <button
          onClick={() => setMode("type")}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm transition-all ${
            mode === "type"
              ? "bg-violet-500/10 border border-violet-500/50 text-violet-300"
              : "bg-white/[0.03] border border-white/[0.08] text-gray-500 hover:text-gray-300"
          }`}
        >
          ⌨️ Type my steps
        </button>
        <button
          onClick={() => setMode("photo")}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm transition-all ${
            mode === "photo"
              ? "bg-violet-500/10 border border-violet-500/50 text-violet-300"
              : "bg-white/[0.03] border border-white/[0.08] text-gray-500 hover:text-gray-300"
          }`}
        >
          📸 Upload a photo
        </button>
      </div>

      {/* Typed steps */}
      {mode === "type" && (
        <div className="space-y-3">
          {steps.map((step, i) => (
            <div
              key={i}
              className="border border-white/[0.08] bg-white/[0.02] rounded-xl p-4 space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500 font-mono">Step {i + 1}</span>
                {steps.length > 1 && (
                  <button
                    onClick={() => removeStep(i)}
                    className="text-xs text-gray-600 hover:text-red-400 transition-colors"
                  >
                    Remove
                  </button>
                )}
              </div>
              <div>
                <label className="block text-[10px] uppercase tracking-widest text-gray-600 mb-1">
                  What are you doing in this step?
                </label>
                <input
                  type="text"
                  value={step.description}
                  onChange={(e) => updateStep(i, "description", e.target.value)}
                  placeholder="e.g., Find intersection points, Factor the quadratic..."
                  className="w-full px-3 py-2.5 rounded-lg bg-black/40 text-white/90 text-sm border border-white/[0.08] focus:border-violet-500/50 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-[10px] uppercase tracking-widest text-gray-600 mb-1">
                  Math (LaTeX or plain text)
                </label>
                <input
                  type="text"
                  value={step.math}
                  onChange={(e) => updateStep(i, "math", e.target.value)}
                  placeholder="e.g., x^2 - x - 2 = 0  or  \int_{-1}^{2} (x+2-x^2) dx"
                  className="w-full px-3 py-2.5 rounded-lg bg-black/40 text-green-400/80 text-sm font-mono border border-white/[0.08] focus:border-violet-500/50 focus:outline-none"
                />
              </div>
            </div>
          ))}

          <button
            onClick={addStep}
            className="w-full py-3 rounded-xl border border-dashed border-white/[0.1] text-sm text-gray-500 hover:text-violet-400 hover:border-violet-500/30 transition-all"
          >
            + Add Step
          </button>
        </div>
      )}

      {/* Photo upload */}
      {mode === "photo" && (
        <div className="space-y-4">
          <div
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-white/[0.1] rounded-xl p-8 text-center cursor-pointer hover:border-violet-500/30 hover:bg-violet-500/5 transition-all"
          >
            <div className="text-4xl mb-3">📸</div>
            <p className="text-sm text-gray-400 mb-1">
              Click to upload a photo of your work
            </p>
            <p className="text-xs text-gray-600">
              Supports: whiteboard, notebook, tablet screenshots, printed worksheets
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              onChange={handleImageUpload}
              className="hidden"
            />
          </div>

          {/* Image previews */}
          {imagePreviews.length > 0 && (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {imagePreviews.map((preview, i) => (
                <div key={i} className="relative group">
                  <img
                    src={preview}
                    alt={`Uploaded work ${i + 1}`}
                    className="w-full aspect-[4/3] object-cover rounded-lg border border-white/[0.08]"
                  />
                  <button
                    onClick={() => removeImage(i)}
                    className="absolute top-2 right-2 p-1 bg-black/80 rounded-full text-gray-400 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-all"
                  >
                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Submit */}
      <button
        onClick={handleSubmit}
        disabled={
          isProcessing ||
          (mode === "type" && !steps.some((s) => s.description.trim() || s.math.trim())) ||
          (mode === "photo" && images.length === 0)
        }
        className="w-full flex items-center justify-center gap-2 px-6 py-4 rounded-xl bg-violet-600 hover:bg-violet-500 text-white font-semibold transition-all disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {isProcessing ? (
          <>
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            Processing your solution...
          </>
        ) : (
          <>
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
            </svg>
            Generate Script from My Solution
          </>
        )}
      </button>

      <p className="text-[10px] text-gray-600 text-center">
        We&apos;ll convert your steps into a polished script with narration. You&apos;ll review it before the video is rendered.
      </p>
    </div>
  );
}
