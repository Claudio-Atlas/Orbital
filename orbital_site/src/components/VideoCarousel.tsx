"use client";

import { useState } from "react";

interface VideoCarouselProps {
  isDark: boolean;
}

const videos = [
  {
    youtubeId: "Eb3NeavCyLY",
    title: "What is Orbital?",
    subtitle: "See the future of math education",
  },
  {
    youtubeId: "USmfu88O0ew",
    title: "Every Group of Order 15 is Cyclic",
    subtitle: "Abstract algebra proof — Sylow Theory",
  },
  {
    youtubeId: "x1fx09DyKx4",
    title: "The Reals are Uncountable",
    subtitle: "Real analysis proof — Dedekind's nested intervals",
  },
];

export function VideoCarousel({ isDark }: VideoCarouselProps) {
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Video container */}
      <div className="relative">
        {videos.map((video, index) => (
          <div
            key={video.youtubeId}
            className={index === activeIndex ? "block" : "hidden"}
          >
            <div
              className={`relative rounded-2xl overflow-hidden ${
                isDark
                  ? "border border-violet-500/30 shadow-[0_0_40px_rgba(139,92,246,0.2)]"
                  : "ring-1 ring-violet-300 shadow-[0_0_30px_rgba(139,92,246,0.12)]"
              }`}
            >
              <div className="relative w-full" style={{ paddingBottom: "56.25%" }}>
                <iframe
                  src={`https://www.youtube.com/embed/${video.youtubeId}?rel=0&modestbranding=1${index === 0 ? "&autoplay=1&mute=1" : ""}`}
                  title={video.title}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="absolute inset-0 w-full h-full"
                />
              </div>
            </div>

            {/* Title below video */}
            <div className="mt-4 text-center">
              <h3 className={`text-lg font-semibold ${isDark ? "text-white" : "text-gray-900"}`}>
                {video.title}
              </h3>
              <p className={`text-sm mt-1 ${isDark ? "text-gray-500" : "text-gray-500"}`}>
                {video.subtitle}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Dot navigation */}
      <div className="flex justify-center gap-2.5 mt-6">
        {videos.map((_, index) => (
          <button
            key={index}
            onClick={() => setActiveIndex(index)}
            className={`transition-all duration-300 rounded-full ${
              index === activeIndex
                ? "w-8 h-2.5 bg-violet-500"
                : `w-2.5 h-2.5 ${isDark ? "bg-white/20 hover:bg-white/40" : "bg-gray-300 hover:bg-gray-400"}`
            }`}
          />
        ))}
      </div>
    </div>
  );
}
