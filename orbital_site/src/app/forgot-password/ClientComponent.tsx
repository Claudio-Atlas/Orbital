"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { getSupabase } from "@/lib/supabase";

type Theme = "dark" | "light";

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
  email: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
    </svg>
  ),
  arrowLeft: (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
    </svg>
  ),
};

export default function ClientComponent() {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [theme, setTheme] = useState<Theme>("dark");

  const supabase = getSupabase();

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/reset-password`,
      });

      if (error) {
        setError(error.message);
        setIsLoading(false);
        return;
      }

      setSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
      setIsLoading(false);
    }
  };

  return (
    <div className={`min-h-screen w-full flex flex-col items-center justify-center px-4 transition-colors duration-300 ${
      isDark ? "bg-black text-white" : "bg-white text-gray-900"
    }`}>
      
      {/* Theme Toggle */}
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

      {/* Logo */}
      <Link href="/" className={`text-2xl font-semibold tracking-tight mb-8 ${
        isDark ? "text-white/80 hover:text-white" : "text-gray-700 hover:text-gray-900"
      } transition-colors`}>
        Orbital
      </Link>

      {/* Card */}
      <div className={`w-full max-w-md rounded-3xl p-8 ${
        isDark 
          ? "bg-gradient-to-b from-white/[0.08] to-white/[0.02] border border-white/[0.08]" 
          : "bg-gray-50 border border-gray-100"
      }`}>
        
        {success ? (
          /* Success State */
          <div className="text-center">
            <div className={`w-16 h-16 mx-auto mb-6 rounded-full flex items-center justify-center ${
              isDark ? "bg-green-500/20" : "bg-green-100"
            }`}>
              <svg className="w-8 h-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
            </div>
            <h1 className="text-2xl font-semibold mb-2">Check your email</h1>
            <p className={`mb-6 ${isDark ? "text-gray-400" : "text-gray-600"}`}>
              We sent a password reset link to<br />
              <span className="font-medium text-white">{email}</span>
            </p>
            <p className={`text-sm mb-8 ${isDark ? "text-gray-500" : "text-gray-500"}`}>
              Didn't receive the email? Check your spam folder or try again.
            </p>
            <Link
              href="/login"
              className={`inline-flex items-center gap-2 font-medium ${
                isDark ? "text-violet-400 hover:text-violet-300" : "text-violet-600 hover:text-violet-500"
              }`}
            >
              {Icons.arrowLeft}
              Back to login
            </Link>
          </div>
        ) : (
          /* Form State */
          <>
            <div className="text-center mb-8">
              <h1 className="text-2xl font-semibold mb-2">Forgot password?</h1>
              <p className={`text-sm ${isDark ? "text-gray-500" : "text-gray-600"}`}>
                No worries, we'll send you reset instructions.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Email Field */}
              <div>
                <label className={`block text-xs font-medium uppercase tracking-widest mb-2 ${
                  isDark ? "text-gray-500" : "text-gray-500"
                }`}>
                  Email
                </label>
                <div className="relative">
                  <div className={`absolute left-4 top-1/2 -translate-y-1/2 ${
                    isDark ? "text-gray-500" : "text-gray-400"
                  }`}>
                    {Icons.email}
                  </div>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    required
                    className={`w-full pl-12 pr-4 py-3.5 rounded-xl transition-all ${
                      isDark 
                        ? "bg-black/40 text-white placeholder-gray-600 border border-white/[0.08] focus:border-violet-500/50" 
                        : "bg-gray-50 text-gray-900 placeholder-gray-400 border border-gray-200 focus:border-violet-400"
                    } focus:outline-none`}
                  />
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
                  {error}
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading}
                className={`w-full py-4 rounded-xl font-semibold text-base transition-all disabled:opacity-50 ${
                  isDark 
                    ? "bg-white text-black hover:bg-gray-100" 
                    : "bg-gray-900 text-white hover:bg-gray-800"
                }`}
              >
                {isLoading ? "Sending..." : "Send Reset Link"}
              </button>
            </form>

            {/* Back to Login */}
            <div className="mt-8 text-center">
              <Link
                href="/login"
                className={`inline-flex items-center gap-2 text-sm font-medium ${
                  isDark ? "text-gray-400 hover:text-white" : "text-gray-600 hover:text-gray-900"
                }`}
              >
                {Icons.arrowLeft}
                Back to login
              </Link>
            </div>
          </>
        )}
      </div>

      {/* Back to Home */}
      <Link href="/" className={`mt-8 text-sm ${
        isDark ? "text-gray-600 hover:text-gray-500" : "text-gray-500 hover:text-gray-600"
      }`}>
        ← Back to home
      </Link>
    </div>
  );
}
