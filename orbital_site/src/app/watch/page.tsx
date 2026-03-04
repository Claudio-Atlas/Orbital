"use client";

import { useState, useEffect } from "react";
import { OrbitalLogo } from "@/components/OrbitalLogo";

type Theme = "dark" | "light";
type VideoFormat = "shorts" | "tutorials";

interface Video {
  id: string;
  title: string;
  youtubeId: string;
  format: "short" | "tutorial";
  duration: string;
  description: string;
  playlist?: string;
}

const VIDEOS: Video[] = [
  // Shorts — Derivatives from Scratch playlist
  {
    id: "s1",
    title: "Why The Derivative of a Constant is ZERO",
    youtubeId: "", // Add YouTube ID after upload
    format: "short",
    duration: "0:59",
    description: "The Constant Rule explained visually",
    playlist: "Derivatives from Scratch",
  },
  {
    id: "s2",
    title: "The ONE Rule That Handles Every Power of x",
    youtubeId: "",
    format: "short",
    duration: "1:06",
    description: "The Power Rule — the most important derivative rule",
    playlist: "Derivatives from Scratch",
  },
  {
    id: "s3",
    title: "Negative Exponents? The Power Rule Still Works",
    youtubeId: "",
    format: "short",
    duration: "1:59",
    description: "Power Rule with negative exponents and fractions",
    playlist: "Derivatives from Scratch",
  },
  {
    id: "s4",
    title: "Find the Derivative of 3x² + 2x - 5",
    youtubeId: "",
    format: "short",
    duration: "1:43",
    description: "Full derivative problem — step by step",
    playlist: "Derivatives from Scratch",
  },

  // Tutorials (long-form)
  {
    id: "t1",
    title: "Group of Order 15 is Cyclic — Full Proof",
    youtubeId: "",
    format: "tutorial",
    duration: "5:30",
    description: "Complete proof using Sylow theorems",
  },
  {
    id: "t2",
    title: "Uncountability of the Reals — Dedekind Cuts",
    youtubeId: "",
    format: "tutorial",
    duration: "4:45",
    description: "Why the real numbers are uncountable",
  },
];

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
    <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 24 24">
      <path d="M8 5v14l11-7z" />
    </svg>
  ),
};

export default function WatchPage() {
  const [theme, setTheme] = useState<Theme>("dark");
  const [activeTab, setActiveTab] = useState<VideoFormat>("shorts");

  useEffect(() => {
    const saved = localStorage.getItem("orbital-theme") as Theme;
    if (saved) setTheme(saved);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    localStorage.setItem("orbital-theme", newTheme);
  };

  const isDark = theme === "dark";
  const filtered = VIDEOS.filter((v) =>
    activeTab === "shorts" ? v.format === "short" : v.format === "tutorial"
  );

  // Group shorts by playlist
  const playlists = filtered.reduce((acc, v) => {
    const key = v.playlist || "Other";
    if (!acc[key]) acc[key] = [];
    acc[key].push(v);
    return acc;
  }, {} as Record<string, Video[]>);

  return (
    <div
      className={`min-h-screen transition-colors duration-300 ${
        isDark ? "bg-black text-white" : "bg-gray-50 text-gray-900"
      }`}
    >
      {/* Header */}
      <header
        className={`fixed top-0 left-0 right-0 z-50 backdrop-blur-xl border-b ${
          isDark ? "bg-black/80 border-white/10" : "bg-white/80 border-gray-200"
        }`}
      >
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <a href="/" className="flex items-center gap-2">
            <OrbitalLogo className="w-8 h-8" />
            <span className="font-semibold text-lg">Orbital</span>
          </a>
          <div className="flex items-center gap-3">
            <button
              onClick={toggleTheme}
              className={`p-2 rounded-lg transition-colors ${
                isDark
                  ? "hover:bg-white/10 text-gray-400 hover:text-white"
                  : "hover:bg-gray-100 text-gray-500 hover:text-gray-900"
              }`}
            >
              {isDark ? Icons.sun : Icons.moon}
            </button>
            <a
              href="/#waitlist"
              className="px-4 py-2 text-sm font-medium rounded-lg bg-cyan-500 text-black hover:bg-cyan-400 transition-colors"
            >
              Get Notified
            </a>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-6xl mx-auto px-6 pt-28 pb-20">
        <div className="text-center mb-12">
          <h1 className="text-3xl sm:text-4xl font-semibold mb-4">Videos</h1>
          <p className={`text-lg ${isDark ? "text-gray-500" : "text-gray-600"}`}>
            AI-generated math walkthroughs — every step explained
          </p>
        </div>

        {/* Toggle */}
        <div className="flex justify-center mb-12">
          <div
            className={`inline-flex rounded-xl p-1 ${
              isDark ? "bg-white/[0.05] border border-white/[0.08]" : "bg-gray-200"
            }`}
          >
            <button
              onClick={() => setActiveTab("shorts")}
              className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === "shorts"
                  ? isDark
                    ? "bg-cyan-500 text-black"
                    : "bg-white text-gray-900 shadow-sm"
                  : isDark
                  ? "text-gray-400 hover:text-white"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              Shorts
            </button>
            <button
              onClick={() => setActiveTab("tutorials")}
              className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === "tutorials"
                  ? isDark
                    ? "bg-cyan-500 text-black"
                    : "bg-white text-gray-900 shadow-sm"
                  : isDark
                  ? "text-gray-400 hover:text-white"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              Tutorials
            </button>
          </div>
        </div>

        {/* Videos */}
        {activeTab === "shorts" ? (
          // Shorts — grouped by playlist
          Object.entries(playlists).map(([playlist, vids]) => (
            <div key={playlist} className="mb-16">
              <h2 className="text-xl font-semibold mb-6">{playlist}</h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                {vids.map((v) => (
                  <VideoCard key={v.id} video={v} isDark={isDark} isShort />
                ))}
              </div>
            </div>
          ))
        ) : (
          // Tutorials — flat grid
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filtered.map((v) => (
              <VideoCard key={v.id} video={v} isDark={isDark} />
            ))}
          </div>
        )}

        {filtered.length === 0 && (
          <div className="text-center py-16">
            <p className={`text-lg ${isDark ? "text-gray-500" : "text-gray-600"}`}>
              More videos coming soon!
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer
        className={`w-full py-12 border-t ${isDark ? "border-white/[0.05]" : "border-gray-200"}`}
      >
        <div className="max-w-4xl mx-auto px-6 text-center">
          <p className={isDark ? "text-gray-600" : "text-gray-500"}>
            © 2026 Orbital. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

function VideoCard({
  video,
  isDark,
  isShort,
}: {
  video: Video;
  isDark: boolean;
  isShort?: boolean;
}) {
  const hasYouTube = video.youtubeId && video.youtubeId.length > 0;
  const embedUrl = hasYouTube
    ? `https://www.youtube.com/embed/${video.youtubeId}`
    : null;

  return (
    <div
      className={`rounded-2xl overflow-hidden transition-all hover:scale-[1.02] ${
        isDark ? "bg-white/[0.03] border border-white/[0.06]" : "bg-white border border-gray-200 shadow-sm"
      }`}
    >
      {/* Embed or placeholder */}
      <div className={`relative ${isShort ? "aspect-[9/16]" : "aspect-video"}`}>
        {embedUrl ? (
          <iframe
            src={embedUrl}
            className="absolute inset-0 w-full h-full"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        ) : (
          <div
            className={`absolute inset-0 flex flex-col items-center justify-center ${
              isDark
                ? "bg-gradient-to-br from-cyan-900/20 to-violet-900/20"
                : "bg-gradient-to-br from-cyan-100 to-violet-100"
            }`}
          >
            <div className={`w-12 h-12 rounded-full flex items-center justify-center mb-3 ${
              isDark ? "bg-cyan-500/20 text-cyan-400" : "bg-cyan-100 text-cyan-600"
            }`}>
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
            </div>
            <span className={`text-xs ${isDark ? "text-gray-500" : "text-gray-400"}`}>
              Coming soon
            </span>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="p-3">
        <h3 className="text-sm font-medium line-clamp-2 mb-1">{video.title}</h3>
        <div className="flex items-center justify-between">
          <span className={`text-xs ${isDark ? "text-gray-500" : "text-gray-400"}`}>
            {video.description}
          </span>
          <span className={`text-xs ${isDark ? "text-gray-600" : "text-gray-400"}`}>
            {video.duration}
          </span>
        </div>
      </div>
    </div>
  );
}
