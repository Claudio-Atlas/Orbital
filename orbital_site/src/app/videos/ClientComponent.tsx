"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import "katex/dist/katex.min.css";
import { InlineMath } from "react-katex";
import { useAuth } from "@/lib/auth";
import { getSupabase } from "@/lib/supabase";
import { OrbitalLogo } from "@/components/OrbitalLogo";

type Theme = "dark" | "light";

// Mock videos for now — will be replaced with Supabase queries
const MOCK_VIDEOS = [
  {
    id: "v1",
    problem: "\\int x \\cdot e^{x^2} \\, dx",
    problemType: "latex" as const,
    createdAt: "2026-02-11T10:30:00Z",
    expiresAt: "2026-02-14T10:30:00Z",
    minutesUsed: 2.5,
    status: "complete",
    thumbnailUrl: null,
  },
  {
    id: "v2", 
    problem: "\\lim_{x \\to 0} \\frac{\\sin x}{x}",
    problemType: "latex" as const,
    createdAt: "2026-02-11T08:00:00Z",
    expiresAt: "2026-02-14T08:00:00Z",
    minutesUsed: 1.8,
    status: "complete",
    thumbnailUrl: null,
  },
  {
    id: "v3",
    problem: "\\frac{d}{dx} \\left[ \\ln(x^2 + 1) \\right]",
    problemType: "latex" as const,
    createdAt: "2026-02-10T14:00:00Z",
    expiresAt: "2026-02-13T14:00:00Z",
    minutesUsed: 2.1,
    status: "complete",
    thumbnailUrl: null,
  },
  {
    id: "v4",
    problem: "Find the derivative of f(x) = 3x^4 - 2x^2 + 5",
    problemType: "text" as const,
    createdAt: "2026-02-09T09:00:00Z",
    expiresAt: "2026-02-12T09:00:00Z",
    minutesUsed: 1.5,
    status: "complete",
    thumbnailUrl: null,
  },
];

const Icons = {
  back: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
    </svg>
  ),
  play: (
    <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
      <path d="M8 5v14l11-7z" />
    </svg>
  ),
  clock: (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
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
};

export default function ClientComponent() {
  const [theme, setTheme] = useState<Theme>("dark");
  const [videos, setVideos] = useState(MOCK_VIDEOS);
  
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();

  useEffect(() => {
    const saved = localStorage.getItem("orbital-theme") as Theme;
    if (saved) setTheme(saved);
  }, []);

  // Redirect if not logged in
  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [user, authLoading, router]);

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    localStorage.setItem("orbital-theme", newTheme);
  };

  const isDark = theme === "dark";

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const getTimeUntilExpiry = (expiresAt: string) => {
    const now = new Date();
    const expiry = new Date(expiresAt);
    const hoursLeft = Math.max(0, Math.floor((expiry.getTime() - now.getTime()) / (1000 * 60 * 60)));
    
    if (hoursLeft > 24) {
      const days = Math.floor(hoursLeft / 24);
      return `${days}d left`;
    }
    return `${hoursLeft}h left`;
  };

  if (authLoading) {
    return (
      <div className={`min-h-screen flex items-center justify-center ${isDark ? "bg-black" : "bg-white"}`}>
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-violet-500" />
      </div>
    );
  }

  return (
    <div className={`min-h-screen transition-colors duration-300 ${
      isDark ? "bg-black text-white" : "bg-gray-50 text-gray-900"
    }`}>
      {/* Header */}
      <header className={`sticky top-0 z-40 backdrop-blur-xl border-b ${
        isDark ? "bg-black/80 border-white/10" : "bg-white/80 border-gray-200"
      }`}>
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link 
              href="/dashboard"
              className={`p-2 rounded-lg transition-colors ${
                isDark ? "hover:bg-white/10" : "hover:bg-gray-100"
              }`}
            >
              {Icons.back}
            </Link>
            <Link href="/dashboard" className="flex items-center gap-2">
              <OrbitalLogo className="h-7 w-7" />
              <span className="text-lg font-semibold">Orbital</span>
            </Link>
          </div>

          <button
            onClick={toggleTheme}
            className={`p-2.5 rounded-xl transition-colors ${
              isDark ? "hover:bg-white/10" : "hover:bg-gray-100"
            }`}
          >
            {isDark ? Icons.sun : Icons.moon}
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold mb-2">All Videos</h1>
          <p className={`${isDark ? "text-gray-400" : "text-gray-600"}`}>
            {videos.length} video{videos.length !== 1 ? "s" : ""} • Videos auto-delete after 3 days
          </p>
        </div>

        {/* Videos Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {videos.map((video) => (
            <div
              key={video.id}
              className={`rounded-2xl overflow-hidden transition-all hover:scale-[1.02] cursor-pointer group ${
                isDark ? "bg-white/5 hover:bg-white/10" : "bg-white hover:shadow-lg"
              }`}
            >
              {/* Thumbnail */}
              <div className={`aspect-video relative ${
                isDark ? "bg-gradient-to-br from-violet-600/20 to-fuchsia-600/20" : "bg-gradient-to-br from-violet-100 to-fuchsia-100"
              }`}>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className={`w-14 h-14 rounded-full flex items-center justify-center transition-transform group-hover:scale-110 ${
                    isDark ? "bg-white/20" : "bg-black/10"
                  }`}>
                    {Icons.play}
                  </div>
                </div>
                
                {/* Expiry badge */}
                <div className={`absolute top-3 right-3 px-2 py-1 rounded-lg text-xs font-medium flex items-center gap-1 ${
                  isDark ? "bg-black/60 text-gray-300" : "bg-white/90 text-gray-600"
                }`}>
                  {Icons.clock}
                  {getTimeUntilExpiry(video.expiresAt)}
                </div>
              </div>

              {/* Info */}
              <div className="p-4">
                <div className={`text-sm mb-2 line-clamp-2 min-h-[2.5rem] ${
                  isDark ? "text-gray-200" : "text-gray-800"
                }`}>
                  {video.problemType === "latex" ? (
                    <InlineMath math={video.problem} />
                  ) : (
                    video.problem
                  )}
                </div>
                
                <div className={`flex items-center justify-between text-xs ${
                  isDark ? "text-gray-500" : "text-gray-400"
                }`}>
                  <span>{formatDate(video.createdAt)}</span>
                  <span>{video.minutesUsed} min</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {videos.length === 0 && (
          <div className={`text-center py-16 ${isDark ? "text-gray-500" : "text-gray-400"}`}>
            <p className="text-lg mb-2">No videos yet</p>
            <p className="text-sm">Solve a problem to create your first video!</p>
            <Link
              href="/dashboard"
              className="inline-block mt-4 px-6 py-2 bg-violet-600 text-white rounded-xl hover:bg-violet-500 transition-colors"
            >
              Go to Solver
            </Link>
          </div>
        )}
      </main>
    </div>
  );
}
