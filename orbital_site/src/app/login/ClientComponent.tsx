"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { getSupabase } from "@/lib/supabase";
import { signInWithGoogle } from "@/app/auth/actions";

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
  lock: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
    </svg>
  ),
  eye: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  ),
  eyeOff: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
    </svg>
  ),
};

export default function ClientComponent() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isGoogleLoading, setIsGoogleLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [theme, setTheme] = useState<Theme>("dark");
  
  const router = useRouter();
  const { user, loading: authLoading, signIn } = useAuth();
  const supabase = getSupabase();

  useEffect(() => {
    const saved = localStorage.getItem("orbital-theme") as Theme;
    if (saved) setTheme(saved);
  }, []);

  // Redirect if already logged in
  useEffect(() => {
    if (!authLoading && user) {
      router.push("/dashboard");
    }
  }, [user, authLoading, router]);

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
      const { data, error: signInError } = await signIn(email, password);
      
      if (signInError) {
        setError(signInError.message);
        setIsLoading(false);
        return;
      }
      
      // Explicitly redirect on success
      router.push("/dashboard");
      
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
      setIsLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setIsGoogleLoading(true);
    setError(null);
    
    try {
      // Use server action to initiate OAuth (stores PKCE verifier in cookies)
      await signInWithGoogle();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Google sign in failed");
      setIsGoogleLoading(false);
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

      {/* Login Card */}
      <div className={`w-full max-w-md rounded-3xl p-8 ${
        isDark 
          ? "bg-gradient-to-b from-white/[0.08] to-white/[0.02] border border-white/[0.08]" 
          : "bg-gray-50 border border-gray-100"
      }`}>
        
        <div className="text-center mb-8">
          <h1 className="text-2xl font-semibold mb-2">Welcome back</h1>
          <p className={`text-sm ${isDark ? "text-gray-500" : "text-gray-600"}`}>
            Sign in to continue solving
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

          {/* Password Field */}
          <div>
            <label className={`block text-xs font-medium uppercase tracking-widest mb-2 ${
              isDark ? "text-gray-500" : "text-gray-500"
            }`}>
              Password
            </label>
            <div className="relative">
              <div className={`absolute left-4 top-1/2 -translate-y-1/2 ${
                isDark ? "text-gray-500" : "text-gray-400"
              }`}>
                {Icons.lock}
              </div>
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className={`w-full pl-12 pr-12 py-3.5 rounded-xl transition-all ${
                  isDark 
                    ? "bg-black/40 text-white placeholder-gray-600 border border-white/[0.08] focus:border-violet-500/50" 
                    : "bg-gray-50 text-gray-900 placeholder-gray-400 border border-gray-200 focus:border-violet-400"
                } focus:outline-none`}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className={`absolute right-4 top-1/2 -translate-y-1/2 ${
                  isDark ? "text-gray-500 hover:text-gray-400" : "text-gray-400 hover:text-gray-500"
                }`}
              >
                {showPassword ? Icons.eyeOff : Icons.eye}
              </button>
            </div>
          </div>

          {/* Forgot Password */}
          <div className="text-right">
            <Link href="/forgot-password" className={`text-sm ${
              isDark ? "text-violet-400 hover:text-violet-300" : "text-violet-600 hover:text-violet-500"
            }`}>
              Forgot password?
            </Link>
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
            {isLoading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        {/* Divider */}
        <div className="flex items-center gap-4 my-8">
          <div className={`flex-1 h-px ${isDark ? "bg-white/[0.08]" : "bg-gray-200"}`} />
          <span className={`text-xs uppercase tracking-widest ${isDark ? "text-gray-600" : "text-gray-400"}`}>
            or
          </span>
          <div className={`flex-1 h-px ${isDark ? "bg-white/[0.08]" : "bg-gray-200"}`} />
        </div>

        {/* Google Sign In */}
        <button
          type="button"
          onClick={handleGoogleSignIn}
          disabled={isGoogleLoading || isLoading}
          className={`w-full py-3.5 rounded-xl font-medium transition-all flex items-center justify-center gap-3 disabled:opacity-50 ${
            isDark 
              ? "bg-white/[0.05] hover:bg-white/[0.08] border border-white/[0.08]" 
              : "bg-gray-50 hover:bg-gray-100 border border-gray-200"
          }`}
        >
          {isGoogleLoading ? (
            <div className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin" />
          ) : (
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
          )}
          {isGoogleLoading ? "Connecting..." : "Continue with Google"}
        </button>

        {/* Sign Up Link */}
        <p className={`text-center mt-8 text-sm ${isDark ? "text-gray-500" : "text-gray-600"}`}>
          Don't have an account?{" "}
          <Link href="/signup" className={`font-medium ${
            isDark ? "text-white hover:text-gray-300" : "text-gray-900 hover:text-gray-700"
          }`}>
            Sign up
          </Link>
        </p>
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
