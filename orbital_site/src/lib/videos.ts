// Video types matching VideoFactory output
export interface VideoMetadata {
  id: string;
  brand: "Orbital";
  title: string;
  course: string;
  university: string;
  topic: string;
  exam?: string;
  product_family: "core" | "mini" | "review" | "drill" | "exam_pack" | "final_sprint";
  duration: string;
  free: boolean;
  seo_title: string;
  seo_description: string;
  transcript?: string;
  // Video source - either self-hosted MP4 or YouTube
  video_url?: string;      // Self-hosted MP4 URL (from VideoFactory)
  youtube_id?: string;     // YouTube ID (for manually uploaded content)
  thumbnail_url?: string;
}

// Sample videos - will be replaced with JSON files from VideoFactory
export const SAMPLE_VIDEOS: VideoMetadata[] = [
  {
    id: "asu-mat170-linear-equations",
    brand: "Orbital",
    title: "Solving Linear Equations",
    course: "MAT170",
    university: "ASU",
    topic: "Exam 1",
    product_family: "core",
    duration: "8:24",
    free: true,
    seo_title: "MAT170 Linear Equations - ASU Exam Prep",
    seo_description: "Step-by-step walkthrough of linear equations for ASU MAT170 Exam 1.",
  },
  {
    id: "asu-mat170-systems",
    brand: "Orbital",
    title: "Systems of Equations",
    course: "MAT170",
    university: "ASU",
    topic: "Exam 1",
    product_family: "core",
    duration: "12:15",
    free: true,
    seo_title: "MAT170 Systems of Equations - ASU Exam Prep",
    seo_description: "Step-by-step walkthrough of systems of equations for ASU MAT170 Exam 1.",
  },
  {
    id: "gcu-mat144-percent-change",
    brand: "Orbital",
    title: "Percent Change & Markup",
    course: "MAT144",
    university: "GCU",
    topic: "Unit 1",
    product_family: "core",
    duration: "6:42",
    free: true,
    seo_title: "MAT144 Percent Change - GCU Exam Prep",
    seo_description: "Step-by-step walkthrough of percent change and markup for GCU MAT144.",
  },
  {
    id: "gcu-mat144-budgeting",
    brand: "Orbital",
    title: "Budgeting Models in Excel",
    course: "MAT144",
    university: "GCU",
    topic: "Unit 1",
    product_family: "core",
    duration: "15:30",
    free: true,
    seo_title: "MAT144 Excel Budgeting - GCU Exam Prep",
    seo_description: "Step-by-step walkthrough of budgeting models in Excel for GCU MAT144.",
  },
  {
    id: "asu-mat170-factoring",
    brand: "Orbital",
    title: "Factoring Quadratics",
    course: "MAT170",
    university: "ASU",
    topic: "Exam 2",
    product_family: "core",
    duration: "10:18",
    free: true,
    seo_title: "MAT170 Factoring Quadratics - ASU Exam Prep",
    seo_description: "Step-by-step walkthrough of factoring quadratics for ASU MAT170 Exam 2.",
  },
  {
    id: "gcu-mat144-loans",
    brand: "Orbital",
    title: "Loan Amortization Tables",
    course: "MAT144",
    university: "GCU",
    topic: "Unit 2",
    product_family: "core",
    duration: "11:45",
    free: true,
    seo_title: "MAT144 Loan Amortization - GCU Exam Prep",
    seo_description: "Step-by-step walkthrough of loan amortization tables for GCU MAT144.",
  },
];

// Helper to get video source URL
export function getVideoSource(video: VideoMetadata): { type: 'mp4' | 'youtube'; src: string } | null {
  if (video.video_url) {
    return { type: 'mp4', src: video.video_url };
  }
  if (video.youtube_id) {
    return { type: 'youtube', src: `https://www.youtube.com/embed/${video.youtube_id}` };
  }
  return null;
}

// Filter videos by university/course
export function filterVideos(
  videos: VideoMetadata[],
  filters: { university?: string; course?: string; free?: boolean }
): VideoMetadata[] {
  return videos.filter((v) => {
    if (filters.university && v.university.toLowerCase() !== filters.university.toLowerCase()) return false;
    if (filters.course && v.course.toLowerCase() !== filters.course.toLowerCase()) return false;
    if (filters.free !== undefined && v.free !== filters.free) return false;
    return true;
  });
}
