import Link from "next/link";
import { Metadata } from "next";
import { PRODUCT_FAMILIES } from "@/lib/constants";

export const metadata: Metadata = {
  title: "Store",
  description: "STEM study guides starting at $2. Orbital Minis, Exam Packs, and the Vault subscription.",
};

const PRODUCTS = [
  {
    category: "Quick Prep",
    items: [
      {
        ...PRODUCT_FAMILIES.mini,
        features: ["Single topic focus", "15-20 practice problems", "Step-by-step solutions", "PDF download"],
      },
      {
        ...PRODUCT_FAMILIES.review,
        features: ["Concept summary", "Key formulas", "Practice problems", "Solution walkthrough"],
      },
      {
        ...PRODUCT_FAMILIES.drill,
        features: ["50+ practice problems", "Timed practice mode", "Difficulty progression", "Full solutions"],
      },
    ],
  },
  {
    category: "Exam Ready",
    items: [
      {
        ...PRODUCT_FAMILIES.examPack,
        features: ["Full exam coverage", "All topic Minis included", "Practice exam", "Video walkthroughs"],
      },
      {
        ...PRODUCT_FAMILIES.finalSprint,
        features: ["Final exam focus", "Comprehensive review", "Quick reference sheets", "Last-minute tips"],
      },
    ],
  },
  {
    category: "Unlimited",
    items: [
      {
        ...PRODUCT_FAMILIES.vault,
        features: ["All courses included", "All future content", "Priority support", "Cancel anytime"],
        priceNote: "per month",
      },
    ],
  },
];

export default function StorePage() {
  return (
    <>
      {/* Hero */}
      <section className="section relative overflow-hidden">
        <div className="glow-orb -top-64 left-1/2 -translate-x-1/2" />
        
        <div className="container-tight relative flex flex-col items-center">
          <h1 className="heading-hero font-display mb-6" style={{ textAlign: 'center' }}>
            Study guides
          </h1>
          
          <p className="text-lg text-[var(--gray-1)] leading-relaxed max-w-lg" style={{ textAlign: 'center' }}>
            Focused exam prep starting at $2. No subscriptions required — pay only for what you need.
          </p>
        </div>
      </section>

      <div className="divider" />

      {/* Products */}
      {PRODUCTS.map((section) => (
        <section key={section.category} className="section section-border-t">
          <div className="container-wide">
            <h2 className="heading-section font-display mb-8">{section.category}</h2>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {section.items.map((product) => (
                <div 
                  key={product.name} 
                  className={`card ${product.name === PRODUCT_FAMILIES.vault.name ? 'card-highlight' : ''}`}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="heading-card">{product.name}</h3>
                      <p className="text-small mt-1">{product.description}</p>
                    </div>
                  </div>
                  
                  <div className="mb-6">
                    <span className="text-3xl font-bold text-accent-violet">
                      ${product.price}
                    </span>
                    {'priceNote' in product && (
                      <span className="text-small ml-1">/{product.priceNote}</span>
                    )}
                  </div>
                  
                  <ul className="space-y-2.5 mb-6">
                    {product.features.map((feature) => (
                      <li key={feature} className="flex items-center gap-2.5 text-sm text-gray-1">
                        <svg className="w-4 h-4 text-accent-violet flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        {feature}
                      </li>
                    ))}
                  </ul>
                  
                  <Link 
                    href="/courses" 
                    className={`btn w-full ${product.name === PRODUCT_FAMILIES.vault.name ? 'btn-primary' : 'btn-secondary'}`}
                  >
                    {product.price === 0 ? 'Start Free' : 'Browse Courses'}
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </section>
      ))}

      {/* FAQ */}
      <section className="section section-elevated section-border-t">
        <div className="container-tight flex flex-col items-center">
          <h2 className="heading-section font-display mb-10" style={{ textAlign: 'center' }}>
            Common questions
          </h2>
          
          <div className="space-y-6 max-w-2xl mx-auto">
            {[
              {
                q: "What's the difference between Minis and Exam Packs?",
                a: "Minis cover a single topic ($2). Exam Packs bundle all topics for an exam plus practice tests ($9). If you only need help with one concept, start with a Mini.",
              },
              {
                q: "Are the free videos really free?",
                a: "Yes. Core walkthrough videos are free forever. Paid guides give you additional practice problems, downloadable materials, and premium content.",
              },
              {
                q: "Can I get a refund?",
                a: "Yes. If you're not satisfied within 7 days of purchase, contact us for a full refund. No questions asked.",
              },
              {
                q: "Is the Vault worth it?",
                a: "If you're taking multiple STEM courses or want access to everything, yes. One month of Vault costs less than two Exam Packs and gives you unlimited access.",
              },
            ].map((faq) => (
              <div key={faq.q} className="pb-6 border-b border-white/[0.06] last:border-0">
                <h3 className="heading-card mb-2">{faq.q}</h3>
                <p className="text-small leading-relaxed">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
