import Link from "next/link";
import { SITE, UNIVERSITIES, PRODUCT_FAMILIES } from "@/lib/constants";

export default function HomePage() {
  return (
    <>
      {/* Hero Section */}
      <section className="section-lg relative overflow-hidden">
        {/* Subtle glow */}
        <div className="glow-orb -top-64 left-1/2 -translate-x-1/2" />
        
        <div className="container-tight relative flex flex-col items-center">
          <div className="badge badge-violet mb-10">
            Now serving ASU &amp; GCU students
          </div>
          
          <h1 className="heading-hero font-display mb-10" style={{ textAlign: 'center' }}>
            Precision prep<br />for STEM.
          </h1>
          
          <p className="text-lg text-[var(--gray-1)] leading-relaxed max-w-2xl" style={{ textAlign: 'center' }}>
            Course-specific walkthroughs built for your actual exams.
            <br />
            Free videos to get started, $2 guides when you need more.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-5 justify-center items-center" style={{ marginTop: '3rem' }}>
            <Link href="/courses" className="btn btn-primary btn-lg min-w-[200px]">
              Find your course
            </Link>
            <Link href="/videos" className="btn btn-secondary btn-lg min-w-[200px]">
              Watch free videos
            </Link>
          </div>
        </div>
      </section>

      {/* Social proof / trust bar */}
      <div className="divider" />
      <section className="py-8">
        <div className="container-wide">
          <p className="text-center text-small">
            Built by educators • Not affiliated with any university • Focused on learning
          </p>
        </div>
      </section>
      <div className="divider" />

      {/* How It Works */}
      <section className="section">
        <div className="container-tight">
          <div className="flex flex-col items-center mb-12">
            <h2 className="heading-section font-display mb-4" style={{ textAlign: 'center' }}>How it works</h2>
            <p className="text-lg text-[var(--gray-1)] leading-relaxed max-w-lg" style={{ textAlign: 'center' }}>
              Five minutes from now, you could be learning.
            </p>
          </div>
          
          <div className="flex flex-col gap-6 max-w-xl mx-auto">
            {[
              { step: "1", title: "Pick your university", desc: "We organize everything by school so you find exactly what matches your course." },
              { step: "2", title: "Choose your course", desc: "MAT144, PHY101, CHM130 — we cover the courses you're actually taking." },
              { step: "3", title: "Watch free walkthroughs", desc: "Step-by-step video solutions for problems that look like your homework." },
              { step: "4", title: "Grab a study guide", desc: "$2 Minis give you focused prep. $9 Exam Packs cover everything." },
            ].map((item, idx) => (
              <div 
                key={item.step} 
                className="flex gap-4 items-start"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <div className="step-number">{item.step}</div>
                <div>
                  <h3 className="heading-card mb-2">{item.title}</h3>
                  <p className="text-small leading-relaxed">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* What You Get */}
      <section className="section section-elevated section-border-t">
        <div className="container-wide flex flex-col items-center">
          <div className="flex flex-col items-center mb-12">
            <h2 className="heading-section font-display mb-4" style={{ textAlign: 'center' }}>What you get</h2>
            <p className="text-lg text-[var(--gray-1)] leading-relaxed max-w-lg" style={{ textAlign: 'center' }}>
              Start free. Pay only when you need focused prep.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl w-full">
            {/* Free */}
            <div className="card" style={{ borderColor: 'rgba(34, 197, 94, 0.3)', background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.05) 0%, transparent 50%)' }}>
              <div className="badge badge-green mb-5">Free forever</div>
              <h3 className="heading-card mb-4">Core Content</h3>
              <ul className="space-y-3">
                {[
                  "Walkthrough videos",
                  "Practice problem sets",
                  "Step-by-step solutions",
                  "Course topic guides",
                ].map((item) => (
                  <li key={item} className="flex items-center gap-3 text-gray-1">
                    <svg className="w-5 h-5 text-green-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            {/* Paid */}
            <div className="card card-highlight">
              <div className="badge badge-violet mb-5">From $2</div>
              <h3 className="heading-card mb-4">Premium Guides</h3>
              <ul className="space-y-3">
                {[
                  { name: PRODUCT_FAMILIES.mini.name, price: "$2" },
                  { name: PRODUCT_FAMILIES.examPack.name, price: "$9" },
                  { name: PRODUCT_FAMILIES.finalSprint.name, price: "$9" },
                  { name: PRODUCT_FAMILIES.vault.name, price: "$19/mo" },
                ].map((item) => (
                  <li key={item.name} className="flex items-center justify-between text-gray-1">
                    <span className="flex items-center gap-3">
                      <svg className="w-5 h-5 text-accent-violet flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      {item.name}
                    </span>
                    <span className="text-small">{item.price}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Universities */}
      <section className="section section-border-t">
        <div className="container-tight">
          <div className="flex flex-col items-center mb-12">
            <h2 className="heading-section font-display mb-4" style={{ textAlign: 'center' }}>Schools we support</h2>
            <p className="text-lg text-[var(--gray-1)] leading-relaxed" style={{ textAlign: 'center' }}>
              More universities coming soon.
            </p>
          </div>
          
          <div className="grid sm:grid-cols-2 gap-5 max-w-2xl mx-auto">
            {Object.values(UNIVERSITIES).map((uni) => (
              <Link
                key={uni.id}
                href={`/courses/${uni.id}`}
                className="card card-interactive group"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="heading-card group-hover:text-accent-violet transition-colors">
                      {uni.shortName}
                    </h3>
                    <p className="text-small mt-1">{uni.name}</p>
                  </div>
                  <svg 
                    className="w-5 h-5 text-gray-2 group-hover:text-accent-violet group-hover:translate-x-1 transition-all" 
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
        </div>
      </section>

      {/* CTA */}
      <section className="section-lg section-elevated section-border-t">
        <div className="container-tight flex flex-col items-center">
          <h2 className="heading-section font-display mb-4" style={{ textAlign: 'center' }}>
            Ready to start?
          </h2>
          <p className="text-lg text-[var(--gray-1)] leading-relaxed max-w-md mb-8" style={{ textAlign: 'center' }}>
            Find your course and start learning with free videos.
            <br />
            Upgrade when you need focused exam prep.
          </p>
          <Link href="/courses" className="btn btn-primary btn-lg">
            Find your course
          </Link>
        </div>
      </section>
    </>
  );
}
