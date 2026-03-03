"use client";

export type PipelinePath = "full_ai" | "ai_review" | "professor_source";

interface PathSelectorProps {
  selected: PipelinePath | null;
  onSelect: (path: PipelinePath) => void;
}

const PATHS = [
  {
    key: "full_ai" as PipelinePath,
    icon: "🤖",
    title: "Let AI solve it",
    desc: "Type a problem. AI generates the full solution, verifies it, and renders the video.",
    cost: "~$0.72–1.26",
    badge: "AI / Lean Verified",
    badgeColor: "text-cyan-400 bg-cyan-500/10",
  },
  {
    key: "ai_review" as PipelinePath,
    icon: "✏️",
    title: "AI draft, I'll review",
    desc: "AI writes the script. You review and edit every step before rendering.",
    cost: "~$0.12–0.56",
    badge: "Teacher Verified",
    badgeColor: "text-amber-400 bg-amber-500/10",
  },
  {
    key: "professor_source" as PipelinePath,
    icon: "📝",
    title: "I'll provide my solution",
    desc: "Type your steps or upload a photo of your work. We turn it into a polished video.",
    cost: "~$0.12–0.62",
    badge: "Teacher Verified",
    badgeColor: "text-amber-400 bg-amber-500/10",
  },
];

export function PathSelector({ selected, onSelect }: PathSelectorProps) {
  return (
    <div className="space-y-3">
      <label className="block text-xs font-medium uppercase tracking-widest text-gray-500 mb-3">
        How do you want to create this video?
      </label>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {PATHS.map((path) => (
          <button
            key={path.key}
            onClick={() => onSelect(path.key)}
            className={`p-5 rounded-xl border text-left transition-all ${
              selected === path.key
                ? "border-violet-500/50 bg-violet-500/10"
                : "border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.04]"
            }`}
          >
            <div className="text-2xl mb-2">{path.icon}</div>
            <h3
              className={`font-medium mb-1 ${
                selected === path.key ? "text-violet-300" : "text-white"
              }`}
            >
              {path.title}
            </h3>
            <p className="text-xs text-gray-500 mb-3 leading-relaxed">{path.desc}</p>
            <div className="flex items-center justify-between">
              <span className="text-[10px] text-gray-600">{path.cost}</span>
              <span className={`text-[10px] px-2 py-0.5 rounded-full ${path.badgeColor}`}>
                {path.badge}
              </span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
