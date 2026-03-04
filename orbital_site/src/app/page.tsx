"use client";

import { useState, useEffect, useRef } from "react";
import { SITE, PRICING_STUDENT, PRICING_INSTRUCTOR } from "@/lib/constants";
import { OrbitalLogo } from "@/components/OrbitalLogo";
import { VideoCarousel } from "@/components/VideoCarousel";

type Theme = "dark" | "light";

// Login Required Modal
function LoginModal({ isOpen, onClose, isDark }: { isOpen: boolean; onClose: () => void; isDark: boolean }) {
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className={`relative w-full max-w-md rounded-3xl p-8 ${
        isDark 
          ? "bg-zinc-900 border border-white/10" 
          : "bg-white border border-gray-200 shadow-2xl"
      }`}>
        {/* Close button */}
        <button
          onClick={onClose}
          className={`absolute top-4 right-4 p-2 rounded-full transition-colors ${
            isDark ? "hover:bg-white/10 text-gray-400" : "hover:bg-gray-100 text-gray-500"
          }`}
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Content */}
        <div className="text-center">
          <div className={`w-16 h-16 mx-auto mb-6 rounded-2xl flex items-center justify-center ${
            isDark 
              ? "bg-violet-500/10 border border-violet-500/20" 
              : "bg-violet-100 border border-violet-200"
          }`}>
            <OrbitalLogo className="w-8 h-8 text-violet-500" />
          </div>
          
          <h2 className="text-2xl font-bold mb-2">Sign in to purchase</h2>
          <p className={`mb-8 ${isDark ? "text-gray-400" : "text-gray-500"}`}>
            Create an account or log in to buy minutes and start generating videos.
          </p>
          
          <div className="flex flex-col gap-3">
            <a
              href="/signup"
              className="w-full py-3.5 rounded-xl font-semibold bg-violet-600 text-white hover:bg-violet-500 transition-colors"
            >
              Sign up
            </a>
            <a
              href="/login"
              className={`w-full py-3.5 rounded-xl font-semibold transition-colors ${
                isDark 
                  ? "bg-white/5 hover:bg-white/10 border border-white/10" 
                  : "bg-gray-100 hover:bg-gray-200 border border-gray-200"
              }`}
            >
              Log in
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

// Clean SVG Icons
const Icons = {
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
  const [theme, setTheme] = useState<Theme>("dark");
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [waitlistEmail, setWaitlistEmail] = useState("");
  const [waitlistName, setWaitlistName] = useState("");
  const [waitlistSubmitted, setWaitlistSubmitted] = useState(false);
  const [waitlistLoading, setWaitlistLoading] = useState(false);
  const [pricingMode, setPricingMode] = useState<"student" | "instructor">("student");

  const handleWaitlist = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!waitlistEmail) return;
    setWaitlistLoading(true);
    // For now just simulate — wire up to Supabase/API later
    await new Promise(r => setTimeout(r, 800));
    setWaitlistSubmitted(true);
    setWaitlistLoading(false);
  };

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

  return (
    <div className={`min-h-screen overflow-x-hidden w-full flex flex-col items-center transition-colors duration-300 ${
      isDark ? "bg-black text-white" : "bg-gray-50 text-gray-900"
    }`}>
      
      {/* Header */}
      <header className={`fixed top-0 left-0 right-0 z-50 backdrop-blur-xl border-b ${
        isDark 
          ? "bg-black/80 border-white/10" 
          : "bg-white/80 border-gray-200"
      }`}>
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          {/* Logo */}
          <a href="/" className="flex items-center gap-2">
            <OrbitalLogo className="w-8 h-8" />
            <span className="font-semibold text-lg">Orbital</span>
          </a>

          {/* Right Side */}
          <div className="flex items-center gap-3">
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className={`p-2 rounded-lg transition-colors ${
                isDark 
                  ? "hover:bg-white/10 text-gray-400 hover:text-white" 
                  : "hover:bg-gray-100 text-gray-500 hover:text-gray-900"
              }`}
              aria-label="Toggle theme"
            >
              {isDark ? Icons.sun : Icons.moon}
            </button>

            {/* Videos link */}
            <a
              href="/watch"
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                isDark 
                  ? "text-gray-300 hover:text-white hover:bg-white/10" 
                  : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
              }`}
            >
              Videos
            </a>

            {/* Notify Me */}
            <a
              href="#waitlist"
              className="px-4 py-2 text-sm font-medium rounded-lg bg-violet-500 text-white hover:bg-violet-400 transition-colors"
            >
              Get Notified
            </a>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="w-full pt-36 pb-24">
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


      {/* Video Showcase */}
      <section className="w-full pb-32">
        <div className="w-full max-w-4xl mx-auto px-6">
          <VideoCarousel isDark={isDark} />
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
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-semibold mb-5">Simple pricing</h2>
            <p className={`text-lg mb-8 ${isDark ? "text-gray-500" : "text-gray-600"}`}>Buy minutes. Use anytime. No subscription.</p>
            
            {/* Student / Instructor toggle */}
            <div className={`inline-flex rounded-xl p-1 ${
              isDark ? "bg-white/[0.05] border border-white/[0.08]" : "bg-gray-200"
            }`}>
              <button
                onClick={() => setPricingMode("student")}
                className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  pricingMode === "student"
                    ? isDark
                      ? "bg-violet-500 text-white"
                      : "bg-white text-gray-900 shadow-sm"
                    : isDark
                    ? "text-gray-400 hover:text-white"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                Students
              </button>
              <button
                onClick={() => setPricingMode("instructor")}
                className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  pricingMode === "instructor"
                    ? isDark
                      ? "bg-violet-500 text-white"
                      : "bg-white text-gray-900 shadow-sm"
                    : isDark
                    ? "text-gray-400 hover:text-white"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                Instructors
              </button>
            </div>
          </div>
          
          <div className={`grid gap-6 ${pricingMode === "instructor" ? "max-w-md mx-auto" : "md:grid-cols-3"}`}>
            {Object.entries(pricingMode === "student" ? PRICING_STUDENT : PRICING_INSTRUCTOR).map(([key, tier]) => (
              <div 
                key={key} 
                className={`rounded-3xl p-8 border transition-all flex flex-col ${
                  (key === "standard" || key === "institution" || key === "institution")
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
                    key === "standard" || key === "institution"
                      ? isDark ? "text-violet-600" : "text-violet-400"
                      : "text-green-500"
                  }`}>{tier.badge}</div>
                )}
                <h3 className="text-xl font-semibold mb-2">{tier.name}</h3>
                <div className="mb-2">
                  <span className="text-5xl font-semibold">{tier.price > 0 ? `$${tier.price}` : "Custom"}</span>
                  {pricingMode === "instructor" && tier.price > 0 && <span className="text-lg font-normal opacity-60">/mo</span>}
                </div>
                <p className={`mb-1 text-lg font-medium ${
                  key === "standard" || key === "institution" 
                    ? isDark ? "text-gray-700" : "text-gray-300"
                    : isDark ? "text-gray-300" : "text-gray-700"
                }`}>{tier.minutes > 0 ? `${tier.minutes} minutes` : pricingMode === "instructor" ? "AI usage at cost" : "Unlimited"}</p>
                <p className={`mb-8 text-sm ${
                  key === "standard" || key === "institution" || key === "institution"
                    ? isDark ? "text-gray-500" : "text-gray-400"
                    : isDark ? "text-gray-600" : "text-gray-500"
                }`}>{tier.price > 0 ? `${tier.pricePerMin}/min` : "Let's talk"}</p>
                <ul className="space-y-4 mb-10 flex-1">
                  {tier.features.map((f) => (
                    <li key={f} className="flex items-center gap-3">
                      <span className={key === "standard" || key === "institution" 
                        ? isDark ? "text-violet-600" : "text-violet-400"
                        : "text-violet-400"
                      }>{Icons.check}</span>
                      <span className={
                        key === "standard" || key === "institution" 
                          ? isDark ? "text-gray-700" : "text-gray-300"
                          : isDark ? "text-gray-400" : "text-gray-600"
                      }>{f}</span>
                    </li>
                  ))}
                </ul>
                <a 
                  href="#waitlist"
                  className={`w-full py-4 rounded-xl font-semibold transition-all text-center block ${
                  (key === "standard" || key === "institution")
                    ? isDark
                      ? "bg-violet-600 text-white hover:bg-violet-500"
                      : "bg-violet-600 text-white hover:bg-violet-500"
                    : isDark
                      ? "bg-white/[0.05] hover:bg-white/[0.08] border border-white/[0.08]"
                      : "bg-gray-100 hover:bg-gray-200 border border-gray-200"
                }`}>
                  {tier.price > 0 ? "Coming Soon" : "Contact Us"}
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Waitlist Section */}
      <section id="waitlist" className={`w-full py-32 border-t ${isDark ? "border-white/[0.05]" : "border-gray-200"}`}>
        <div className="w-full max-w-2xl mx-auto px-6 text-center">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-semibold mb-5">
            <span className={`bg-clip-text text-transparent ${
              isDark 
                ? "bg-gradient-to-r from-violet-400 to-purple-400" 
                : "bg-gradient-to-r from-violet-600 to-purple-600"
            }`}>
              Be the first to know
            </span>
          </h2>
          <p className={`text-lg mb-12 ${isDark ? "text-gray-500" : "text-gray-600"}`}>
            We&apos;re launching soon. Drop your info and we&apos;ll let you know when Orbital is live.
          </p>
          
          {waitlistSubmitted ? (
            <div className={`rounded-2xl p-8 ${
              isDark ? "bg-white/[0.03] border border-white/[0.08]" : "bg-gray-100 border border-gray-200"
            }`}>
              <div className="text-4xl mb-4">🎉</div>
              <h3 className="text-xl font-semibold mb-2">You&apos;re on the list!</h3>
              <p className={isDark ? "text-gray-400" : "text-gray-600"}>We&apos;ll notify you as soon as Orbital launches.</p>
            </div>
          ) : (
            <form onSubmit={handleWaitlist} className="flex flex-col sm:flex-row items-center justify-center gap-3 max-w-2xl mx-auto">
              <input
                type="text"
                placeholder="Your name"
                value={waitlistName}
                onChange={(e) => setWaitlistName(e.target.value)}
                className={`w-full sm:w-56 px-5 py-4 rounded-xl text-base outline-none transition-colors ${
                  isDark 
                    ? "bg-white/[0.05] border border-white/[0.1] text-white placeholder-gray-500 focus:border-violet-500/50" 
                    : "bg-white border border-gray-300 text-gray-900 placeholder-gray-400 focus:border-violet-500"
                }`}
              />
              <input
                type="email"
                placeholder="Your email"
                value={waitlistEmail}
                onChange={(e) => setWaitlistEmail(e.target.value)}
                required
                className={`w-full sm:w-56 px-5 py-4 rounded-xl text-base outline-none transition-colors ${
                  isDark 
                    ? "bg-white/[0.05] border border-white/[0.1] text-white placeholder-gray-500 focus:border-violet-500/50" 
                    : "bg-white border border-gray-300 text-gray-900 placeholder-gray-400 focus:border-violet-500"
                }`}
              />
              <button
                type="submit"
                disabled={waitlistLoading}
                className="px-8 py-4 rounded-xl font-semibold bg-violet-500 text-white hover:bg-violet-400 transition-colors disabled:opacity-50 whitespace-nowrap"
              >
                {waitlistLoading ? "..." : "Notify Me"}
              </button>
            </form>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className={`w-full py-20 border-t ${isDark ? "border-white/[0.05]" : "border-gray-200"}`}>
        <div className="w-full max-w-4xl mx-auto px-6 text-center">
          <div className={`text-2xl font-semibold tracking-tight mb-4 ${isDark ? "text-white/40" : "text-gray-400"}`}>Orbital</div>
          <div className="flex justify-center gap-6 mb-4">
            <a href="/terms" className={`text-sm hover:underline ${isDark ? "text-gray-500 hover:text-gray-400" : "text-gray-500 hover:text-gray-600"}`}>Terms of Service</a>
            <a href="/privacy" className={`text-sm hover:underline ${isDark ? "text-gray-500 hover:text-gray-400" : "text-gray-500 hover:text-gray-600"}`}>Privacy Policy</a>
          </div>
          <p className={isDark ? "text-gray-600" : "text-gray-500"}>{SITE.footer}</p>
        </div>
      </footer>

      {/* Login Required Modal */}
      <LoginModal 
        isOpen={showLoginModal} 
        onClose={() => setShowLoginModal(false)} 
        isDark={isDark} 
      />
    </div>
  );
}
