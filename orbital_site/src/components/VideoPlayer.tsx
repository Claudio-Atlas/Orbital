"use client";

import { VideoMetadata, getVideoSource } from "@/lib/videos";

interface VideoPlayerProps {
  video: VideoMetadata;
  className?: string;
}

export function VideoPlayer({ video, className = "" }: VideoPlayerProps) {
  const source = getVideoSource(video);

  if (!source) {
    // Placeholder when no video source available
    return (
      <div className={`aspect-video bg-white/[0.03] rounded-lg flex items-center justify-center border border-white/[0.06] ${className}`}>
        <div className="text-center">
          <div className="w-16 h-16 rounded-full bg-accent-violet/20 flex items-center justify-center mx-auto mb-3">
            <svg className="w-7 h-7 text-accent-violet ml-1" fill="currentColor" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </div>
          <p className="text-small">Video coming soon</p>
        </div>
      </div>
    );
  }

  if (source.type === 'youtube') {
    return (
      <div className={`aspect-video rounded-lg overflow-hidden ${className}`}>
        <iframe
          src={source.src}
          title={video.title}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          className="w-full h-full"
        />
      </div>
    );
  }

  // Self-hosted MP4 player
  return (
    <div className={`aspect-video rounded-lg overflow-hidden bg-black ${className}`}>
      <video
        src={source.src}
        controls
        className="w-full h-full"
        poster={video.thumbnail_url}
      >
        <track kind="captions" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
}

// Thumbnail component for video cards
interface VideoThumbnailProps {
  video: VideoMetadata;
  className?: string;
}

export function VideoThumbnail({ video, className = "" }: VideoThumbnailProps) {
  return (
    <div className={`aspect-video bg-white/[0.03] rounded-lg flex items-center justify-center border border-white/[0.06] group-hover:border-accent-violet/30 transition-colors relative overflow-hidden ${className}`}>
      {video.thumbnail_url ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img 
          src={video.thumbnail_url} 
          alt={video.title}
          className="w-full h-full object-cover"
        />
      ) : null}
      
      {/* Play button overlay */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="w-12 h-12 rounded-full bg-accent-violet/20 flex items-center justify-center group-hover:bg-accent-violet/30 transition-colors backdrop-blur-sm">
          <svg className="w-5 h-5 text-accent-violet ml-0.5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z"/>
          </svg>
        </div>
      </div>
      
      {/* Duration badge */}
      <div className="absolute bottom-2 right-2 px-2 py-0.5 bg-black/80 rounded text-xs font-medium">
        {video.duration}
      </div>
    </div>
  );
}
