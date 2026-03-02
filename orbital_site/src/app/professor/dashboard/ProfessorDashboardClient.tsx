"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { useTheme } from "@/lib/theme-context";
import { OrbitalLogo } from "@/components/OrbitalLogo";

type DetailLevel = "quick" | "standard" | "detailed";
type JobStatus = "idle" | "generating" | "circle" | "rendering" | "complete" | "error";

type VideoItem = {
  id: string;
  problem: string;
  detailLevel: DetailLevel;
  status: JobStatus;
  createdAt: string;
  duration: number | null;
  videoUrl: string | null;
};

const Icons = {
  sun: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
    </svg>
  ),
  moon: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
    </svg>
  ),
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
  circle: { label: "Verifying math...", color: "text-cyan-400" },
  rendering: { label: "Rendering video...", color: "text-amber-400" },
  complete: { label: "Complete", color: "text-green-400" },
  error: { label: "Error", color: "text-red-400" },
};

export default function ProfessorDashboardClient() {
  const { user, profile, loading, signOut } = useAuth();
  const router = useRouter();

  const [problem, setProblem] = useState("");
  const [detailLevel, setDetailLevel] = useState<DetailLevel>("standard");
  const [showNotes, setShowNotes] = useState(false);
  const [notes, setNotes] = useState("");
  const [jobStatus, setJobStatus] = useState<JobStatus>("idle");
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [activeTab, setActiveTab] = useState<"dashboard" | "library" | "settings">("dashboard");

  const isDark = true; // Professor portal is always dark for now

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [loading, user, router]);

  const handleGenerate = async () => {
    if (!problem.trim()) return;

    // Mock pipeline stages
    setJobStatus("generating");
    console.log("[Orbital] Generating video:", { problem, detailLevel, notes });

    // Simulate pipeline progress
    setTimeout(() => setJobStatus("circle"), 2000);
    setTimeout(() => setJobStatus("rendering"), 5000);
    setTimeout(() => {
      setJobStatus("complete");
      const newVideo: VideoItem = {
        id: crypto.randomUUID(),
        problem: problem.trim(),
        detailLevel,
        status: "complete",
        createdAt: new Date().toISOString(),
        duration: detailLevel === "quick" ? 90 : detailLevel === "standard" ? 210 : 360,
        videoUrl: null,
      };
      setVideos((prev) => [newVideo, ...prev]);
      setProblem("");
      setNotes("");
    }, 8000);
  };

  const handleSignOut = async () => {
    await signOut();
    router.push("/");
  };

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
                  onClick={() => setActiveTab(tab.key)}
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
        {activeTab === "dashboard" && (
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
                        <span className={`font-medium ${
                          detailLevel === level.value ? "text-violet-300" : "text-white"
                        }`}>
                          {level.label}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500">{level.desc}</p>
                    </button>
                  ))}
                </div>
              </div>

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
                  disabled={!problem.trim() || (jobStatus !== "idle" && jobStatus !== "complete" && jobStatus !== "error")}
                  className="flex items-center gap-2 px-8 py-4 rounded-xl bg-violet-600 hover:bg-violet-500 text-white font-semibold transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  {Icons.sparkles}
                  Generate Video
                </button>
                {jobStatus !== "idle" && (
                  <div className="flex items-center gap-3">
                    {jobStatus !== "complete" && jobStatus !== "error" && (
                      <div className="w-5 h-5 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
                    )}
                    {jobStatus === "complete" && (
                      <span className="text-green-400">✓</span>
                    )}
                    <span className={`text-sm ${STATUS_LABELS[jobStatus].color}`}>
                      {STATUS_LABELS[jobStatus].label}
                    </span>
                  </div>
                )}
              </div>

              {/* Cost Estimate */}
              <div className="mt-4 flex items-center gap-2 text-xs text-gray-600">
                <span>Estimated cost:</span>
                <span className="text-gray-400">
                  {detailLevel === "quick" ? "~$0.35" : detailLevel === "standard" ? "~$0.55" : "~$0.75"}
                </span>
                <span>•</span>
                <span>
                  {detailLevel === "quick" ? "~90s video" : detailLevel === "standard" ? "~3-4 min video" : "~6+ min video"}
                </span>
              </div>
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
                      {/* Thumbnail placeholder */}
                      <div className="aspect-video bg-white/[0.04] rounded-lg mb-4 flex items-center justify-center text-gray-600">
                        {Icons.play}
                      </div>
                      <p className="text-sm text-white font-medium mb-2 line-clamp-2">{video.problem}</p>
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>{new Date(video.createdAt).toLocaleDateString()}</span>
                        <span className={STATUS_LABELS[video.status].color}>
                          {STATUS_LABELS[video.status].label}
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
                    <div className="flex items-center gap-2 text-xs text-gray-500">
                      <span className="capitalize">{video.detailLevel}</span>
                      <span>•</span>
                      <span>{new Date(video.createdAt).toLocaleDateString()}</span>
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
                <h3 className="text-sm font-medium text-gray-400 uppercase tracking-widest mb-3">Default Detail Level</h3>
                <p className="text-sm text-gray-500">Coming soon — set your preferred default for new videos.</p>
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
