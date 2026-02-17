"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { getSupabase } from "@/lib/supabase";
import { useTheme } from "@/lib/theme-context";
import { OrbitalLogo } from "@/components/OrbitalLogo";
import { AccentColorPicker, AccentColorPickerGrid } from "@/components/AccentColorPicker";

const VOICES = [
  { id: "clayton", name: "Clayton", desc: "Warm & clear", avatar: "🎓" },
  { id: "professor", name: "Professor", desc: "Deep & authoritative", avatar: "👨‍🏫" },
  { id: "alex", name: "Alex", desc: "Friendly & casual", avatar: "😊" },
  { id: "sarah", name: "Sarah", desc: "Bright & engaging", avatar: "👩‍🔬" },
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
  arrowLeft: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
    </svg>
  ),
  check: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
    </svg>
  ),
  user: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
  ),
  microphone: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
    </svg>
  ),
  palette: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.098 19.902a3.75 3.75 0 005.304 0l6.401-6.402M6.75 21A3.75 3.75 0 013 17.25V4.125C3 3.504 3.504 3 4.125 3h5.25c.621 0 1.125.504 1.125 1.125v4.072M6.75 21a3.75 3.75 0 003.75-3.75V8.197M6.75 21h13.125c.621 0 1.125-.504 1.125-1.125v-5.25c0-.621-.504-1.125-1.125-1.125h-4.072M10.5 8.197l2.88-2.88c.438-.439 1.15-.439 1.59 0l3.712 3.713c.44.44.44 1.152 0 1.59l-2.879 2.88M6.75 17.25h.008v.008H6.75v-.008z" />
    </svg>
  ),
  sparkles: (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z" />
    </svg>
  ),
};

export default function SettingsClient() {
  const { theme, toggleTheme, isDark, accent } = useTheme();
  const [defaultVoice, setDefaultVoice] = useState("clayton");
  const [displayName, setDisplayName] = useState("");
  const [isSavingName, setIsSavingName] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [nameSuccess, setNameSuccess] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteConfirmText, setDeleteConfirmText] = useState("");
  const [deleteError, setDeleteError] = useState<string | null>(null);

  const router = useRouter();
  const { user, profile, loading: authLoading, refreshProfile, signOut } = useAuth();
  const supabase = getSupabase();

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    const storedVoice = localStorage.getItem("orbital-default-voice");
    if (storedVoice) setDefaultVoice(storedVoice);
  }, []);

  useEffect(() => {
    if (profile?.display_name) {
      setDisplayName(profile.display_name);
    }
  }, [profile]);

  const handleSaveVoice = (voiceId: string) => {
    setDefaultVoice(voiceId);
    localStorage.setItem("orbital-default-voice", voiceId);
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 2000);
  };

  const handleSaveName = async () => {
    if (!user) return;
    setIsSavingName(true);
    try {
      const { error } = await supabase.from("profiles").update({ display_name: displayName.trim() }).eq("id", user.id);
      if (!error) {
        setNameSuccess(true);
        setTimeout(() => setNameSuccess(false), 2000);
        refreshProfile();
      }
    } catch (err) {
      console.error("Error saving name:", err);
    } finally {
      setIsSavingName(false);
    }
  };

  const handleDeleteAccount = async () => {
    if (deleteConfirmText !== "DELETE") return;
    setIsDeleting(true);
    try {
      const { error: deleteError } = await supabase.from("profiles").delete().eq("id", user?.id);
      if (deleteError) {
        console.error("Error deleting profile:", deleteError);
        setDeleteError("We couldn't delete your account right now. Please try again or contact hello@orbitalsolver.io");
        setIsDeleting(false);
        return;
      }
      await signOut();
      router.push("/?deleted=true");
    } catch (err) {
      console.error("Error deleting account:", err);
      setDeleteError("Something went wrong. Please try again or contact hello@orbitalsolver.io");
      setIsDeleting(false);
    }
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
        <div className="max-w-3xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className={`p-2 rounded-lg transition-colors ${isDark ? "hover:bg-white/10" : "hover:bg-gray-100"}`}>
              {Icons.arrowLeft}
            </Link>
            <h1 className="text-lg font-semibold">Settings</h1>
          </div>
          <Link href="/" className="flex items-center gap-2">
            <OrbitalLogo className="w-8 h-8" />
          </Link>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-6 py-8 space-y-8">
        {/* Account Section */}
        <section className={`rounded-2xl p-6 ${isDark ? "bg-white/5 border border-white/10" : "bg-white border border-gray-200"}`}>
          <div className="flex items-center gap-3 mb-6">
            {Icons.user}
            <h2 className="text-lg font-semibold">Account</h2>
          </div>
          <div className="space-y-4">
            <div>
              <label className="text-xs font-medium uppercase tracking-widest text-themed-muted">Display Name</label>
              <div className="mt-2 flex gap-2">
                <input 
                  type="text" 
                  value={displayName} 
                  onChange={(e) => setDisplayName(e.target.value)} 
                  placeholder="Your name" 
                  className={`flex-1 px-4 py-2.5 rounded-xl transition-all input-glow ${isDark ? "bg-black/40 text-white placeholder-gray-600 border border-white/10 focus:border-[var(--accent)]" : "bg-gray-50 text-gray-900 placeholder-gray-400 border border-gray-200 focus:border-[var(--accent)]"} focus:outline-none`} 
                />
                <button 
                  onClick={handleSaveName} 
                  disabled={isSavingName} 
                  className="px-4 py-2.5 rounded-xl font-medium text-white disabled:opacity-50 transition-all btn-glow"
                  style={{ background: accent.main }}
                >
                  {isSavingName ? "..." : nameSuccess ? "✓" : "Save"}
                </button>
              </div>
              <p className="mt-1.5 text-xs text-themed-muted">Used to personalize your video explanations</p>
            </div>
            <div>
              <label className="text-xs font-medium uppercase tracking-widest text-themed-muted">Email</label>
              <p className="mt-1 font-medium">{user?.email}</p>
            </div>
            <div>
              <label className="text-xs font-medium uppercase tracking-widest text-themed-muted">Minutes Balance</label>
              <p className="mt-1">
                <span className="text-2xl font-bold" style={{ color: accent.main }}>{profile?.minutes_balance ?? 0}</span>
                <span className="ml-2 text-themed-secondary">minutes</span>
              </p>
            </div>
            <div>
              <label className="text-xs font-medium uppercase tracking-widest text-themed-muted">Member Since</label>
              <p className="mt-1 font-medium">{profile?.created_at ? new Date(profile.created_at).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" }) : "—"}</p>
            </div>
          </div>
        </section>

        {/* Voice Section */}
        <section className={`rounded-2xl p-6 ${isDark ? "bg-white/5 border border-white/10" : "bg-white border border-gray-200"}`}>
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              {Icons.microphone}
              <h2 className="text-lg font-semibold">Default Voice</h2>
            </div>
            {saveSuccess && <span className="flex items-center gap-1 text-sm text-green-500">{Icons.check} Saved</span>}
          </div>
          <p className="mb-4 text-sm text-themed-secondary">Choose the default voice for your video explanations.</p>
          <div className="grid grid-cols-2 gap-3">
            {VOICES.map((voice) => (
              <button 
                key={voice.id} 
                onClick={() => handleSaveVoice(voice.id)} 
                className={`flex items-center gap-3 p-4 rounded-xl text-left transition-all ${
                  defaultVoice === voice.id 
                    ? `border-2` 
                    : `border ${isDark ? "bg-white/5 border-white/10 hover:border-white/20" : "bg-gray-50 border-gray-200 hover:border-gray-300"}`
                }`}
                style={defaultVoice === voice.id ? { 
                  borderColor: accent.main,
                  background: `${accent.main}15`
                } : undefined}
              >
                <span className="text-2xl">{voice.avatar}</span>
                <div className="flex-1">
                  <p className="font-medium">{voice.name}</p>
                  <p className="text-xs text-themed-muted">{voice.desc}</p>
                </div>
                {defaultVoice === voice.id && <span style={{ color: accent.main }}>{Icons.check}</span>}
              </button>
            ))}
          </div>
        </section>

        {/* Appearance Section */}
        <section className={`rounded-2xl p-6 ${isDark ? "bg-white/5 border border-white/10" : "bg-white border border-gray-200"}`}>
          <div className="flex items-center gap-3 mb-6">
            {Icons.palette}
            <h2 className="text-lg font-semibold">Appearance</h2>
          </div>
          
          <div className="space-y-6">
            {/* Theme Toggle */}
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Theme</p>
                <p className="text-sm text-themed-secondary">{isDark ? "Dark mode" : "Light mode"}</p>
              </div>
              <button 
                onClick={toggleTheme} 
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${isDark ? "bg-white/10 hover:bg-white/15" : "bg-gray-100 hover:bg-gray-200"}`}
              >
                {isDark ? Icons.sun : Icons.moon}
                <span className="text-sm font-medium">{isDark ? "Light" : "Dark"}</span>
              </button>
            </div>

            {/* Accent Color */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                {Icons.sparkles}
                <p className="font-medium">Accent Color</p>
              </div>
              <p className="text-sm text-themed-secondary mb-4">Personalize Orbital with your favorite color.</p>
              <AccentColorPickerGrid />
            </div>
          </div>
        </section>

        {/* Danger Zone */}
        <section className={`rounded-2xl p-6 border ${isDark ? "border-red-500/20" : "border-red-200"}`}>
          <h2 className="text-lg font-semibold text-red-500 mb-4">Danger Zone</h2>
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Delete Account</p>
              <p className="text-sm text-themed-secondary">Permanently delete your account and all data</p>
            </div>
            <button 
              onClick={() => setShowDeleteModal(true)} 
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${isDark ? "bg-red-500/10 text-red-400 hover:bg-red-500/20" : "bg-red-50 text-red-600 hover:bg-red-100"}`}
            >
              Delete Account
            </button>
          </div>
        </section>
      </main>

      {/* Delete Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => !isDeleting && setShowDeleteModal(false)} />
          <div className={`relative w-full max-w-md rounded-2xl p-6 ${isDark ? "bg-zinc-900 border border-white/10" : "bg-white"}`}>
            <h3 className="text-xl font-bold text-red-500 mb-2">Delete Account</h3>
            <p className="text-sm mb-4 text-themed-secondary">This action is <strong>permanent</strong>. All your data will be deleted.</p>
            <p className="text-sm mb-2 text-themed-primary">Type <strong>DELETE</strong> to confirm:</p>
            <input 
              type="text" 
              value={deleteConfirmText} 
              onChange={(e) => { setDeleteConfirmText(e.target.value); setDeleteError(null); }} 
              placeholder="DELETE" 
              disabled={isDeleting} 
              className={`w-full px-4 py-2 rounded-lg mb-4 ${isDark ? "bg-black/50 border border-white/10 text-white placeholder-gray-600" : "bg-gray-50 border border-gray-200 text-gray-900 placeholder-gray-400"} focus:outline-none focus:ring-2 focus:ring-red-500/50`} 
            />
            {deleteError && (
              <p className="text-sm text-red-400 mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20">{deleteError}</p>
            )}
            <div className="flex gap-3">
              <button 
                onClick={() => { setShowDeleteModal(false); setDeleteConfirmText(""); }} 
                disabled={isDeleting} 
                className={`flex-1 py-2 rounded-lg font-medium transition-colors ${isDark ? "bg-white/10 hover:bg-white/20" : "bg-gray-100 hover:bg-gray-200"}`}
              >
                Cancel
              </button>
              <button 
                onClick={handleDeleteAccount} 
                disabled={deleteConfirmText !== "DELETE" || isDeleting} 
                className="flex-1 py-2 rounded-lg font-medium bg-red-600 text-white hover:bg-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isDeleting ? "Deleting..." : "Delete Forever"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
