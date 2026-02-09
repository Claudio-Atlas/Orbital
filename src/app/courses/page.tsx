import Link from "next/link";
import { UNIVERSITIES } from "@/lib/constants";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Courses",
  description: "Find your university and course for step-by-step STEM exam prep.",
};

export default function CoursesPage() {
  return (
    <>
      {/* Hero */}
      <section className="section relative overflow-hidden">
        <div className="glow-orb -top-64 left-1/2 -translate-x-1/2" />
        
        <div className="container-tight relative flex flex-col items-center">
          <h1 className="heading-hero font-display mb-6" style={{ textAlign: 'center' }}>
            Find your course
          </h1>
          <p className="text-lg text-[var(--gray-1)] leading-relaxed max-w-lg" style={{ textAlign: 'center' }}>
            Select your university to see available courses and start learning.
          </p>
        </div>
      </section>

      <div className="divider" />

      {/* University Selection */}
      <section className="section">
        <div className="container-tight">
          <div className="grid gap-5">
            {Object.values(UNIVERSITIES).map((uni) => (
              <Link
                key={uni.id}
                href={`/courses/${uni.id}`}
                className="card card-interactive group p-6"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="heading-section font-display group-hover:text-accent-violet transition-colors">
                      {uni.shortName}
                    </h2>
                    <p className="text-body mt-1">{uni.name}</p>
                  </div>
                  <svg 
                    className="w-6 h-6 text-gray-2 group-hover:text-accent-violet group-hover:translate-x-1 transition-all" 
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
              Don&apos;t see your university?
            </p>
            <a 
              href="mailto:support@orbitallearning.org?subject=Request%20University"
              className="btn btn-secondary"
            >
              Request your school
            </a>
          </div>
        </div>
      </section>
    </>
  );
}
