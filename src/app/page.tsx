"use client";

import { useState, useRef, useEffect } from "react";
import { SITE, PRICING } from "@/lib/constants";

type JobStatus = "idle" | "parsing" | "generating" | "complete" | "error";
type Theme = "dark" | "light";

interface Job {
  job_id: string;
  status: string;
  problem?: string;
  steps?: Array<{ narration: string; latex: string }>;
  video_url?: string;
  error?: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8002";

// Clean SVG Icons
const Icons = {
  camera: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0z" />
    </svg>
  ),
  download: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
    </svg>
  ),
  edit: (
    <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125" />
    </svg>
  ),
  cpu: (
    <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5M4.5 15.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H6.75A2.25 2.25 0 004.5 6.75v10.5a2.25 2.25 0 002.25 2.25z" />
    </svg>
  ),
  play: (
    <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.91 11.672a.375.375 0 010 .656l-5.603 3.113a.375.375 0 01-.557-.328V8.887c0-.286.307-.466.557-.327l5.603 3.112z" />
    </svg>
  ),
  check: (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
    </svg>
  ),
  x: (
    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
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

export default function HomePage() {
  const [problem, setProblem] = useState("");
  const [status, setStatus] = useState<JobStatus>("idle");
  const [job, setJob] = useState<Job | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [theme, setTheme] = useState<Theme>("dark");
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Load theme from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem("orbital-theme") as Theme;
    if (saved) setTheme(saved);
  }, []);

  // Save theme to localStorage
  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    localStorage.setItem("orbital-theme", newTheme);
  };

  const isDark = theme === "dark";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!problem.trim()) return;

    setStatus("parsing");
    setError(null);
    setJob(null);

    try {
      const res = await fetch(`${API_URL}/solve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ problem: problem.trim() }),
      });

      if (!res.ok) throw new Error("Failed to submit problem");

      const data = await res.json();
      setJob(data);
      setStatus("generating");
      pollJob(data.job_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setStatus("error");
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setStatus("parsing");
    setError(null);
    setJob(null);

    try {
      const base64 = await fileToBase64(file);
      const res = await fetch(`${API_URL}/solve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64 }),
      });

      if (!res.ok) throw new Error("Failed to process image");

      const data = await res.json();
      setJob(data);
      setProblem(data.problem || "Problem from image");
      setStatus("generating");
      pollJob(data.job_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setStatus("error");
    }
  };

  const pollJob = async (jobId: string) => {
    const maxAttempts = 120;
    let attempts = 0;

    const poll = async () => {
      try {
        const res = await fetch(`${API_URL}/job/${jobId}`);
        const data: Job = await res.json();
        setJob(data);

        if (data.status === "complete") {
          setStatus("complete");
          return;
        }
        if (data.status === "failed") {
          setError(data.error || "Video generation failed");
          setStatus("error");
          return;
        }

        attempts++;
        if (attempts < maxAttempts) {
          setTimeout(poll, 1000);
        } else {
          setError("Timeout: Video generation took too long");
          setStatus("error");
        }
      } catch {
        setError("Failed to check job status");
        setStatus("error");
      }
    };
    poll();
  };

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        resolve(result.split(",")[1]);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  const reset = () => {
    setProblem("");
    setStatus("idle");
    setJob(null);
    setError(null);
  };

  return (
    <div className={`min-h-screen overflow-x-hidden w-full flex flex-col items-center transition-colors duration-300 ${
      isDark ? "bg-black text-white" : "bg-gray-50 text-gray-900"
    }`}>
      
      {/* Theme Toggle - Fixed position */}
      <button
        onClick={toggleTheme}
        className={`fixed top-6 right-6 z-50 p-3 rounded-full transition-all ${
          isDark 
            ? "bg-white/10 hover:bg-white/20 text-white" 
            : "bg-black/5 hover:bg-black/10 text-gray-700"
        }`}
        aria-label="Toggle theme"
      >
        {isDark ? Icons.sun : Icons.moon}
      </button>

      {/* Hero Section */}
      <section className="w-full pt-32 pb-24">
        <div className="w-full max-w-5xl mx-auto px-8 md:px-12">
          {/* Ambient glow */}
          <div className={`absolute top-20 left-1/2 -translate-x-1/2 w-[800px] h-[400px] rounded-full blur-3xl pointer-events-none ${
            isDark ? "bg-gradient-to-b from-violet-600/10 to-transparent" : "bg-gradient-to-b from-violet-400/20 to-transparent"
          }`} />
          
          <div className="relative text-center">
            <div className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-medium mb-10 ${
              isDark 
                ? "bg-white/[0.03] border border-white/[0.08] text-gray-400" 
                : "bg-violet-100 border border-violet-200 text-violet-600"
            }`}>
              <span className="w-1.5 h-1.5 rounded-full bg-violet-500" />
              <span>AI-Powered</span>
            </div>
            
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-semibold tracking-tight mb-8 leading-[1.1] max-w-4xl mx-auto">
              <span className={`bg-clip-text text-transparent ${
                isDark 
                  ? "bg-gradient-to-b from-white via-white to-gray-500" 
                  : "bg-gradient-to-b from-gray-900 via-gray-800 to-gray-500"
              }`}>
                {SITE.tagline}
              </span>
            </h1>
            
            <p className={`text-lg md:text-xl max-w-2xl mx-auto leading-relaxed ${
              isDark ? "text-gray-500" : "text-gray-600"
            }`}>
              {SITE.taglineSecondary}
            </p>
          </div>
        </div>
      </section>

      {/* Solver Interface */}
      <section className="w-full pb-32">
        <div className="w-full max-w-2xl mx-auto px-6">
          <div className={`rounded-[2rem] p-8 md:p-10 ${
            isDark 
              ? "bg-gradient-to-b from-white/[0.08] to-white/[0.02] border border-white/[0.08]" 
              : "bg-white border border-gray-200 shadow-xl shadow-gray-200/50"
          }`}>
            
            {status === "idle" && (
              <>
                <form onSubmit={handleSubmit}>
                  <label className={`block mb-4 text-xs font-medium uppercase tracking-widest text-center ${
                    isDark ? "text-gray-500" : "text-gray-500"
                  }`}>
                    Enter your math problem
                  </label>
                  
                  {/* Textarea with neon glow */}
                  <textarea
                    value={problem}
                    onChange={(e) => setProblem(e.target.value)}
                    placeholder="e.g., Find the derivative of f(x) = x³ + 2x² - 5x + 1"
                    className={`w-full p-5 rounded-2xl transition-all resize-none text-lg text-center ${
                      isDark 
                        ? "bg-black/40 text-white placeholder-gray-600 border border-violet-500/30 shadow-[0_0_15px_rgba(139,92,246,0.15)] focus:border-violet-500/60 focus:shadow-[0_0_25px_rgba(139,92,246,0.3)]" 
                        : "bg-gray-50 text-gray-900 placeholder-gray-400 border border-violet-300/50 shadow-[0_0_15px_rgba(139,92,246,0.1)] focus:border-violet-400 focus:shadow-[0_0_25px_rgba(139,92,246,0.2)]"
                    } focus:outline-none`}
                    rows={3}
                  />

                  <div className="flex flex-col sm:flex-row gap-4 mt-8">
                    <button
                      type="submit"
                      disabled={!problem.trim()}
                      className={`flex-1 py-4 px-8 rounded-2xl font-semibold text-base transition-all disabled:opacity-30 disabled:cursor-not-allowed ${
                        isDark 
                          ? "bg-white text-black hover:bg-gray-100" 
                          : "bg-gray-900 text-white hover:bg-gray-800"
                      }`}
                    >
                      Generate Video
                    </button>

                    <button
                      type="button"
                      onClick={() => fileInputRef.current?.click()}
                      className={`flex-1 py-4 px-8 rounded-2xl font-semibold text-base transition-all flex items-center justify-center gap-3 ${
                        isDark 
                          ? "bg-white/[0.05] hover:bg-white/[0.08] border border-white/[0.08]" 
                          : "bg-gray-100 hover:bg-gray-200 border border-gray-200"
                      }`}
                    >
                      {Icons.camera}
                      <span>Upload Photo</span>
                    </button>
                  </div>
                </form>

                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  capture="environment"
                  onChange={handleImageUpload}
                  className="hidden"
                />

                <div className={`mt-10 pt-8 border-t ${isDark ? "border-white/[0.05]" : "border-gray-100"}`}>
                  <p className={`text-xs uppercase tracking-widest mb-4 text-center ${
                    isDark ? "text-gray-600" : "text-gray-400"
                  }`}>Try an example</p>
                  <div className="flex flex-wrap gap-3 justify-center">
                    {[
                      "Solve for x: 3x - 7 = 14",
                      "Find the derivative of x² + 3x",
                      "Prove by induction: 1+2+...+n = n(n+1)/2",
                    ].map((ex) => (
                      <button
                        key={ex}
                        onClick={() => setProblem(ex)}
                        className={`px-5 py-2.5 text-sm rounded-full transition-all ${
                          isDark 
                            ? "bg-white/[0.03] hover:bg-white/[0.06] border border-white/[0.05] hover:border-white/[0.1] text-gray-400 hover:text-white" 
                            : "bg-gray-100 hover:bg-gray-200 border border-gray-200 text-gray-600 hover:text-gray-900"
                        }`}
                      >
                        {ex}
                      </button>
                    ))}
                  </div>
                </div>
              </>
            )}

            {(status === "parsing" || status === "generating") && (
              <div className="flex flex-col items-center py-16">
                <div className={`w-10 h-10 border-2 rounded-full animate-spin mb-10 ${
                  isDark ? "border-white/10 border-t-white" : "border-gray-200 border-t-gray-900"
                }`} />
                
                <h3 className="text-2xl font-medium mb-3 text-center">
                  {status === "parsing" ? "Analyzing problem" : "Generating video"}
                </h3>
                
                <p className={`text-center max-w-sm ${isDark ? "text-gray-500" : "text-gray-600"}`}>
                  {status === "parsing"
                    ? "Breaking down the problem into clear steps"
                    : "Creating animations and narration — about 30 seconds"}
                </p>

                {job?.steps && (
                  <div className="mt-10 w-full max-w-md">
                    <p className={`text-xs uppercase tracking-widest mb-4 text-center ${
                      isDark ? "text-gray-600" : "text-gray-400"
                    }`}>{job.steps.length} steps identified</p>
                    <div className="space-y-3 max-h-48 overflow-y-auto">
                      {job.steps.slice(0, 5).map((step, i) => (
                        <div key={i} className="flex items-start gap-4 text-sm">
                          <span className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-medium ${
                            isDark ? "bg-white/[0.05] text-gray-500" : "bg-gray-100 text-gray-500"
                          }`}>
                            {i + 1}
                          </span>
                          <span className={`pt-1 ${isDark ? "text-gray-400" : "text-gray-600"}`}>{step.narration}</span>
                        </div>
                      ))}
                      {job.steps.length > 5 && (
                        <p className={`text-xs pl-11 ${isDark ? "text-gray-600" : "text-gray-400"}`}>+{job.steps.length - 5} more</p>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}

            {status === "complete" && job?.video_url && (
              <div className="flex flex-col items-center">
                <div className={`w-full aspect-video rounded-2xl overflow-hidden mb-8 ring-1 ${
                  isDark ? "bg-black ring-white/[0.08]" : "bg-gray-100 ring-gray-200"
                }`}>
                  <video
                    src={`${API_URL}${job.video_url}`}
                    controls
                    autoPlay
                    className="w-full h-full"
                  />
                </div>

                <h3 className="text-2xl font-medium mb-3 text-center">
                  Video ready
                </h3>

                <p className={`text-center mb-8 max-w-md ${isDark ? "text-gray-500" : "text-gray-600"}`}>
                  {job.problem}
                </p>

                <div className="flex gap-4">
                  <a
                    href={`${API_URL}${job.video_url}`}
                    download
                    className={`py-3.5 px-6 rounded-xl font-medium transition-all flex items-center gap-2.5 ${
                      isDark 
                        ? "bg-white/[0.05] hover:bg-white/[0.08] border border-white/[0.08]" 
                        : "bg-gray-100 hover:bg-gray-200 border border-gray-200"
                    }`}
                  >
                    {Icons.download}
                    <span>Download</span>
                  </a>
                  <button 
                    onClick={reset} 
                    className={`py-3.5 px-8 rounded-xl font-medium transition-all ${
                      isDark 
                        ? "bg-white text-black hover:bg-gray-100" 
                        : "bg-gray-900 text-white hover:bg-gray-800"
                    }`}
                  >
                    Solve Another
                  </button>
                </div>
              </div>
            )}

            {status === "error" && (
              <div className="flex flex-col items-center py-16">
                <div className="w-14 h-14 rounded-full bg-red-500/10 text-red-400 flex items-center justify-center mb-8">
                  {Icons.x}
                </div>
                <h3 className="text-2xl font-medium mb-3 text-center">Something went wrong</h3>
                <p className={`text-center mb-8 ${isDark ? "text-gray-500" : "text-gray-600"}`}>{error || "Please try again."}</p>
                <button onClick={reset} className={`py-3.5 px-8 rounded-xl font-medium transition-all ${
                  isDark 
                    ? "bg-white text-black hover:bg-gray-100" 
                    : "bg-gray-900 text-white hover:bg-gray-800"
                }`}>
                  Try Again
                </button>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className={`w-full py-32 border-t ${isDark ? "border-white/[0.05]" : "border-gray-200"}`}>
        <div className="w-full max-w-6xl mx-auto px-6 md:px-12">
          <div className="text-center mb-20">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-semibold mb-5">How it works</h2>
            <p className={`text-lg ${isDark ? "text-gray-500" : "text-gray-600"}`}>Three simple steps to understanding</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-12 md:gap-16">
            {[
              { icon: Icons.edit, title: "Type or snap", desc: "Enter any math problem or upload a photo of your homework" },
              { icon: Icons.cpu, title: "AI explains", desc: "Every step broken down with clear, human-like narration" },
              { icon: Icons.play, title: "Watch & learn", desc: "Custom video walkthrough generated in seconds" },
            ].map((item, i) => (
              <div key={item.title} className="flex flex-col items-center text-center">
                <div className={`w-20 h-20 mb-8 rounded-2xl flex items-center justify-center ${
                  isDark 
                    ? "bg-white/[0.03] border border-white/[0.08] text-gray-400" 
                    : "bg-gray-100 border border-gray-200 text-gray-500"
                }`}>
                  {item.icon}
                </div>
                <div className={`text-xs uppercase tracking-widest mb-3 ${isDark ? "text-gray-600" : "text-gray-400"}`}>Step {i + 1}</div>
                <h3 className="text-xl font-semibold mb-3">{item.title}</h3>
                <p className={`leading-relaxed ${isDark ? "text-gray-500" : "text-gray-600"}`}>{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className={`w-full py-32 border-t ${isDark ? "border-white/[0.05]" : "border-gray-200"}`}>
        <div className="w-full max-w-5xl mx-auto px-8 md:px-12">
          <div className="text-center mb-20">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-semibold mb-5">Simple pricing</h2>
            <p className={`text-lg ${isDark ? "text-gray-500" : "text-gray-600"}`}>Buy minutes. Use anytime. No subscription.</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-6">
            {Object.entries(PRICING).map(([key, tier]) => (
              <div 
                key={key} 
                className={`rounded-3xl p-8 border transition-all flex flex-col ${
                  key === "standard" 
                    ? isDark
                      ? "bg-white text-black border-white shadow-2xl shadow-white/10 md:-mt-4 md:mb-4"
                      : "bg-gray-900 text-white border-gray-900 shadow-2xl shadow-gray-900/20 md:-mt-4 md:mb-4"
                    : isDark
                      ? "bg-white/[0.02] border-white/[0.08]"
                      : "bg-white border-gray-200"
                }`}
              >
                {tier.badge && (
                  <div className={`text-xs font-semibold uppercase tracking-widest mb-3 ${
                    key === "standard"
                      ? isDark ? "text-violet-600" : "text-violet-400"
                      : "text-green-500"
                  }`}>{tier.badge}</div>
                )}
                <h3 className="text-xl font-semibold mb-2">{tier.name}</h3>
                <div className="mb-2">
                  <span className="text-5xl font-semibold">${tier.price}</span>
                </div>
                <p className={`mb-1 text-lg font-medium ${
                  key === "standard" 
                    ? isDark ? "text-gray-700" : "text-gray-300"
                    : isDark ? "text-gray-300" : "text-gray-700"
                }`}>{tier.minutes} minutes</p>
                <p className={`mb-8 text-sm ${
                  key === "standard" 
                    ? isDark ? "text-gray-500" : "text-gray-400"
                    : isDark ? "text-gray-600" : "text-gray-500"
                }`}>{tier.pricePerMin}/min</p>
                <ul className="space-y-4 mb-10 flex-1">
                  {tier.features.map((f) => (
                    <li key={f} className="flex items-center gap-3">
                      <span className={key === "standard" 
                        ? isDark ? "text-violet-600" : "text-violet-400"
                        : "text-violet-400"
                      }>{Icons.check}</span>
                      <span className={
                        key === "standard" 
                          ? isDark ? "text-gray-700" : "text-gray-300"
                          : isDark ? "text-gray-400" : "text-gray-600"
                      }>{f}</span>
                    </li>
                  ))}
                </ul>
                <button className={`w-full py-4 rounded-xl font-semibold transition-all ${
                  key === "standard"
                    ? isDark
                      ? "bg-black text-white hover:bg-gray-900"
                      : "bg-white text-gray-900 hover:bg-gray-100"
                    : isDark
                      ? "bg-white/[0.05] hover:bg-white/[0.08] border border-white/[0.08]"
                      : "bg-gray-100 hover:bg-gray-200 border border-gray-200"
                }`}>
                  Buy Now
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className={`w-full py-20 border-t ${isDark ? "border-white/[0.05]" : "border-gray-200"}`}>
        <div className="w-full max-w-4xl mx-auto px-6 text-center">
          <div className={`text-2xl font-semibold tracking-tight mb-4 ${isDark ? "text-white/40" : "text-gray-400"}`}>Orbital</div>
          <p className={isDark ? "text-gray-600" : "text-gray-500"}>{SITE.footer}</p>
        </div>
      </footer>
    </div>
  );
}
