"use client";

import { useState, useEffect } from "react";
import { getSupabase } from "@/lib/supabase";

interface ApiKeys {
  deepseek_key: string;
  anthropic_key: string;
  elevenlabs_key: string;
}

interface ApiKeySettingsProps {
  userId: string;
}

function KeyInput({
  label,
  description,
  value,
  onChange,
  placeholder,
  required,
  docsUrl,
}: {
  label: string;
  description: string;
  value: string;
  onChange: (v: string) => void;
  placeholder: string;
  required?: boolean;
  docsUrl?: string;
}) {
  const [visible, setVisible] = useState(false);

  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-gray-300">{label}</label>
          {required && <span className="text-[10px] text-amber-400 bg-amber-500/10 px-1.5 py-0.5 rounded">Required</span>}
          {!required && <span className="text-[10px] text-gray-600 bg-white/[0.03] px-1.5 py-0.5 rounded">Optional</span>}
        </div>
        {docsUrl && (
          <a href={docsUrl} target="_blank" rel="noopener noreferrer" className="text-[10px] text-violet-400 hover:text-violet-300">
            Get API key →
          </a>
        )}
      </div>
      <p className="text-xs text-gray-600 mb-2">{description}</p>
      <div className="relative">
        <input
          type={visible ? "text" : "password"}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full px-3 py-2.5 rounded-lg bg-black/40 text-white/90 text-sm font-mono border border-white/[0.08] focus:border-violet-500/50 focus:outline-none pr-16"
        />
        <button
          onClick={() => setVisible(!visible)}
          className="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-500 hover:text-gray-300 transition-colors px-2 py-1"
        >
          {visible ? "Hide" : "Show"}
        </button>
      </div>
      {value && (
        <div className="mt-1 flex items-center gap-1">
          <span className="text-green-400 text-xs">✓</span>
          <span className="text-xs text-gray-600">Key saved ({value.slice(0, 8)}...)</span>
        </div>
      )}
    </div>
  );
}

export function ApiKeySettings({ userId }: ApiKeySettingsProps) {
  const [keys, setKeys] = useState<ApiKeys>({
    deepseek_key: "",
    anthropic_key: "",
    elevenlabs_key: "",
  });
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(true);

  // Load existing keys
  useEffect(() => {
    async function load() {
      const supabase = getSupabase();
      const { data } = await supabase
        .from("api_keys")
        .select("*")
        .eq("user_id", userId)
        .single();
      
      if (data) {
        setKeys({
          deepseek_key: data.deepseek_key || "",
          anthropic_key: data.anthropic_key || "",
          elevenlabs_key: data.elevenlabs_key || "",
        });
      }
      setLoading(false);
    }
    load();
  }, [userId]);

  const handleSave = async () => {
    setSaving(true);
    const supabase = getSupabase();
    
    const { error } = await supabase
      .from("api_keys")
      .upsert({
        user_id: userId,
        deepseek_key: keys.deepseek_key || null,
        anthropic_key: keys.anthropic_key || null,
        elevenlabs_key: keys.elevenlabs_key || null,
        updated_at: new Date().toISOString(),
      }, { onConflict: "user_id" });
    
    setSaving(false);
    if (!error) {
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="w-5 h-5 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const hasAllRequired = keys.deepseek_key && keys.anthropic_key && keys.elevenlabs_key;

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-sm font-medium text-gray-400 uppercase tracking-widest mb-1">
          API Keys
        </h3>
        <p className="text-xs text-gray-600 mb-4">
          These keys power video generation. Your keys are stored securely and never shared.
          {!hasAllRequired && (
            <span className="text-amber-400 ml-1">Add all required keys to enable generation.</span>
          )}
        </p>
      </div>

      <div className="space-y-5">
        <KeyInput
          label="DeepSeek"
          description="Used for script generation (Stage 1). Cheapest stage — ~$0.001 per video."
          value={keys.deepseek_key}
          onChange={(v) => setKeys((k) => ({ ...k, deepseek_key: v }))}
          placeholder="sk-..."
          required
          docsUrl="https://platform.deepseek.com/api_keys"
        />

        <KeyInput
          label="Anthropic (Claude)"
          description="Used for Verification Circle (Stage 2) and Lean formalization (Stage 3). Most expensive stage — ~$0.60 per video."
          value={keys.anthropic_key}
          onChange={(v) => setKeys((k) => ({ ...k, anthropic_key: v }))}
          placeholder="sk-ant-..."
          required
          docsUrl="https://console.anthropic.com/settings/keys"
        />

        <KeyInput
          label="ElevenLabs"
          description="Used for text-to-speech narration (Stage 4). ~$0.08 per 1K characters."
          value={keys.elevenlabs_key}
          onChange={(v) => setKeys((k) => ({ ...k, elevenlabs_key: v }))}
          placeholder="sk_..."
          required
          docsUrl="https://elevenlabs.io/app/settings/api-keys"
        />
      </div>

      {/* Cost summary */}
      <div className="bg-white/[0.02] border border-white/[0.06] rounded-lg p-4">
        <h4 className="text-xs text-gray-400 uppercase tracking-widest mb-2">Estimated Costs Per Video</h4>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <span className="text-gray-500">Script (DeepSeek)</span>
          <span className="text-gray-300 text-right">~$0.001</span>
          <span className="text-gray-500">Verification (Claude)</span>
          <span className="text-gray-300 text-right">~$0.60</span>
          <span className="text-gray-500">Lean Proof (Claude)</span>
          <span className="text-gray-300 text-right">~$0.10</span>
          <span className="text-gray-500">Narration (ElevenLabs)</span>
          <span className="text-gray-300 text-right">~$0.12–0.56</span>
          <span className="text-gray-500">Render + Delivery</span>
          <span className="text-gray-300 text-right">Free</span>
          <div className="col-span-2 border-t border-white/[0.06] mt-1 pt-1 flex justify-between">
            <span className="text-gray-400 font-medium">Total (Full AI + Lean)</span>
            <span className="text-white font-medium">~$0.82–1.26</span>
          </div>
          <div className="col-span-2 flex justify-between">
            <span className="text-gray-400 font-medium">Total (Teacher Verified)</span>
            <span className="text-white font-medium">~$0.12–0.56</span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={handleSave}
          disabled={saving}
          className="px-6 py-2.5 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium transition-all disabled:opacity-50"
        >
          {saving ? "Saving..." : "Save Keys"}
        </button>
        {saved && (
          <span className="text-sm text-green-400 flex items-center gap-1">
            ✓ Saved
          </span>
        )}
      </div>
    </div>
  );
}
