import Link from "next/link";
import { notFound } from "next/navigation";
import { UNIVERSITIES } from "@/lib/constants";
import { Metadata } from "next";

// Sample courses per university - will be replaced with JSON content system
const UNI_COURSES: Record<string, { id: string; name: string; title: string; description: string }[]> = {
  asu: [
    { id: "mat170", name: "MAT170", title: "College Algebra", description: "Linear equations, systems, quadratics, and polynomial functions." },
    { id: "mat210", name: "MAT210", title: "Brief Calculus", description: "Derivatives, integrals, and applications for business and life sciences." },
  ],
  gcu: [
    { id: "mat144", name: "MAT144", title: "College Mathematics", description: "Budgeting, Excel, loans, and practical quantitative reasoning." },
    { id: "mat261", name: "MAT261", title: "Applied Statistics", description: "Descriptive statistics, probability, and hypothesis testing." },
  ],
};

interface PageProps {
  params: Promise<{ university: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { university } = await params;
  const uni = UNIVERSITIES[university as keyof typeof UNIVERSITIES];
  
  if (!uni) {
    return { title: "University Not Found" };
  }

  return {
    title: `${uni.name} Courses`,
    description: `STEM exam prep for ${uni.shortName} students. Step-by-step walkthroughs and study guides.`,
  };
}

export default async function UniversityPage({ params }: PageProps) {
  const { university } = await params;
  const uni = UNIVERSITIES[university as keyof typeof UNIVERSITIES];
  const courses = UNI_COURSES[university];

  if (!uni || !courses) {
    notFound();
  }

  return (
    <>
      {/* Header */}
      <section className="section relative overflow-hidden">
        <div className="glow-orb -top-64 left-1/2 -translate-x-1/2" />
        
        <div className="container-tight relative flex flex-col items-center">
          {/* Breadcrumb */}
          <nav className="flex items-center gap-2 text-small mb-8">
            <Link href="/courses" className="hover:text-white transition-colors">Courses</Link>
            <span className="text-gray-2">/</span>
            <span className="text-white">{uni.shortName}</span>
          </nav>

          <h1 className="heading-hero font-display mb-4" style={{ textAlign: 'center' }}>
            {uni.shortName}
          </h1>
          <p className="text-lg text-[var(--gray-1)] leading-relaxed" style={{ textAlign: 'center' }}>
            {uni.name}
          </p>
        </div>
      </section>

      <div className="divider" />

      {/* Course List */}
      <section className="section">
        <div className="container-tight">
          <h2 className="heading-section font-display mb-8">Available Courses</h2>
          
          <div className="space-y-4">
            {courses.map((course) => (
              <Link
                key={course.id}
                href={`/courses/${university}/${course.id}`}
                className="card card-interactive group block"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <span className="font-display text-lg font-semibold text-accent-violet">
                        {course.name}
                      </span>
                    </div>
                    <h3 className="heading-card group-hover:text-accent-violet transition-colors mb-1">
                      {course.title}
                    </h3>
                    <p className="text-small">{course.description}</p>
                  </div>
                  <svg 
                    className="w-5 h-5 text-gray-2 group-hover:text-accent-violet group-hover:translate-x-1 transition-all flex-shrink-0 mt-1" 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </Link>
            ))}
          </div>

          <div className="mt-12 text-center">
            <p className="text-small mb-4">
              Course not listed?
            </p>
            <a 
              href={`mailto:support@orbitallearning.org?subject=Request%20${uni.shortName}%20Course`}
              className="btn btn-secondary"
            >
              Request a course
            </a>
          </div>
        </div>
      </section>
    </>
  );
}
