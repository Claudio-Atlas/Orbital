"use client";

import { useState, useEffect } from "react";
import { SITE, PRICING } from "@/lib/constants";
import { OrbitalLogo } from "@/components/OrbitalLogo";

type Theme = "dark" | "light";

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

            {/* Auth Links */}
            <a
              href="/login"
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                isDark 
                  ? "text-gray-300 hover:text-white hover:bg-white/10" 
                  : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
              }`}
            >
              Log in
            </a>
            <a
              href="/signup"
              className="px-4 py-2 text-sm font-medium rounded-lg bg-violet-600 text-white hover:bg-violet-500 transition-colors"
            >
              Sign up
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

      {/* Coming Soon */}
      <section className="w-full pb-32">
        <div className="w-full max-w-2xl mx-auto px-6">
          <div className={`rounded-[2rem] p-8 md:p-12 ${
            isDark 
              ? "bg-gradient-to-b from-white/[0.08] to-white/[0.02] border border-white/[0.08]" 
              : "bg-white border border-gray-200 shadow-xl shadow-gray-200/50"
          }`}>
            <div className="flex flex-col items-center text-center py-8">
              {/* Orbital logo/icon */}
              <div className={`w-20 h-20 mb-8 rounded-2xl flex items-center justify-center ${
                isDark 
                  ? "bg-violet-500/10 border border-violet-500/20" 
                  : "bg-violet-100 border border-violet-200"
              }`}>
                <OrbitalLogo className="w-10 h-10 text-violet-500" />
              </div>
              
              <h2 className={`text-3xl sm:text-4xl font-semibold mb-4 ${
                isDark ? "text-white" : "text-gray-900"
              }`}>
                Coming Soon
              </h2>
              
              <p className={`text-lg max-w-md mb-8 ${
                isDark ? "text-gray-400" : "text-gray-600"
              }`}>
                AI-powered math videos that explain any problem step by step. 
                We&apos;re putting the finishing touches on something special.
              </p>
              
              {/* Example problems teaser */}
              <div className={`w-full rounded-2xl p-6 ${
                isDark 
                  ? "bg-black/40 border border-violet-500/20" 
                  : "bg-gray-50 border border-gray-200"
              }`}>
                <p className={`text-xs uppercase tracking-widest mb-4 ${
                  isDark ? "text-gray-500" : "text-gray-400"
                }`}>
                  Soon you&apos;ll be able to solve
                </p>
                <div className="space-y-3">
                  {[
                    "Solve for x: 3x - 7 = 14",
                    "Find the derivative of x² + 3x",
                    "Prove by induction: 1+2+...+n = n(n+1)/2",
                  ].map((ex) => (
                    <div 
                      key={ex}
                      className={`px-4 py-3 rounded-xl text-sm ${
                        isDark 
                          ? "bg-white/[0.03] border border-white/[0.05] text-gray-400" 
                          : "bg-white border border-gray-200 text-gray-600"
                      }`}
                    >
                      {ex}
                    </div>
                  ))}
                </div>
              </div>
            </div>
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
          <div className="flex justify-center gap-6 mb-4">
            <a href="/terms" className={`text-sm hover:underline ${isDark ? "text-gray-500 hover:text-gray-400" : "text-gray-500 hover:text-gray-600"}`}>Terms of Service</a>
            <a href="/privacy" className={`text-sm hover:underline ${isDark ? "text-gray-500 hover:text-gray-400" : "text-gray-500 hover:text-gray-600"}`}>Privacy Policy</a>
          </div>
          <p className={isDark ? "text-gray-600" : "text-gray-500"}>{SITE.footer}</p>
        </div>
      </footer>
    </div>
  );
}
