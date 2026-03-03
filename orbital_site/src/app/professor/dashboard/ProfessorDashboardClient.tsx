"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { OrbitalLogo } from "@/components/OrbitalLogo";
import { PathSelector, type PipelinePath } from "@/components/PathSelector";
import { ScriptEditor, type ScriptStep } from "@/components/ScriptEditor";
import { SolutionInput, type SolutionStep } from "@/components/SolutionInput";

type DetailLevel = "quick" | "standard" | "detailed";
type JobStatus = "idle" | "generating" | "reviewing" | "processing_solution" | "circle" | "lean" | "tts" | "rendering" | "complete" | "error";

type VideoItem = {
  id: string;
  problem: string;
  detailLevel: DetailLevel;
  path: PipelinePath;
  status: JobStatus;
  badge: "lean4_verified" | "ai_verified" | "teacher_verified";
  createdAt: string;
  duration: number | null;
  videoUrl: string | null;
};

type DashboardView = "main" | "editor" | "solution_input";

const Icons = {
  sparkles: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
    </svg>
  ),
  video: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="m15.75 10.5 4.72-4.72a.75.75 0 0 1 1.28.53v11.38a.75.75 0 0 1-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25h-9A2.25 2.25 0 0 0 2.25 7.5v9a2.25 2.25 0 0 0 2.25 2.25Z" />
    </svg>
  ),
  settings: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
    </svg>
  ),
  chevronDown: (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
    </svg>
  ),
  logout: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9" />
    </svg>
  ),
  play: (
    <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.91 11.672a.375.375 0 0 1 0 .656l-5.603 3.113a.375.375 0 0 1-.557-.328V8.887c0-.286.307-.466.557-.327l5.603 3.112Z" />
    </svg>
  ),
};

const DETAIL_LEVELS = [
  { value: "quick" as DetailLevel, label: "Quick", desc: "~90 seconds", icon: "⚡" },
  { value: "standard" as DetailLevel, label: "Standard", desc: "~3-4 min", icon: "📐" },
  { value: "detailed" as DetailLevel, label: "Detailed", desc: "~6+ min", icon: "🔬" },
];

const STATUS_LABELS: Record<JobStatus, { label: string; color: string }> = {
  idle: { label: "Ready", color: "text-gray-500" },
  generating: { label: "Writing script...", color: "text-violet-400" },
  reviewing: { label: "Ready for review", color: "text-amber-400" },
  processing_solution: { label: "Processing your solution...", color: "text-violet-400" },
  circle: { label: "Verifying mathematics...", color: "text-cyan-400" },
  lean: { label: "Formally proving...", color: "text-cyan-400" },
  tts: { label: "Generating narration...", color: "text-violet-400" },
  rendering: { label: "Rendering video...", color: "text-amber-400" },
  complete: { label: "Complete", color: "text-green-400" },
  error: { label: "Error", color: "text-red-400" },
};

const BADGE_LABELS: Record<string, { label: string; icon: string; color: string }> = {
  lean4_verified: { label: "Lean 4 Verified", icon: "🏛️", color: "text-cyan-400 bg-cyan-500/10" },
  ai_verified: { label: "AI Verified", icon: "✅", color: "text-green-400 bg-green-500/10" },
  teacher_verified: { label: "Teacher Verified", icon: "👨‍🏫", color: "text-amber-400 bg-amber-500/10" },
};

// Mock: convert professor solution to script steps
function mockProfessorStepsToScript(steps: SolutionStep[], problem: string): ScriptStep[] {
  const script: ScriptStep[] = [
    {
      step_number: 1,
      type: "text",
      narration: `Let's work through this problem: ${problem}`,
    },
  ];
  steps.forEach((s, i) => {
    script.push({
      step_number: i + 2,
      type: s.math ? "mixed" : "text",
      narration: s.description || `Step ${i + 1}`,
      display_latex: s.math || undefined,
    });
  });
  script.push({
    step_number: steps.length + 2,
    type: "text",
    narration: "And that's our solution! The key takeaway here is understanding each step and why it works.",
  });
  return script;
}

// Mock: generate AI script
function mockAIScript(problem: string, detailLevel: DetailLevel): ScriptStep[] {
  return [
    { step_number: 1, type: "text", narration: `Today we're going to solve: ${problem}. Let's break it down step by step.` },
    { step_number: 2, type: "text", narration: "First, let's understand what the problem is asking us to find." },
    { step_number: 3, type: "math", narration: "We start by setting up our equation.", display_latex: "x^2 - x - 2 = 0" },
    { step_number: 4, type: "transform", narration: "Let's factor this quadratic.", from_latex: "x^2 - x - 2 = 0", to_latex: "(x-2)(x+1) = 0" },
    { step_number: 5, type: "math", narration: "Setting each factor equal to zero gives us our solutions.", display_latex: "x = 2 \\quad \\text{or} \\quad x = -1" },
    { step_number: 6, type: "box", narration: "And there's our answer!", display_latex: "x = -1, \\quad x = 2" },
    { step_number: 7, type: "text", narration: "Remember: when you factor a quadratic, you're looking for two numbers that multiply to give you the constant term and add to give you the middle coefficient." },
  ];
}

export default function ProfessorDashboardClient() {
  const { user, profile, loading, signOut } = useAuth();
  const router = useRouter();

  // Main state
  const [problem, setProblem] = useState("");
  const [detailLevel, setDetailLevel] = useState<DetailLevel>("standard");
  const [selectedPath, setSelectedPath] = useState<PipelinePath | null>(null);
  const [leanEnabled, setLeanEnabled] = useState(true);
  const [showNotes, setShowNotes] = useState(false);
  const [notes, setNotes] = useState("");
  const [jobStatus, setJobStatus] = useState<JobStatus>("idle");
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [activeTab, setActiveTab] = useState<"dashboard" | "library" | "settings">("dashboard");

  // Editor state
  const [view, setView] = useState<DashboardView>("main");
  const [scriptSteps, setScriptSteps] = useState<ScriptStep[]>([]);
  const [isProcessingSolution, setIsProcessingSolution] = useState(false);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [loading, user, router]);

  const getCostEstimate = () => {
    if (!selectedPath) return detailLevel === "quick" ? "~$0.35" : detailLevel === "standard" ? "~$0.55" : "~$0.75";
    switch (selectedPath) {
      case "full_ai": return detailLevel === "quick" ? "~$0.82" : detailLevel === "standard" ? "~$0.98" : "~$1.26";
      case "ai_review": return detailLevel === "quick" ? "~$0.12" : detailLevel === "standard" ? "~$0.28" : "~$0.56";
      case "professor_source": return detailLevel === "quick" ? "~$0.13" : detailLevel === "standard" ? "~$0.30" : "~$0.62";
    }
  };

  const getBadge = (): VideoItem["badge"] => {
    if (selectedPath === "full_ai") return leanEnabled ? "lean4_verified" : "ai_verified";
    return "teacher_verified";
  };

  // Path A: Full AI pipeline
  const handleFullAI = () => {
    if (!problem.trim()) return;
    setJobStatus("generating");

    // Simulate full pipeline
    setTimeout(() => setJobStatus("circle"), 2000);
    setTimeout(() => {
      if (leanEnabled) {
        setJobStatus("lean");
        setTimeout(() => setJobStatus("tts"), 3000);
      } else {
        setJobStatus("tts");
      }
    }, 5000);
    setTimeout(() => setJobStatus("rendering"), leanEnabled ? 9000 : 7000);
    setTimeout(() => {
      setJobStatus("complete");
      addVideo(getBadge());
    }, leanEnabled ? 12000 : 10000);
  };

  // Path B: AI draft → editor
  const handleAIReview = () => {
    if (!problem.trim()) return;
    setJobStatus("generating");

    // Simulate script generation, then open editor
    setTimeout(() => {
      const script = mockAIScript(problem, detailLevel);
      setScriptSteps(script);
      setJobStatus("reviewing");
      setView("editor");
    }, 2000);
  };

  // Path C: Professor provides solution
  const handleProfessorSource = () => {
    if (!problem.trim()) return;
    setView("solution_input");
  };

  // Handle solution submission (Path C)
  const handleSolutionSubmit = (steps: SolutionStep[], images: File[]) => {
    setIsProcessingSolution(true);

    if (images.length > 0) {
      // TODO: OCR processing — for now mock it
      setTimeout(() => {
        const mockExtracted: SolutionStep[] = [
          { description: "Set up the equation", math: "x^2 + 2x - 3 = 0" },
          { description: "Factor", math: "(x+3)(x-1) = 0" },
          { description: "Solve", math: "x = -3, \\quad x = 1" },
        ];
        const script = mockProfessorStepsToScript(mockExtracted, problem);
        setScriptSteps(script);
        setIsProcessingSolution(false);
        setView("editor");
      }, 3000);
    } else {
      // Convert typed steps to script
      setTimeout(() => {
        const script = mockProfessorStepsToScript(steps, problem);
        setScriptSteps(script);
        setIsProcessingSolution(false);
        setView("editor");
      }, 1500);
    }
  };

  // Handle script approval (from editor)
  const handleApprove = (steps: ScriptStep[]) => {
    setView("main");
    setJobStatus("tts");
    setScriptSteps(steps);

    // Simulate TTS → render → complete
    setTimeout(() => setJobStatus("rendering"), 3000);
    setTimeout(() => {
      setJobStatus("complete");
      addVideo("teacher_verified");
    }, 6000);
  };

  const addVideo = (badge: VideoItem["badge"]) => {
    const newVideo: VideoItem = {
      id: crypto.randomUUID(),
      problem: problem.trim(),
      detailLevel,
      path: selectedPath || "full_ai",
      status: "complete",
      badge,
      createdAt: new Date().toISOString(),
      duration: detailLevel === "quick" ? 90 : detailLevel === "standard" ? 210 : 360,
      videoUrl: null,
    };
    setVideos((prev) => [newVideo, ...prev]);
    setProblem("");
    setNotes("");
    setSelectedPath(null);
  };

  const handleGenerate = () => {
    switch (selectedPath) {
      case "full_ai": return handleFullAI();
      case "ai_review": return handleAIReview();
      case "professor_source": return handleProfessorSource();
    }
  };

  const handleSignOut = async () => {
    await signOut();
    router.push("/");
  };

  const isGenerating = jobStatus !== "idle" && jobStatus !== "complete" && jobStatus !== "error" && jobStatus !== "reviewing";

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Top Nav */}
      <nav className="border-b border-white/[0.06] px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/" className="flex items-center gap-2 text-white/80 hover:text-white transition-colors">
              <OrbitalLogo />
              <span className="font-semibold text-lg">Orbital</span>
              <span className="text-xs text-violet-400 bg-violet-500/10 px-2 py-0.5 rounded-full ml-1">Professor</span>
            </Link>
            <div className="flex gap-1">
              {[
                { key: "dashboard" as const, label: "Dashboard", icon: Icons.sparkles },
                { key: "library" as const, label: "Library", icon: Icons.video },
                { key: "settings" as const, label: "Settings", icon: Icons.settings },
              ].map((tab) => (
                <button
                  key={tab.key}
                  onClick={() => { setActiveTab(tab.key); setView("main"); }}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition-all ${
                    activeTab === tab.key
                      ? "bg-white/[0.08] text-white"
                      : "text-gray-500 hover:text-gray-300 hover:bg-white/[0.03]"
                  }`}
                >
                  {tab.icon}
                  {tab.label}
                </button>
              ))}
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-500">{user?.email}</span>
            <button
              onClick={handleSignOut}
              className="flex items-center gap-2 text-sm text-gray-500 hover:text-white transition-colors"
            >
              {Icons.logout}
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Dashboard Tab */}
        {activeTab === "dashboard" && view === "main" && (
          <div className="space-y-8">
            {/* Problem Submission */}
            <div className="bg-gradient-to-b from-white/[0.06] to-white/[0.02] border border-white/[0.08] rounded-2xl p-8">
              <h2 className="text-xl font-semibold mb-6">Generate a Video</h2>

              {/* Problem Input */}
              <div className="mb-6">
                <label className="block text-xs font-medium uppercase tracking-widest text-gray-500 mb-2">
                  Math Problem
                </label>
                <textarea
                  value={problem}
                  onChange={(e) => setProblem(e.target.value)}
                  placeholder="Find the area enclosed by y = x + 2 and y = x²"
                  rows={3}
                  className="w-full px-4 py-3.5 rounded-xl bg-black/40 text-white placeholder-gray-600 border border-white/[0.08] focus:border-violet-500/50 focus:outline-none resize-none text-lg"
                />
              </div>

              {/* Path Selection */}
              <div className="mb-6">
                <PathSelector selected={selectedPath} onSelect={setSelectedPath} />
              </div>

              {/* Detail Level */}
              <div className="mb-6">
                <label className="block text-xs font-medium uppercase tracking-widest text-gray-500 mb-3">
                  Detail Level
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {DETAIL_LEVELS.map((level) => (
                    <button
                      key={level.value}
                      onClick={() => setDetailLevel(level.value)}
                      className={`p-4 rounded-xl border text-left transition-all ${
                        detailLevel === level.value
                          ? "border-violet-500/50 bg-violet-500/10"
                          : "border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.04]"
                      }`}
                    >
                      <div className="flex items-center gap-2 mb-1">
                        <span>{level.icon}</span>
                        <span className={`font-medium ${detailLevel === level.value ? "text-violet-300" : "text-white"}`}>
                          {level.label}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500">{level.desc}</p>
                    </button>
                  ))}
                </div>
              </div>

              {/* Lean toggle (only for Path A) */}
              {selectedPath === "full_ai" && (
                <div className="mb-6 flex items-center gap-3">
                  <button
                    onClick={() => setLeanEnabled(!leanEnabled)}
                    className={`relative w-11 h-6 rounded-full transition-colors ${
                      leanEnabled ? "bg-violet-600" : "bg-white/[0.1]"
                    }`}
                  >
                    <div
                      className={`absolute top-0.5 w-5 h-5 rounded-full bg-white transition-transform ${
                        leanEnabled ? "translate-x-[22px]" : "translate-x-0.5"
                      }`}
                    />
                  </button>
                  <div>
                    <span className="text-sm text-gray-300">Verify with Lean 4</span>
                    <p className="text-xs text-gray-600">Formal mathematical proof (+~$0.10)</p>
                  </div>
                </div>
              )}

              {/* Notes (collapsible) */}
              <div className="mb-6">
                <button
                  onClick={() => setShowNotes(!showNotes)}
                  className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-300 transition-colors"
                >
                  <span className={`transition-transform ${showNotes ? "rotate-180" : ""}`}>
                    {Icons.chevronDown}
                  </span>
                  Notes for AI (optional)
                </button>
                {showNotes && (
                  <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="e.g., 'Emphasize the geometric interpretation' or 'Skip the factoring — they already know that'"
                    rows={2}
                    className="w-full mt-3 px-4 py-3 rounded-xl bg-black/40 text-white placeholder-gray-600 border border-white/[0.08] focus:border-violet-500/50 focus:outline-none resize-none text-sm"
                  />
                )}
              </div>

              {/* Generate Button + Status */}
              <div className="flex items-center gap-4">
                <button
                  onClick={handleGenerate}
                  disabled={!problem.trim() || !selectedPath || isGenerating}
                  className="flex items-center gap-2 px-8 py-4 rounded-xl bg-violet-600 hover:bg-violet-500 text-white font-semibold transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  {Icons.sparkles}
                  {selectedPath === "professor_source" ? "Provide My Solution" : "Generate Video"}
                </button>
                {jobStatus !== "idle" && (
                  <div className="flex items-center gap-3">
                    {isGenerating && (
                      <div className="w-5 h-5 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
                    )}
                    {jobStatus === "complete" && <span className="text-green-400">✓</span>}
                    <span className={`text-sm ${STATUS_LABELS[jobStatus].color}`}>
                      {STATUS_LABELS[jobStatus].label}
                    </span>
                  </div>
                )}
              </div>

              {/* Cost + Badge Estimate */}
              {selectedPath && (
                <div className="mt-4 flex items-center gap-3 text-xs text-gray-600">
                  <span>Est. cost: <span className="text-gray-400">{getCostEstimate()}</span></span>
                  <span>•</span>
                  <span className={`px-2 py-0.5 rounded-full ${BADGE_LABELS[getBadge()].color}`}>
                    {BADGE_LABELS[getBadge()].icon} {BADGE_LABELS[getBadge()].label}
                  </span>
                  <span>•</span>
                  <span>
                    {detailLevel === "quick" ? "~90s video" : detailLevel === "standard" ? "~3-4 min video" : "~6+ min video"}
                  </span>
                </div>
              )}
            </div>

            {/* Recent Videos */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Recent Videos</h3>
              {videos.length === 0 ? (
                <div className="bg-white/[0.02] border border-white/[0.06] rounded-2xl p-12 text-center">
                  <div className="text-gray-600 mb-2">{Icons.video}</div>
                  <p className="text-gray-500 text-sm">No videos yet. Submit your first problem above!</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {videos.map((video) => (
                    <div
                      key={video.id}
                      className="bg-white/[0.03] border border-white/[0.08] rounded-xl p-5 hover:bg-white/[0.05] transition-all cursor-pointer"
                    >
                      <div className="aspect-video bg-white/[0.04] rounded-lg mb-4 flex items-center justify-center text-gray-600">
                        {Icons.play}
                      </div>
                      <p className="text-sm text-white font-medium mb-2 line-clamp-2">{video.problem}</p>
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-gray-500">{new Date(video.createdAt).toLocaleDateString()}</span>
                        <span className={`px-2 py-0.5 rounded-full ${BADGE_LABELS[video.badge].color}`}>
                          {BADGE_LABELS[video.badge].icon} {BADGE_LABELS[video.badge].label}
                        </span>
                      </div>
                      {video.duration && (
                        <p className="text-xs text-gray-600 mt-1">
                          {Math.floor(video.duration / 60)}:{String(video.duration % 60).padStart(2, "0")}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Script Editor View (Path B & C) */}
        {activeTab === "dashboard" && view === "editor" && (
          <ScriptEditor
            steps={scriptSteps}
            onStepsChange={setScriptSteps}
            onApprove={handleApprove}
            onBack={() => { setView("main"); setJobStatus("idle"); }}
            problem={problem}
            badge={getBadge()}
          />
        )}

        {/* Solution Input View (Path C) */}
        {activeTab === "dashboard" && view === "solution_input" && (
          <SolutionInput
            onSubmit={handleSolutionSubmit}
            onBack={() => { setView("main"); setJobStatus("idle"); }}
            problem={problem}
            isProcessing={isProcessingSolution}
          />
        )}

        {/* Library Tab */}
        {activeTab === "library" && (
          <div>
            <h2 className="text-xl font-semibold mb-6">Video Library</h2>
            {videos.length === 0 ? (
              <div className="bg-white/[0.02] border border-white/[0.06] rounded-2xl p-12 text-center">
                <p className="text-gray-500">Your video library is empty. Generate your first video from the Dashboard.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {videos.map((video) => (
                  <div
                    key={video.id}
                    className="bg-white/[0.03] border border-white/[0.08] rounded-xl p-5 hover:bg-white/[0.05] transition-all cursor-pointer"
                  >
                    <div className="aspect-video bg-white/[0.04] rounded-lg mb-4 flex items-center justify-center text-gray-600">
                      {Icons.play}
                    </div>
                    <p className="text-sm text-white font-medium mb-2 line-clamp-2">{video.problem}</p>
                    <div className="flex items-center justify-between text-xs">
                      <div className="flex items-center gap-2 text-gray-500">
                        <span className="capitalize">{video.detailLevel}</span>
                        <span>•</span>
                        <span>{new Date(video.createdAt).toLocaleDateString()}</span>
                      </div>
                      <span className={`px-2 py-0.5 rounded-full ${BADGE_LABELS[video.badge].color}`}>
                        {BADGE_LABELS[video.badge].icon}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === "settings" && (
          <div>
            <h2 className="text-xl font-semibold mb-6">Settings</h2>
            <div className="bg-white/[0.03] border border-white/[0.08] rounded-2xl p-8 space-y-6">
              <div>
                <h3 className="text-sm font-medium text-gray-400 uppercase tracking-widest mb-3">Account</h3>
                <p className="text-sm text-gray-300">{user?.email}</p>
                <p className="text-xs text-gray-600 mt-1">Professor account</p>
              </div>
              <div className="border-t border-white/[0.06] pt-6">
                <h3 className="text-sm font-medium text-gray-400 uppercase tracking-widest mb-3">Default Settings</h3>
                <p className="text-sm text-gray-500">Coming soon — set your preferred defaults for detail level, Lean verification, and path.</p>
              </div>
              <div className="border-t border-white/[0.06] pt-6">
                <h3 className="text-sm font-medium text-gray-400 uppercase tracking-widest mb-3">API Keys (BYOK)</h3>
                <p className="text-sm text-gray-500">Coming soon — bring your own API keys to reduce costs.</p>
              </div>
              <div className="border-t border-white/[0.06] pt-6">
                <h3 className="text-sm font-medium text-gray-400 uppercase tracking-widest mb-3">Billing</h3>
                <p className="text-sm text-gray-500">Coming soon — usage tracking and invoices.</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
