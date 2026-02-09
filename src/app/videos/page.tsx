import Link from "next/link";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Videos",
  description: "Free STEM walkthrough videos. Step-by-step solutions for your actual course problems.",
};

// Sample video data
const FEATURED_VIDEOS = [
  {
    id: "asu-mat170-linear-equations",
    title: "Solving Linear Equations",
    course: "MAT170",
    university: "ASU",
    topic: "Exam 1",
    duration: "8:24",
  },
  {
    id: "asu-mat170-systems",
    title: "Systems of Equations",
    course: "MAT170",
    university: "ASU",
    topic: "Exam 1",
    duration: "12:15",
  },
  {
    id: "gcu-mat144-percent-change",
    title: "Percent Change & Markup",
    course: "MAT144",
    university: "GCU",
    topic: "Unit 1",
    duration: "6:42",
  },
  {
    id: "gcu-mat144-budgeting",
    title: "Budgeting Models in Excel",
    course: "MAT144",
    university: "GCU",
    topic: "Unit 1",
    duration: "15:30",
  },
  {
    id: "asu-mat170-factoring",
    title: "Factoring Quadratics",
    course: "MAT170",
    university: "ASU",
    topic: "Exam 2",
    duration: "10:18",
  },
  {
    id: "gcu-mat144-loans",
    title: "Loan Amortization Tables",
    course: "MAT144",
    university: "GCU",
    topic: "Unit 2",
    duration: "11:45",
  },
];

export default function VideosPage() {
  return (
    <>
      {/* Hero */}
      <section className="section relative overflow-hidden">
        <div className="glow-orb -top-64 left-1/2 -translate-x-1/2" />
        
        <div className="container-tight relative flex flex-col items-center">
          <div className="badge badge-green mb-6">All free</div>
          
          <h1 className="heading-hero font-display mb-6" style={{ textAlign: 'center' }}>
            Walkthrough videos
          </h1>
          
          <p className="text-lg text-[var(--gray-1)] leading-relaxed max-w-lg" style={{ textAlign: 'center' }}>
            Step-by-step solutions for problems that look like your homework and exams.
          </p>
        </div>
      </section>

      <div className="divider" />

      {/* Video Grid */}
      <section className="section">
        <div className="container-wide">
          <div className="flex items-center justify-between mb-8">
            <h2 className="heading-section font-display">Featured Videos</h2>
            <Link href="/courses" className="btn btn-ghost">
              Browse by course →
            </Link>
          </div>
          
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {FEATURED_VIDEOS.map((video) => (
              <Link
                key={video.id}
                href={`/videos/${video.id}`}
                className="card card-interactive group"
              >
                {/* Thumbnail placeholder */}
                <div className="aspect-video bg-white/[0.03] rounded-lg mb-4 flex items-center justify-center border border-white/[0.06] group-hover:border-accent-violet/30 transition-colors">
                  <div className="w-12 h-12 rounded-full bg-accent-violet/20 flex items-center justify-center group-hover:bg-accent-violet/30 transition-colors">
                    <svg className="w-5 h-5 text-accent-violet ml-0.5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M8 5v14l11-7z"/>
                    </svg>
                  </div>
                </div>
                
                <div className="flex items-center gap-2 mb-2">
                  <span className="badge text-xs">{video.university}</span>
                  <span className="text-small">{video.course}</span>
                </div>
                
                <h3 className="heading-card group-hover:text-accent-violet transition-colors mb-1">
                  {video.title}
                </h3>
                
                <div className="flex items-center justify-between text-small">
                  <span>{video.topic}</span>
                  <span>{video.duration}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section section-elevated section-border-t">
        <div className="container-tight flex flex-col items-center">
          <h2 className="heading-section font-display mb-4" style={{ textAlign: 'center' }}>
            Find videos for your course
          </h2>
          <p className="text-lg text-[var(--gray-1)] leading-relaxed max-w-md mb-8" style={{ textAlign: 'center' }}>
            Browse by university and course to find walkthroughs that match your actual exams.
          </p>
          <Link href="/courses" className="btn btn-primary btn-lg">
            Browse courses
          </Link>
        </div>
      </section>
    </>
  );
}
