"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import "katex/dist/katex.min.css";
import { InlineMath } from "react-katex";
import { useAuth } from "@/lib/auth";
import { getSupabase } from "@/lib/supabase";
import { useTheme } from "@/lib/theme-context";
import { OrbitalLogo } from "@/components/OrbitalLogo";
import { PricingModal } from "@/components/PricingModal";

type JobStatus = "idle" | "parsing" | "verifying" | "generating" | "complete" | "error";

const VOICES = [
  { id: "clayton", name: "Clayton", desc: "Warm & clear", avatar: "🎓" },
  { id: "professor", name: "Professor", desc: "Deep & authoritative", avatar: "👨‍🏫" },
  { id: "alex", name: "Alex", desc: "Friendly & casual", avatar: "😊" },
  { id: "sarah", name: "Sarah", desc: "Bright & engaging", avatar: "👩‍🔬" },
];

type VideoItem = {
  id: string;
  problem: string;
  problemType: "latex" | "text";
  createdAt: string;
  expiresAt: string;
  minutesUsed: number;
  status: string;
  thumbnailUrl: string | null;
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
  play: (
    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.91 11.672a.375.375 0 010 .656l-5.603 3.113a.375.375 0 01-.557-.328V8.887c0-.286.307-.466.557-.327l5.603 3.112z" />
    </svg>
  ),
  plus: (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
    </svg>
  ),
  sparkles: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
    </svg>
  ),
  clock: (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  user: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
  ),
  arrowRight: (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
    </svg>
  ),
  chevronRight: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
    </svg>
  ),
  microphone: (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
    </svg>
  ),
  check: (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
    </svg>
  ),
};

function timeAgo(dateString: string) {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function timeUntilExpiry(expiresAt: string) {
  const expiry = new Date(expiresAt);
  const now = new Date();
  const diffMs = expiry.getTime() - now.getTime();
  
  if (diffMs <= 0) return { text: "Expired", urgent: true };
  
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffHours / 24);
  
  if (diffHours < 24) return { text: `${diffHours}h left`, urgent: true };
  if (diffDays < 3) return { text: `${diffDays}d left`, urgent: true };
  return { text: `${diffDays}d left`, urgent: false };
}

function truncateText(text: string, maxLength: number = 50) {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).trim() + "...";
}

export default function DashboardClient() {
  const { theme, toggleTheme, isDark, accent } = useTheme();
  const [problem, setProblem] = useState("");
  const [status, setStatus] = useState<JobStatus>("idle");
  const [estimatedMinutes, setEstimatedMinutes] = useState<number | null>(null);
  const [selectedVoice, setSelectedVoice] = useState(VOICES[0].id);
  const [showVoiceSelector, setShowVoiceSelector] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [_loadingVideos, setLoadingVideos] = useState(true);
  const [showPricingModal, setShowPricingModal] = useState(false);

  const _router = useRouter();
  const { user, profile, loading: authLoading, signOut } = useAuth();
  const supabase = getSupabase();

  useEffect(() => {
    const handlePageShow = (e: PageTransitionEvent) => {
      if (e.persisted) {
        window.location.href = window.location.pathname + window.location.search;
      }
    };
    window.addEventListener("pageshow", handlePageShow);
    return () => window.removeEventListener("pageshow", handlePageShow);
  }, []);

  useEffect(() => {
    const storedVoice = localStorage.getItem("orbital-default-voice");
    if (storedVoice) setSelectedVoice(storedVoice);
  }, []);

  useEffect(() => {
    async function fetchVideos() {
      if (!user) return;
      
      try {
        const { data } = await supabase
          .from('videos')
          .select('*')
          .eq('user_id', user.id)
          .order('created_at', { ascending: false })
          .limit(10);

        if (data && data.length > 0) {
          interface SupabaseVideo {
            id: string;
            problem: string;
            problem_type?: string;
            created_at: string;
            expires_at: string;
            minutes_used: number;
            status: string;
            thumbnail_url: string | null;
          }
          setVideos(data.map((v: SupabaseVideo) => ({
            id: v.id,
            problem: v.problem,
            problemType: (v.problem_type || 'latex') as 'latex' | 'text',
            createdAt: v.created_at,
            expiresAt: v.expires_at,
            minutesUsed: v.minutes_used,
            status: v.status,
            thumbnailUrl: v.thumbnail_url,
          })));
        }
      } catch (err) {
        console.error('Error fetching videos:', err);
      } finally {
        setLoadingVideos(false);
      }
    }

    if (user) {
      fetchVideos();
    }
  }, [user, supabase]);

  useEffect(() => {
    const handleClickOutside = () => {
      setShowVoiceSelector(false);
      setShowUserMenu(false);
    };
    if (showVoiceSelector || showUserMenu) {
      document.addEventListener("click", handleClickOutside);
      return () => document.removeEventListener("click", handleClickOutside);
    }
  }, [showVoiceSelector, showUserMenu]);

  const handleSignOut = async () => {
    await signOut();
    window.location.href = '/';
  };

  const handleSolve = () => {
    if (!problem.trim()) return;
    setStatus("parsing");
    setEstimatedMinutes(2.5);
    setTimeout(() => setStatus("idle"), 2000);
  };

  if (authLoading) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-themed">
        <div 
          className="w-8 h-8 border-2 border-t-transparent rounded-full animate-spin"
          style={{ borderColor: accent.main, borderTopColor: 'transparent' }}
        />
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-themed">
        <div 
          className="w-8 h-8 border-2 border-t-transparent rounded-full animate-spin"
          style={{ borderColor: accent.main, borderTopColor: 'transparent' }}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full transition-colors duration-300 bg-themed text-themed-primary">
      {/* Header */}
      <header className={`sticky top-0 z-50 border-b backdrop-blur-xl ${isDark ? "bg-black/80 border-white/10" : "bg-white/80 border-gray-200"}`}>
        <div className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <OrbitalLogo className="w-8 h-8" />
            <span className="font-semibold text-lg">Orbital</span>
          </Link>

          <div className="flex items-center gap-3">
            {/* Minutes Balance */}
            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full ${isDark ? "bg-white/10" : "bg-gray-100"}`}>
              <div 
                className="w-2 h-2 rounded-full glow-accent"
                style={{ background: accent.main }}
              />
              <span className="font-semibold">{profile?.minutes_balance ?? 0}</span>
              <span className="text-sm text-themed-secondary">min</span>
            </div>

            {/* Buy More Button */}
            <button
              onClick={() => setShowPricingModal(true)}
              className="flex items-center gap-1 px-3 py-1.5 rounded-full text-sm font-medium text-white transition-all btn-glow"
              style={{ background: accent.main }}
            >
              {Icons.plus}
              <span className="hidden sm:inline">Buy More</span>
            </button>

            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className={`p-2 rounded-lg transition-colors ${isDark ? "hover:bg-white/10 text-gray-400 hover:text-white" : "hover:bg-gray-100 text-gray-500 hover:text-gray-900"}`}
            >
              {isDark ? Icons.sun : Icons.moon}
            </button>

            {/* User Menu */}
            <div className="relative">
              <button
                onClick={(e) => { e.stopPropagation(); setShowUserMenu(!showUserMenu); }}
                className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors ${isDark ? "bg-white/10 hover:bg-white/15" : "bg-gray-200 hover:bg-gray-300"}`}
              >
                {Icons.user}
              </button>

              {showUserMenu && (
                <div
                  onClick={(e) => e.stopPropagation()}
                  className={`absolute right-0 top-full mt-2 w-64 rounded-xl shadow-xl border overflow-hidden z-50 ${isDark ? "bg-zinc-900 border-white/10" : "bg-white border-gray-200"}`}
                >
                  <div className={`px-4 py-3 border-b ${isDark ? "border-white/10" : "border-gray-100"}`}>
                    <p className="font-medium truncate">{user?.email}</p>
                    <p className="text-sm text-themed-secondary">
                      {profile?.minutes_balance ?? 0} minutes remaining
                    </p>
                  </div>

                  <div className="py-1">
                    <Link href="/settings" className={`w-full flex items-center gap-3 px-4 py-2.5 text-left text-sm transition-colors ${isDark ? "hover:bg-white/5 text-gray-300" : "hover:bg-gray-50 text-gray-700"}`}>
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      Settings
                    </Link>
                    <Link href="/purchases" className={`w-full flex items-center gap-3 px-4 py-2.5 text-left text-sm transition-colors ${isDark ? "hover:bg-white/5 text-gray-300" : "hover:bg-gray-50 text-gray-700"}`}>
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
                      </svg>
                      Purchase History
                    </Link>
                  </div>

                  <div className={`border-t ${isDark ? "border-white/10" : "border-gray-100"}`}>
                    <button
                      onClick={handleSignOut}
                      className={`w-full flex items-center gap-3 px-4 py-2.5 text-left text-sm transition-colors ${isDark ? "hover:bg-white/5 text-red-400" : "hover:bg-gray-50 text-red-600"}`}
                    >
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                      </svg>
                      Sign Out
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-6 py-8">
        {/* Solver Section */}
        <div className="mb-10">
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold mb-2">What would you like to solve?</h1>
            <p className="text-themed-secondary">
              Type any math problem and get a step-by-step video
            </p>
          </div>

          {/* Input Card with Glow */}
          <div 
            className={`relative rounded-2xl transition-all duration-300 input-glow ${isDark ? "bg-white/5 border border-white/10" : "bg-white border border-gray-200"}`}
            style={{ 
              borderColor: problem.trim() ? `rgba(${accent.rgb}, 0.3)` : undefined 
            }}
          >
            <textarea
              value={problem}
              onChange={(e) => setProblem(e.target.value)}
              placeholder="e.g., integrate x^2 sin(x) dx"
              rows={3}
              className={`w-full px-5 py-4 bg-transparent resize-none focus:outline-none text-lg ${isDark ? "text-white placeholder-gray-500" : "text-gray-900 placeholder-gray-400"}`}
            />
            
            <div className={`flex items-center justify-between px-5 py-3 border-t ${isDark ? "border-white/10 bg-white/[0.02]" : "border-gray-100 bg-gray-50"}`}>
              <div className="flex items-center gap-4">
                {/* Voice Selector */}
                <div className="relative">
                  <button
                    onClick={(e) => { e.stopPropagation(); setShowVoiceSelector(!showVoiceSelector); }}
                    className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm transition-colors ${isDark ? "bg-white/5 hover:bg-white/10 text-gray-300" : "bg-gray-100 hover:bg-gray-200 text-gray-700"}`}
                  >
                    <span>{VOICES.find(v => v.id === selectedVoice)?.avatar}</span>
                    <span>{VOICES.find(v => v.id === selectedVoice)?.name}</span>
                    {Icons.microphone}
                  </button>

                  {showVoiceSelector && (
                    <div
                      onClick={(e) => e.stopPropagation()}
                      className={`absolute bottom-full left-0 mb-2 w-56 rounded-xl shadow-xl border overflow-hidden z-50 ${isDark ? "bg-zinc-900 border-white/10" : "bg-white border-gray-200"}`}
                    >
                      <div className="px-3 py-2 text-xs font-medium text-themed-muted">
                        Choose a voice
                      </div>
                      {VOICES.map((voice) => (
                        <button
                          key={voice.id}
                          onClick={() => { setSelectedVoice(voice.id); setShowVoiceSelector(false); }}
                          className={`w-full flex items-center gap-3 px-3 py-2.5 text-left transition-colors ${
                            selectedVoice === voice.id 
                              ? `text-white` 
                              : isDark ? "hover:bg-white/5 text-gray-300" : "hover:bg-gray-50 text-gray-700"
                          }`}
                          style={selectedVoice === voice.id ? { background: `${accent.main}30` } : undefined}
                        >
                          <span className="text-xl">{voice.avatar}</span>
                          <div className="flex-1">
                            <p className="font-medium text-sm">{voice.name}</p>
                            <p className="text-xs text-themed-muted">{voice.desc}</p>
                          </div>
                          {selectedVoice === voice.id && <span style={{ color: accent.main }}>{Icons.check}</span>}
                        </button>
                      ))}
                    </div>
                  )}
                </div>

                {/* Estimated time */}
                <div className="text-sm text-themed-muted">
                  {estimatedMinutes && (
                    <span className="flex items-center gap-1">
                      {Icons.clock}
                      ~{estimatedMinutes} min
                    </span>
                  )}
                </div>
              </div>

              {/* Solve Button */}
              <button
                onClick={handleSolve}
                disabled={!problem.trim() || status !== "idle"}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium transition-all ${
                  problem.trim() && status === "idle" 
                    ? "text-white btn-glow" 
                    : isDark ? "bg-white/10 text-gray-500 cursor-not-allowed" : "bg-gray-200 text-gray-400 cursor-not-allowed"
                }`}
                style={problem.trim() && status === "idle" ? { 
                  background: accent.main,
                  boxShadow: `0 4px 20px rgba(${accent.rgb}, 0.35)`
                } : undefined}
              >
                {status === "parsing" ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Parsing...
                  </>
                ) : (
                  <>
                    {Icons.sparkles}
                    Solve
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Recent Videos */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Recent Videos</h2>
            <Link href="/videos" className="flex items-center gap-1 text-sm font-medium transition-colors text-themed-secondary hover:text-themed-primary">
              See All
              {Icons.chevronRight}
            </Link>
          </div>

          {videos.length === 0 ? (
            <div className={`rounded-xl p-8 text-center card-glow ${isDark ? "bg-white/5 border border-white/10" : "bg-gray-50 border border-gray-200"}`}>
              <div className={`w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center ${isDark ? "bg-white/10" : "bg-gray-200"}`}>
                {Icons.play}
              </div>
              <h3 className="font-medium mb-2">No videos yet</h3>
              <p className="text-sm text-themed-secondary mb-4">
                Solve your first problem to create a video
              </p>
            </div>
          ) : (
            <div className="flex gap-4 overflow-x-auto pb-4 -mx-6 px-6 scrollbar-hide">
              {videos.map((video) => (
                <div
                  key={video.id}
                  className={`flex-shrink-0 w-64 rounded-xl overflow-hidden transition-all hover:scale-[1.02] cursor-pointer group card-glow ${isDark ? "bg-white/5 border border-white/10" : "bg-white border border-gray-200 hover:shadow-lg"}`}
                >
                  <div className={`relative h-36 flex items-center justify-center overflow-hidden ${isDark ? "bg-white/[0.03]" : "bg-gray-50"}`}>
                    {video.thumbnailUrl && (
                      <img src={video.thumbnailUrl} alt="Video thumbnail" className="absolute inset-0 w-full h-full object-cover" />
                    )}
                    <div 
                      className="relative z-10 w-14 h-14 rounded-full flex items-center justify-center transition-all group-hover:scale-110 text-white"
                      style={{ 
                        background: `${accent.main}cc`,
                        boxShadow: `0 4px 20px rgba(${accent.rgb}, 0.4)`
                      }}
                    >
                      {Icons.play}
                    </div>
                    <div className={`absolute bottom-2 right-2 z-10 px-2 py-0.5 rounded text-xs font-medium ${isDark ? "bg-black/60 text-white" : "bg-black/70 text-white"}`}>
                      {video.minutesUsed} min
                    </div>
                  </div>
                  <div className="p-4">
                    <div className="font-medium mb-1 overflow-hidden min-h-[1.75rem]">
                      {video.problemType === "latex" ? (
                        <InlineMath math={video.problem} />
                      ) : (
                        <span className="text-sm leading-tight line-clamp-2">{truncateText(video.problem, 60)}</span>
                      )}
                    </div>
                    <div className="flex items-center justify-between">
                      <p className="text-sm text-themed-muted">{timeAgo(video.createdAt)}</p>
                      {(() => {
                        const expiry = timeUntilExpiry(video.expiresAt);
                        return (
                          <span className={`text-xs px-1.5 py-0.5 rounded ${expiry.urgent ? "bg-amber-500/20 text-amber-400" : (isDark ? "bg-white/10 text-gray-400" : "bg-gray-100 text-gray-500")}`}>
                            {expiry.text}
                          </span>
                        );
                      })()}
                    </div>
                  </div>
                </div>
              ))}

              {/* View All Card */}
              <Link
                href="/videos"
                className={`flex-shrink-0 w-64 h-[13.5rem] rounded-xl flex flex-col items-center justify-center transition-all cursor-pointer ${isDark ? "bg-white/[0.02] border border-dashed border-white/10 hover:border-white/20" : "bg-gray-50 border border-dashed border-gray-200 hover:border-gray-300"}`}
              >
                <div className={`w-12 h-12 rounded-full flex items-center justify-center mb-3 ${isDark ? "bg-white/10" : "bg-gray-200"}`}>
                  {Icons.arrowRight}
                </div>
                <span className="text-sm font-medium text-themed-secondary">View All Videos</span>
              </Link>
            </div>
          )}
        </div>

        {/* Quick Stats */}
        <div className="mt-8 grid grid-cols-3 gap-4">
          <div className={`rounded-xl p-4 text-center card-glow ${isDark ? "bg-white/5 border border-white/10" : "bg-white border border-gray-200"}`}>
            <p className="text-3xl font-bold" style={{ color: accent.main }}>{videos.length}</p>
            <p className="text-sm text-themed-secondary">Videos Created</p>
          </div>
          <div className={`rounded-xl p-4 text-center card-glow ${isDark ? "bg-white/5 border border-white/10" : "bg-white border border-gray-200"}`}>
            <p className="text-3xl font-bold" style={{ color: accent.main }}>{videos.reduce((acc, v) => acc + v.minutesUsed, 0).toFixed(1)}</p>
            <p className="text-sm text-themed-secondary">Minutes Used</p>
          </div>
          <div className={`rounded-xl p-4 text-center card-glow ${isDark ? "bg-white/5 border border-white/10" : "bg-white border border-gray-200"}`}>
            <p className="text-3xl font-bold" style={{ color: accent.main }}>{profile?.minutes_balance ?? 0}</p>
            <p className="text-sm text-themed-secondary">Minutes Left</p>
          </div>
        </div>
      </main>

      <PricingModal isOpen={showPricingModal} onClose={() => setShowPricingModal(false)} isDark={isDark} />
    </div>
  );
}
