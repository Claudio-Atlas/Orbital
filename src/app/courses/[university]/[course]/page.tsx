import Link from "next/link";
import { notFound } from "next/navigation";
import { UNIVERSITIES } from "@/lib/constants";

// Sample course data - will be replaced with JSON content system
const COURSE_DATA: Record<string, Record<string, {
  name: string;
  title: string;
  description: string;
  videos: { id: string; title: string; topic: string; free: boolean }[];
  guides: { id: string; name: string; price: number }[];
}>> = {
  asu: {
    mat170: {
      name: "MAT170",
      title: "College Algebra",
      description: "Complete exam prep for ASU MAT170. Linear equations, systems, quadratics, and more.",
      videos: [
        { id: "linear-equations", title: "Solving Linear Equations", topic: "Exam 1", free: true },
        { id: "systems", title: "Systems of Equations", topic: "Exam 1", free: true },
        { id: "inequalities", title: "Linear Inequalities", topic: "Exam 1", free: false },
        { id: "factoring", title: "Factoring Quadratics", topic: "Exam 2", free: true },
        { id: "rational", title: "Rational Expressions", topic: "Exam 2", free: false },
      ],
      guides: [
        { id: "exam1", name: "Orbital Mini — MAT170 Exam 1", price: 2 },
        { id: "exam2", name: "Orbital Mini — MAT170 Exam 2", price: 2 },
        { id: "full", name: "Orbital Exam Pack — MAT170", price: 9 },
      ],
    },
  },
  gcu: {
    mat144: {
      name: "MAT144",
      title: "College Mathematics",
      description: "Complete exam prep for GCU MAT144. Budgeting, Excel, loans, and practical math.",
      videos: [
        { id: "percent-change", title: "Percent Change & Markup", topic: "Unit 1", free: true },
        { id: "budgeting", title: "Budgeting Models in Excel", topic: "Unit 1", free: true },
        { id: "loans", title: "Loan Amortization Tables", topic: "Unit 2", free: true },
      ],
      guides: [
        { id: "excel-lab", name: "Orbital Mini — MAT144 Excel Lab", price: 2 },
        { id: "full", name: "Orbital Exam Pack — MAT144", price: 9 },
      ],
    },
  },
};

interface PageProps {
  params: Promise<{
    university: string;
    course: string;
  }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { university, course } = await params;
  const courseData = COURSE_DATA[university]?.[course];
  const uni = UNIVERSITIES[university as keyof typeof UNIVERSITIES];
  
  if (!courseData || !uni) {
    return { title: "Course Not Found" };
  }

  return {
    title: `${courseData.name} Exam Prep — ${uni.shortName}`,
    description: courseData.description,
  };
}

export default async function CoursePage({ params }: PageProps) {
  const { university, course } = await params;
  const courseData = COURSE_DATA[university]?.[course];
  const uni = UNIVERSITIES[university as keyof typeof UNIVERSITIES];

  if (!courseData || !uni) {
    notFound();
  }

  const freeVideos = courseData.videos.filter((v) => v.free);
  const paidVideos = courseData.videos.filter((v) => !v.free);

  return (
    <>
      {/* Header */}
      <section className="section pb-8">
        <div className="container-wide">
          {/* Breadcrumb */}
          <nav className="flex items-center gap-2 text-small mb-8">
            <Link href="/courses" className="hover:text-white transition-colors">Courses</Link>
            <span className="text-gray-2">/</span>
            <Link href={`/courses/${university}`} className="hover:text-white transition-colors">{uni.shortName}</Link>
            <span className="text-gray-2">/</span>
            <span className="text-white">{courseData.name}</span>
          </nav>

          <div className="flex items-center gap-3 mb-4">
            <span className="badge badge-violet">{uni.shortName}</span>
            <span className="font-display text-xl font-semibold text-accent-violet">
              {courseData.name}
            </span>
          </div>
          
          <h1 className="heading-hero font-display mb-4">
            {courseData.title}
          </h1>
          
          <p className="text-body max-w-2xl">
            {courseData.description}
          </p>
        </div>
      </section>

      <div className="divider" />

      {/* Content Grid */}
      <section className="section">
        <div className="container-wide">
          <div className="grid lg:grid-cols-3 gap-10">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-12">
              {/* Free Videos */}
              <div>
                <div className="flex items-center gap-3 mb-6">
                  <h2 className="heading-section font-display">Free Videos</h2>
                  <span className="badge badge-green">FREE</span>
                </div>
                <div className="space-y-3">
                  {freeVideos.map((video) => (
                    <Link
                      key={video.id}
                      href={`/videos/${university}-${course}-${video.id}`}
                      className="card card-interactive flex items-center justify-between group"
                    >
                      <div>
                        <h3 className="heading-card group-hover:text-accent-violet transition-colors">
                          {video.title}
                        </h3>
                        <p className="text-small mt-1">{video.topic}</p>
                      </div>
                      <div className="flex items-center gap-2 text-accent-violet">
                        <span className="text-sm">Watch</span>
                        <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>

              {/* Premium Videos */}
              {paidVideos.length > 0 && (
                <div>
                  <div className="flex items-center gap-3 mb-6">
                    <h2 className="heading-section font-display">Premium Videos</h2>
                    <span className="badge badge-violet">WITH GUIDE</span>
                  </div>
                  <div className="space-y-3">
                    {paidVideos.map((video) => (
                      <div
                        key={video.id}
                        className="card flex items-center justify-between opacity-60"
                      >
                        <div>
                          <h3 className="heading-card">{video.title}</h3>
                          <p className="text-small mt-1">{video.topic}</p>
                        </div>
                        <span className="text-small">Included in guides</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Sidebar: Study Guides */}
            <aside>
              <div className="sticky top-24">
                <h2 className="heading-card mb-6">Study Guides</h2>
                <div className="space-y-4">
                  {courseData.guides.map((guide) => (
                    <div key={guide.id} className="card card-highlight">
                      <h3 className="font-medium mb-3">{guide.name}</h3>
                      <div className="flex items-center justify-between">
                        <span className="text-2xl font-bold text-accent-violet">
                          ${guide.price}
                        </span>
                        <button className="btn btn-primary text-sm py-2 px-4">
                          Get Now
                        </button>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-8 p-5 bg-white/[0.02] border border-white/[0.06] rounded-2xl">
                  <p className="text-small leading-relaxed">
                    <strong className="text-white block mb-1">Not sure?</strong>
                    Start with the free videos. Upgrade when you&apos;re ready for the full exam prep.
                  </p>
                </div>
              </div>
            </aside>
          </div>
        </div>
      </section>
    </>
  );
}
