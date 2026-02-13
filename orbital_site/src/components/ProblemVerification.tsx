"use client";

import { useState } from "react";
import { MathRenderer, StepDisplay } from "./MathRenderer";

interface Step {
  narration: string;
  latex: string;
}

interface ProblemVerificationProps {
  originalInput: string;
  parsedProblem: string;
  parsedLatex?: string;
  steps: Step[];
  estimatedMinutes: number;
  characterCount: number;
  isDark: boolean;
  onConfirm: () => void;
  onEdit: (newProblem: string) => void;
  onCancel: () => void;
}

export function ProblemVerification({
  originalInput,
  parsedProblem,
  parsedLatex,
  steps,
  estimatedMinutes,
  characterCount,
  isDark,
  onConfirm,
  onEdit,
  onCancel,
}: ProblemVerificationProps) {
  const [showSteps, setShowSteps] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editedProblem, setEditedProblem] = useState(parsedProblem);

  const handleEditSubmit = () => {
    if (editedProblem.trim() && editedProblem.trim() !== parsedProblem) {
      onEdit(editedProblem.trim());
    }
    setIsEditing(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h3 className={`text-xl font-semibold mb-2 ${isDark ? "text-white" : "text-gray-900"}`}>
          {isEditing ? "Edit Your Problem" : "Verify Your Problem"}
        </h3>
        <p className={`text-sm ${isDark ? "text-gray-500" : "text-gray-600"}`}>
          {isEditing 
            ? "Correct the problem text and we'll re-analyze it"
            : "Make sure we understood your problem correctly before generating"
          }
        </p>
      </div>

      {isEditing ? (
        /* Edit Mode */
        <div className="space-y-4">
          <textarea
            value={editedProblem}
            onChange={(e) => setEditedProblem(e.target.value)}
            className={`w-full p-5 rounded-2xl transition-all resize-none text-lg ${
              isDark 
                ? "bg-black/40 text-white placeholder-gray-600 border border-violet-500/30 focus:border-violet-500/60 focus:shadow-[0_0_25px_rgba(139,92,246,0.3)]" 
                : "bg-gray-50 text-gray-900 placeholder-gray-400 border border-violet-300/50 focus:border-violet-400"
            } focus:outline-none`}
            rows={3}
            autoFocus
          />
          
          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={() => {
                setIsEditing(false);
                setEditedProblem(parsedProblem);
              }}
              className={`flex-1 py-3.5 px-6 rounded-xl font-medium transition-all ${
                isDark 
                  ? "bg-white/[0.05] hover:bg-white/[0.08] border border-white/[0.08] text-white" 
                  : "bg-gray-100 hover:bg-gray-200 border border-gray-200 text-gray-700"
              }`}
            >
              Cancel Edit
            </button>
            <button
              onClick={handleEditSubmit}
              disabled={!editedProblem.trim()}
              className={`flex-1 py-3.5 px-6 rounded-xl font-semibold transition-all disabled:opacity-30 ${
                isDark 
                  ? "bg-white text-black hover:bg-gray-100" 
                  : "bg-gray-900 text-white hover:bg-gray-800"
              }`}
            >
              Re-analyze
            </button>
          </div>
        </div>
      ) : (
        /* Verification Mode */
        <>
          {/* Side by Side Comparison */}
          <div className="grid md:grid-cols-2 gap-4">
            {/* Left: Original Input */}
            <div className={`p-5 rounded-2xl ${isDark ? "bg-white/[0.03] border border-white/[0.08]" : "bg-gray-50 border border-gray-200"}`}>
              <div className={`text-xs font-medium uppercase tracking-widest mb-3 ${isDark ? "text-gray-500" : "text-gray-400"}`}>
                Your Input
              </div>
              <p className={`text-lg ${isDark ? "text-gray-300" : "text-gray-700"}`}>
                {originalInput}
              </p>
            </div>

            {/* Right: Parsed/Rendered Math */}
            <div className={`p-5 rounded-2xl ${isDark ? "bg-violet-500/10 border border-violet-500/20" : "bg-violet-50 border border-violet-200"}`}>
              <div className={`text-xs font-medium uppercase tracking-widest mb-3 ${isDark ? "text-violet-400" : "text-violet-600"}`}>
                We Understood
              </div>
              {parsedLatex ? (
                <div className={`text-lg ${isDark ? "text-white" : "text-gray-900"}`}>
                  <MathRenderer latex={parsedLatex} display={true} />
                </div>
              ) : (
                <p className={`text-lg ${isDark ? "text-white" : "text-gray-900"}`}>
                  {parsedProblem}
                </p>
              )}
            </div>
          </div>

          {/* Steps Preview Toggle */}
          <button
            onClick={() => setShowSteps(!showSteps)}
            className={`w-full py-3 px-4 rounded-xl text-sm font-medium flex items-center justify-between ${
              isDark 
                ? "bg-white/[0.03] hover:bg-white/[0.05] border border-white/[0.08]" 
                : "bg-gray-50 hover:bg-gray-100 border border-gray-200"
            }`}
          >
            <span className={isDark ? "text-gray-300" : "text-gray-700"}>
              Preview {steps.length} steps
            </span>
            <svg 
              className={`w-5 h-5 transition-transform ${showSteps ? "rotate-180" : ""} ${isDark ? "text-gray-400" : "text-gray-500"}`}
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          {/* Steps List (Collapsible) */}
          {showSteps && (
            <div className="space-y-3 max-h-80 overflow-y-auto">
              {steps.map((step, i) => (
                <StepDisplay
                  key={i}
                  stepNumber={i + 1}
                  narration={step.narration}
                  latex={step.latex}
                  isDark={isDark}
                />
              ))}
            </div>
          )}

          {/* Cost Display */}
          <div className={`p-5 rounded-2xl text-center ${isDark ? "bg-white/[0.03] border border-white/[0.08]" : "bg-gray-50 border border-gray-200"}`}>
            <div className={`text-sm mb-1 ${isDark ? "text-gray-500" : "text-gray-500"}`}>
              This video will use
            </div>
            <div className={`text-3xl font-semibold ${isDark ? "text-white" : "text-gray-900"}`}>
              {estimatedMinutes.toFixed(1)} minutes
            </div>
            <div className={`text-xs mt-1 ${isDark ? "text-gray-600" : "text-gray-400"}`}>
              {characterCount.toLocaleString()} characters of narration
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={() => {
                setEditedProblem(parsedProblem);
                setIsEditing(true);
              }}
              className={`flex-1 py-3.5 px-6 rounded-xl font-medium transition-all ${
                isDark 
                  ? "bg-white/[0.05] hover:bg-white/[0.08] border border-white/[0.08] text-white" 
                  : "bg-gray-100 hover:bg-gray-200 border border-gray-200 text-gray-700"
              }`}
            >
              Edit Problem
            </button>
            <button
              onClick={onConfirm}
              className={`flex-1 py-3.5 px-6 rounded-xl font-semibold transition-all ${
                isDark 
                  ? "bg-white text-black hover:bg-gray-100" 
                  : "bg-gray-900 text-white hover:bg-gray-800"
              }`}
            >
              Generate Video
            </button>
          </div>

          {/* Cancel Link */}
          <button
            onClick={onCancel}
            className={`w-full text-center text-sm ${isDark ? "text-gray-500 hover:text-gray-400" : "text-gray-500 hover:text-gray-600"}`}
          >
            Cancel
          </button>
        </>
      )}
    </div>
  );
}
