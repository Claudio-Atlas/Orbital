"use client";

import { useState } from "react";

export interface CourseVideo {
  id: string;
  problem: string;
  duration: number | null;
  badge: "lean4_verified" | "ai_verified" | "teacher_verified";
  youtubeId: string | null;
  tags: string[];
}

export interface Course {
  id: string;
  name: string;
  description: string;
  visibility: "unlisted" | "public";
  videos: CourseVideo[];
  youtubePlaylistId: string | null;
  createdAt: string;
  updatedAt: string;
  viewCount: number;
}

const BADGE_LABELS: Record<string, { icon: string; color: string }> = {
  lean4_verified: { icon: "🏛️", color: "text-cyan-400" },
  ai_verified: { icon: "✅", color: "text-green-400" },
  teacher_verified: { icon: "👨‍🏫", color: "text-amber-400" },
};

function formatDuration(seconds: number | null): string {
  if (!seconds) return "--:--";
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

// ─── Tag Input ───

function TagInput({
  tags,
  onChange,
  suggestions,
}: {
  tags: string[];
  onChange: (tags: string[]) => void;
  suggestions?: string[];
}) {
  const [input, setInput] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);

  const addTag = (tag: string) => {
    const t = tag.trim().toLowerCase();
    if (t && !tags.includes(t)) {
      onChange([...tags, t]);
    }
    setInput("");
    setShowSuggestions(false);
  };

  const removeTag = (tag: string) => {
    onChange(tags.filter((t) => t !== tag));
  };

  const filtered = suggestions?.filter(
    (s) => s.toLowerCase().includes(input.toLowerCase()) && !tags.includes(s)
  );

  return (
    <div className="relative">
      <div className="flex flex-wrap gap-1.5 p-2 rounded-lg bg-black/40 border border-white/[0.08] min-h-[38px]">
        {tags.map((tag) => (
          <span
            key={tag}
            className="flex items-center gap-1 px-2 py-0.5 rounded-md bg-violet-500/15 text-violet-300 text-xs"
          >
            {tag}
            <button
              onClick={() => removeTag(tag)}
              className="text-violet-400/50 hover:text-violet-300 transition-colors"
            >
              ×
            </button>
          </span>
        ))}
        <input
          type="text"
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            setShowSuggestions(true);
          }}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === ",") {
              e.preventDefault();
              addTag(input);
            }
            if (e.key === "Backspace" && !input && tags.length > 0) {
              removeTag(tags[tags.length - 1]);
            }
          }}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
          placeholder={tags.length === 0 ? "Add tags (press Enter)..." : ""}
          className="flex-1 min-w-[120px] bg-transparent text-white/90 text-sm outline-none placeholder-gray-600"
        />
      </div>
      {showSuggestions && filtered && filtered.length > 0 && input && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-gray-900 border border-white/[0.1] rounded-lg overflow-hidden z-10">
          {filtered.slice(0, 6).map((s) => (
            <button
              key={s}
              onMouseDown={() => addTag(s)}
              className="w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-violet-500/10 hover:text-violet-300 transition-colors"
            >
              {s}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

// ─── Course Card ───

function CourseCard({
  course,
  onOpen,
}: {
  course: Course;
  onOpen: () => void;
}) {
  const totalDuration = course.videos.reduce((sum, v) => sum + (v.duration || 0), 0);

  return (
    <div
      onClick={onOpen}
      className="bg-white/[0.03] border border-white/[0.08] rounded-xl p-5 hover:bg-white/[0.05] transition-all cursor-pointer"
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-medium text-white">{course.name}</h3>
          {course.description && (
            <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">{course.description}</p>
          )}
        </div>
        <span
          className={`text-[10px] px-2 py-0.5 rounded-full ${
            course.visibility === "public"
              ? "bg-green-500/10 text-green-400"
              : "bg-gray-500/10 text-gray-400"
          }`}
        >
          {course.visibility === "public" ? "Public" : "Unlisted"}
        </span>
      </div>
      <div className="flex items-center gap-3 text-xs text-gray-500">
        <span>{course.videos.length} video{course.videos.length !== 1 ? "s" : ""}</span>
        <span>•</span>
        <span>{formatDuration(totalDuration)}</span>
        {course.visibility === "public" && course.viewCount > 0 && (
          <>
            <span>•</span>
            <span>{course.viewCount.toLocaleString()} views</span>
          </>
        )}
        <span>•</span>
        <span>Updated {new Date(course.updatedAt).toLocaleDateString()}</span>
      </div>
    </div>
  );
}

// ─── Course Detail ───

function CourseDetail({
  course,
  availableVideos,
  onBack,
  onUpdate,
  onAddVideo,
  onRemoveVideo,
  onReorder,
}: {
  course: Course;
  availableVideos: CourseVideo[];
  onBack: () => void;
  onUpdate: (updates: Partial<Course>) => void;
  onAddVideo: (videoId: string) => void;
  onRemoveVideo: (videoId: string) => void;
  onReorder: (videoId: string, direction: -1 | 1) => void;
}) {
  const [showAddVideo, setShowAddVideo] = useState(false);
  const [editName, setEditName] = useState(false);
  const [name, setName] = useState(course.name);
  const [description, setDescription] = useState(course.description);
  const [copied, setCopied] = useState<string | null>(null);

  const courseVideoIds = new Set(course.videos.map((v) => v.id));
  const addableVideos = availableVideos.filter((v) => !courseVideoIds.has(v.id));

  const shareUrl = `orbitalsolver.io/course/${course.id}`;
  const youtubeUrl = course.youtubePlaylistId
    ? `youtube.com/playlist?list=${course.youtubePlaylistId}`
    : null;
  const embedCode = course.youtubePlaylistId
    ? `<iframe width="560" height="315" src="https://www.youtube.com/embed/videoseries?list=${course.youtubePlaylistId}" frameborder="0" allowfullscreen></iframe>`
    : `<iframe width="560" height="315" src="https://orbitalsolver.io/embed/course/${course.id}" frameborder="0" allowfullscreen></iframe>`;

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopied(label);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <button
          onClick={onBack}
          className="text-sm text-gray-500 hover:text-gray-300 transition-colors mb-3 flex items-center gap-1"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
          All Courses
        </button>

        <div className="flex items-start justify-between">
          <div className="flex-1">
            {editName ? (
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                onBlur={() => {
                  setEditName(false);
                  if (name.trim() !== course.name) onUpdate({ name: name.trim() });
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    setEditName(false);
                    if (name.trim() !== course.name) onUpdate({ name: name.trim() });
                  }
                }}
                autoFocus
                className="text-xl font-semibold bg-transparent text-white border-b border-violet-500 outline-none w-full"
              />
            ) : (
              <h2
                onClick={() => setEditName(true)}
                className="text-xl font-semibold text-white cursor-pointer hover:text-violet-300 transition-colors"
                title="Click to edit"
              >
                {course.name}
              </h2>
            )}
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              onBlur={() => {
                if (description !== course.description) onUpdate({ description });
              }}
              placeholder="Add a course description..."
              rows={1}
              className="w-full mt-1 bg-transparent text-sm text-gray-500 outline-none resize-none placeholder-gray-700"
            />
          </div>

          {/* Visibility toggle */}
          <div className="flex items-center gap-2 ml-4">
            <button
              onClick={() =>
                onUpdate({
                  visibility: course.visibility === "unlisted" ? "public" : "unlisted",
                })
              }
              className={`text-xs px-3 py-1.5 rounded-lg border transition-all ${
                course.visibility === "public"
                  ? "border-green-500/30 bg-green-500/10 text-green-400"
                  : "border-white/[0.1] bg-white/[0.03] text-gray-400"
              }`}
            >
              {course.visibility === "public" ? "🌍 Public" : "🔒 Unlisted"}
            </button>
          </div>
        </div>
      </div>

      {/* Share bar */}
      <div className="bg-white/[0.03] border border-white/[0.08] rounded-xl p-4">
        <label className="block text-[10px] uppercase tracking-widest text-gray-600 mb-3">
          Share
        </label>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => copyToClipboard(shareUrl, "link")}
            className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/[0.05] border border-white/[0.08] text-sm text-gray-300 hover:text-white hover:border-violet-500/30 transition-all"
          >
            🔗 {copied === "link" ? "Copied!" : "Share Link"}
          </button>
          <button
            onClick={() => copyToClipboard(embedCode, "embed")}
            className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/[0.05] border border-white/[0.08] text-sm text-gray-300 hover:text-white hover:border-violet-500/30 transition-all"
          >
            📋 {copied === "embed" ? "Copied!" : "LMS Embed Code"}
          </button>
          {youtubeUrl && (
            <button
              onClick={() => copyToClipboard(youtubeUrl, "youtube")}
              className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/[0.05] border border-white/[0.08] text-sm text-gray-300 hover:text-white hover:border-violet-500/30 transition-all"
            >
              ▶️ {copied === "youtube" ? "Copied!" : "YouTube Playlist"}
            </button>
          )}
        </div>
      </div>

      {/* Video list */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-medium text-gray-400 uppercase tracking-widest">
            Videos ({course.videos.length})
          </h3>
          <button
            onClick={() => setShowAddVideo(!showAddVideo)}
            className="text-sm text-violet-400 hover:text-violet-300 transition-colors"
          >
            + Add Video
          </button>
        </div>

        {course.videos.length === 0 ? (
          <div className="bg-white/[0.02] border border-dashed border-white/[0.08] rounded-xl p-8 text-center">
            <p className="text-gray-500 text-sm">No videos in this course yet.</p>
            <button
              onClick={() => setShowAddVideo(true)}
              className="mt-2 text-sm text-violet-400 hover:text-violet-300 transition-colors"
            >
              + Add your first video
            </button>
          </div>
        ) : (
          <div className="space-y-2">
            {course.videos.map((video, i) => (
              <div
                key={video.id}
                className="flex items-center gap-3 bg-white/[0.02] border border-white/[0.06] rounded-lg px-4 py-3 group"
              >
                <span className="text-xs text-gray-600 font-mono w-6 text-right">{i + 1}.</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-white truncate">{video.problem}</p>
                  <div className="flex items-center gap-2 mt-0.5">
                    {video.tags.slice(0, 3).map((tag) => (
                      <span key={tag} className="text-[10px] text-violet-400/60 bg-violet-500/5 px-1.5 py-0.5 rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
                <span className="text-xs text-gray-500">{formatDuration(video.duration)}</span>
                <span className={`text-sm ${BADGE_LABELS[video.badge].color}`}>
                  {BADGE_LABELS[video.badge].icon}
                </span>
                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    onClick={() => onReorder(video.id, -1)}
                    disabled={i === 0}
                    className="p-1 text-gray-600 hover:text-gray-300 disabled:opacity-20"
                  >
                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5" />
                    </svg>
                  </button>
                  <button
                    onClick={() => onReorder(video.id, 1)}
                    disabled={i === course.videos.length - 1}
                    className="p-1 text-gray-600 hover:text-gray-300 disabled:opacity-20"
                  >
                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                    </svg>
                  </button>
                  <button
                    onClick={() => onRemoveVideo(video.id)}
                    className="p-1 text-gray-600 hover:text-red-400"
                  >
                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Add video panel */}
        {showAddVideo && (
          <div className="mt-3 bg-white/[0.03] border border-white/[0.08] rounded-xl p-4">
            <h4 className="text-xs text-gray-400 uppercase tracking-widest mb-3">
              Add from your library
            </h4>
            {addableVideos.length === 0 ? (
              <p className="text-sm text-gray-500">
                All your videos are already in this course, or you haven&apos;t generated any yet.
              </p>
            ) : (
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {addableVideos.map((video) => (
                  <button
                    key={video.id}
                    onClick={() => {
                      onAddVideo(video.id);
                      if (addableVideos.length <= 1) setShowAddVideo(false);
                    }}
                    className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left hover:bg-violet-500/5 transition-colors"
                  >
                    <span className={`text-sm ${BADGE_LABELS[video.badge].color}`}>
                      {BADGE_LABELS[video.badge].icon}
                    </span>
                    <span className="text-sm text-gray-300 flex-1 truncate">{video.problem}</span>
                    <span className="text-xs text-gray-600">{formatDuration(video.duration)}</span>
                    <span className="text-xs text-violet-400">+ Add</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Main CourseBuilder ───

interface CourseBuilderProps {
  videos: CourseVideo[];
  tagSuggestions?: string[];
}

// Mock data
const MOCK_VIDEOS: CourseVideo[] = [
  { id: "v1", problem: "Find the area between y = x + 2 and y = x²", duration: 232, badge: "lean4_verified", youtubeId: "Eb3NeavCyLY", tags: ["calculus", "integration", "area"] },
  { id: "v2", problem: "Prove the group of order 15 is cyclic", duration: 287, badge: "lean4_verified", youtubeId: "USmfu88O0ew", tags: ["abstract algebra", "group theory", "proof"] },
  { id: "v3", problem: "Prove the reals are uncountable (Dedekind cuts)", duration: 194, badge: "ai_verified", youtubeId: "x1fx09DyKx4", tags: ["analysis", "set theory", "proof"] },
  { id: "v4", problem: "Find the derivative of f(x) = x³ - 6x² + 9x + 1", duration: 180, badge: "teacher_verified", youtubeId: null, tags: ["calculus", "derivatives", "power rule"] },
  { id: "v5", problem: "Solve the system: 2x + 3y = 7, x - y = 1", duration: 150, badge: "teacher_verified", youtubeId: null, tags: ["algebra", "systems", "substitution"] },
];

const TAG_SUGGESTIONS = [
  "calculus", "precalculus", "algebra", "trigonometry", "statistics",
  "derivatives", "integration", "limits", "series", "sequences",
  "proof", "abstract algebra", "linear algebra", "differential equations",
  "midterm review", "final review", "homework", "practice",
  "power rule", "chain rule", "product rule", "quotient rule",
  "area", "volume", "optimization", "related rates",
];

export function CourseBuilder({ videos = MOCK_VIDEOS, tagSuggestions = TAG_SUGGESTIONS }: CourseBuilderProps) {
  const [courses, setCourses] = useState<Course[]>([
    {
      id: "c1",
      name: "Calculus 1 — Fall 2026",
      description: "Complete video walkthrough of Calc 1 topics",
      visibility: "unlisted",
      videos: [MOCK_VIDEOS[0], MOCK_VIDEOS[3]],
      youtubePlaylistId: "PLmock123",
      createdAt: "2026-03-01T00:00:00Z",
      updatedAt: "2026-03-02T00:00:00Z",
      viewCount: 0,
    },
  ]);
  const [selectedCourseId, setSelectedCourseId] = useState<string | null>(null);
  const [showNewCourse, setShowNewCourse] = useState(false);
  const [newCourseName, setNewCourseName] = useState("");

  const selectedCourse = courses.find((c) => c.id === selectedCourseId);

  const createCourse = () => {
    if (!newCourseName.trim()) return;
    const newCourse: Course = {
      id: crypto.randomUUID(),
      name: newCourseName.trim(),
      description: "",
      visibility: "unlisted",
      videos: [],
      youtubePlaylistId: null,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      viewCount: 0,
    };
    setCourses((prev) => [...prev, newCourse]);
    setNewCourseName("");
    setShowNewCourse(false);
    setSelectedCourseId(newCourse.id);
  };

  const updateCourse = (courseId: string, updates: Partial<Course>) => {
    setCourses((prev) =>
      prev.map((c) =>
        c.id === courseId ? { ...c, ...updates, updatedAt: new Date().toISOString() } : c
      )
    );
  };

  const addVideoToCourse = (courseId: string, videoId: string) => {
    const video = MOCK_VIDEOS.find((v) => v.id === videoId);
    if (!video) return;
    setCourses((prev) =>
      prev.map((c) =>
        c.id === courseId
          ? { ...c, videos: [...c.videos, video], updatedAt: new Date().toISOString() }
          : c
      )
    );
  };

  const removeVideoFromCourse = (courseId: string, videoId: string) => {
    setCourses((prev) =>
      prev.map((c) =>
        c.id === courseId
          ? { ...c, videos: c.videos.filter((v) => v.id !== videoId), updatedAt: new Date().toISOString() }
          : c
      )
    );
  };

  const reorderVideo = (courseId: string, videoId: string, direction: -1 | 1) => {
    setCourses((prev) =>
      prev.map((c) => {
        if (c.id !== courseId) return c;
        const idx = c.videos.findIndex((v) => v.id === videoId);
        if (idx < 0) return c;
        const newIdx = idx + direction;
        if (newIdx < 0 || newIdx >= c.videos.length) return c;
        const newVideos = [...c.videos];
        [newVideos[idx], newVideos[newIdx]] = [newVideos[newIdx], newVideos[idx]];
        return { ...c, videos: newVideos, updatedAt: new Date().toISOString() };
      })
    );
  };

  // Course detail view
  if (selectedCourse) {
    return (
      <CourseDetail
        course={selectedCourse}
        availableVideos={MOCK_VIDEOS}
        onBack={() => setSelectedCourseId(null)}
        onUpdate={(updates) => updateCourse(selectedCourse.id, updates)}
        onAddVideo={(videoId) => addVideoToCourse(selectedCourse.id, videoId)}
        onRemoveVideo={(videoId) => removeVideoFromCourse(selectedCourse.id, videoId)}
        onReorder={(videoId, dir) => reorderVideo(selectedCourse.id, videoId, dir)}
      />
    );
  }

  // Course list view
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Courses</h2>
        <button
          onClick={() => setShowNewCourse(true)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium transition-all"
        >
          + New Course
        </button>
      </div>

      {/* New course form */}
      {showNewCourse && (
        <div className="bg-white/[0.03] border border-violet-500/30 rounded-xl p-4 flex items-center gap-3">
          <input
            type="text"
            value={newCourseName}
            onChange={(e) => setNewCourseName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && createCourse()}
            placeholder="Course name (e.g., Calculus 1 — Fall 2026)"
            autoFocus
            className="flex-1 px-3 py-2.5 rounded-lg bg-black/40 text-white text-sm border border-white/[0.08] focus:border-violet-500/50 focus:outline-none"
          />
          <button
            onClick={createCourse}
            disabled={!newCourseName.trim()}
            className="px-4 py-2.5 rounded-lg bg-violet-600 text-white text-sm font-medium disabled:opacity-40 transition-all"
          >
            Create
          </button>
          <button
            onClick={() => { setShowNewCourse(false); setNewCourseName(""); }}
            className="px-3 py-2.5 text-sm text-gray-500 hover:text-gray-300 transition-colors"
          >
            Cancel
          </button>
        </div>
      )}

      {/* Course cards */}
      {courses.length === 0 && !showNewCourse ? (
        <div className="bg-white/[0.02] border border-dashed border-white/[0.08] rounded-2xl p-12 text-center">
          <p className="text-gray-500 mb-2">No courses yet.</p>
          <p className="text-sm text-gray-600">
            Create a course to organize your videos into playlists that students can watch in order.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {courses.map((course) => (
            <CourseCard
              key={course.id}
              course={course}
              onOpen={() => setSelectedCourseId(course.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
