import Link from "next/link";
import { Metadata } from "next";
import { SITE } from "@/lib/constants";

export const metadata: Metadata = {
  title: "About",
  description: "Orbital Learning — precision STEM exam prep built by educators. Not affiliated with any university.",
};

export default function AboutPage() {
  return (
    <>
      {/* Hero */}
      <section className="section-lg relative overflow-hidden">
        <div className="glow-orb -top-64 left-1/2 -translate-x-1/2" />
        
        <div className="container-tight relative flex flex-col items-center">
          <h1 className="heading-hero font-display mb-6" style={{ textAlign: 'center' }}>
            About Orbital
          </h1>
          
          <p className="text-lg text-[var(--gray-1)] leading-relaxed max-w-2xl" style={{ textAlign: 'center' }}>
            We build exam prep that actually helps. Course-specific walkthroughs, 
            real problems, no fluff.
          </p>
        </div>
      </section>

      <div className="divider" />

      {/* Mission */}
      <section className="section">
        <div className="container-tight">
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <h2 className="heading-section font-display mb-6">Our approach</h2>
              <div className="space-y-4 text-body">
                <p>
                  Most study resources are too generic. They teach concepts but don&apos;t 
                  match what you actually see on your exams.
                </p>
                <p>
                  Orbital is different. We build content for specific courses at specific 
                  universities. When you study MAT144 at GCU, you get walkthroughs for 
                  problems that look like your homework.
                </p>
                <p>
                  Free videos get you started. $2 Minis go deeper when you need them. 
                  No subscriptions, no upsells — just focused prep.
                </p>
              </div>
            </div>
            
            <div className="space-y-6">
              {[
                { 
                  title: "Course-specific", 
                  desc: "Content built for your actual class, not generic topics." 
                },
                { 
                  title: "Step-by-step", 
                  desc: "Every problem walked through clearly, no skipped steps." 
                },
                { 
                  title: "Affordable", 
                  desc: "Free videos. $2 guides. $9 exam packs. Fair pricing." 
                },
                { 
                  title: "No fluff", 
                  desc: "Direct to the point. We respect your study time." 
                },
              ].map((item) => (
                <div key={item.title} className="card">
                  <h3 className="heading-card mb-1">{item.title}</h3>
                  <p className="text-small">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Trust */}
      <section className="section section-elevated section-border-t">
        <div className="container-tight flex flex-col items-center">
          <h2 className="heading-section font-display mb-6" style={{ textAlign: 'center' }}>
            Built by educators
          </h2>
          
          <div className="max-w-2xl space-y-4">
            <p className="text-lg text-[var(--gray-1)] leading-relaxed" style={{ textAlign: 'center' }}>
              Orbital is created by people who have taught these courses and understand 
              what students struggle with. We know which topics trip people up and 
              where most exam questions come from.
            </p>
            <p className="text-sm text-[var(--gray-2)] mt-8" style={{ textAlign: 'center' }}>
              <strong className="text-white">Note:</strong> Orbital is not affiliated 
              with, endorsed by, or connected to any university. We&apos;re an independent 
              educational resource.
            </p>
          </div>
        </div>
      </section>

      {/* Contact */}
      <section className="section section-border-t">
        <div className="container-tight flex flex-col items-center">
          <h2 className="heading-section font-display mb-4" style={{ textAlign: 'center' }}>
            Questions?
          </h2>
          <p className="text-lg text-[var(--gray-1)] leading-relaxed mb-8" style={{ textAlign: 'center' }}>
            We&apos;re here to help.
          </p>
          <a 
            href={`mailto:${SITE.supportEmail}`}
            className="btn btn-primary btn-lg"
          >
            Contact us
          </a>
        </div>
      </section>

      {/* CTA */}
      <section className="section-lg section-elevated section-border-t">
        <div className="container-tight flex flex-col items-center">
          <h2 className="heading-section font-display mb-4" style={{ textAlign: 'center' }}>
            Ready to start?
          </h2>
          <p className="text-lg text-[var(--gray-1)] leading-relaxed max-w-md mb-8" style={{ textAlign: 'center' }}>
            Find your course and start learning with free walkthrough videos.
          </p>
          <Link href="/courses" className="btn btn-primary btn-lg">
            Find your course
          </Link>
        </div>
      </section>
    </>
  );
}
