"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

type Theme = "dark" | "light";

export default function TermsPage() {
  const [theme, setTheme] = useState<Theme>("dark");

  useEffect(() => {
    const saved = localStorage.getItem("orbital-theme") as Theme;
    if (saved) setTheme(saved);
  }, []);

  const isDark = theme === "dark";

  return (
    <div className={`min-h-screen transition-colors duration-300 ${
      isDark ? "bg-black text-white" : "bg-white text-gray-900"
    }`}>
      <div className="max-w-3xl mx-auto px-6 py-16">
        {/* Back link */}
        <Link 
          href="/"
          className={`inline-flex items-center gap-2 mb-8 text-sm ${
            isDark ? "text-gray-400 hover:text-white" : "text-gray-500 hover:text-gray-900"
          }`}
        >
          ← Back to home
        </Link>

        <h1 className="text-3xl font-bold mb-2">Terms of Service</h1>
        <p className={`text-sm mb-8 ${isDark ? "text-gray-500" : "text-gray-400"}`}>
          Last updated: February 11, 2026
        </p>

        <div className={`prose prose-lg max-w-none ${isDark ? "prose-invert" : ""}`}>
          
          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">1. Acceptance of Terms</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              By accessing or using Orbital ("the Service"), you agree to be bound by these 
              Terms of Service. If you do not agree to these terms, please do not use the Service.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">2. Description of Service</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              Orbital is an AI-powered service that generates step-by-step math tutorial videos. 
              Users can submit math problems via text or image, and receive video explanations 
              in exchange for purchased minutes.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">3. Account Registration</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              To use certain features of the Service, you must create an account. You agree to:
            </p>
            <ul className={`list-disc pl-6 mt-2 space-y-1 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li>Provide accurate and complete information</li>
              <li>Maintain the security of your account credentials</li>
              <li>Accept responsibility for all activities under your account</li>
              <li>Notify us immediately of any unauthorized use</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">4. Pricing and Payments</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              Orbital operates on a minutes-based pricing model. You purchase minutes which are 
              consumed when generating videos. Minutes do not expire for one-time purchases. 
              All sales are final and non-refundable except as required by law.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">5. Fair Use and Anti-Abuse Policy</h2>
            <div className={`p-4 rounded-lg mb-4 ${isDark ? "bg-violet-500/10 border border-violet-500/20" : "bg-violet-50 border border-violet-200"}`}>
              <p className={`font-medium ${isDark ? "text-violet-300" : "text-violet-700"}`}>
                ⚠️ Important: Estimate Cancellation Limits
              </p>
            </div>
            <p className={`mb-4 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              When you submit a problem, we generate an estimate showing how long your video will 
              be and how many minutes it will cost. You may then confirm or cancel before any 
              minutes are deducted.
            </p>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              To prevent abuse of the estimate feature, we enforce the following limits:
            </p>
            <ul className={`list-disc pl-6 mt-2 space-y-2 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li>
                <strong>Cancellation limit:</strong> If you cancel <strong>8 consecutive estimates</strong> without 
                generating a video, your account will be placed on a <strong>24-hour hold</strong> and 
                a small fee (5 seconds of video time) will be deducted from your balance to cover 
                processing costs.
              </li>
              <li>
                <strong>Why this exists:</strong> Each estimate requires server resources to process. 
                This policy prevents bots or bad actors from spamming estimates to drain our resources.
              </li>
              <li>
                <strong>Normal use:</strong> This limit only affects consecutive cancellations. 
                If you generate a video, your cancellation counter resets to zero.
              </li>
              <li>
                <strong>Severe violations:</strong> Automated scraping, bot access, or systematic abuse 
                may result in immediate account termination without refund.
              </li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">6. Prohibited Uses</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              You agree NOT to:
            </p>
            <ul className={`list-disc pl-6 mt-2 space-y-1 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li>Use the Service for any illegal purpose</li>
              <li>Attempt to reverse engineer or copy our AI models</li>
              <li>Use automated tools to access the Service</li>
              <li>Resell or redistribute generated content commercially without permission</li>
              <li>Submit content that infringes on intellectual property rights</li>
              <li>Attempt to bypass usage limits or security measures</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">7. Intellectual Property</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              Videos generated by Orbital are licensed for your personal, educational use. 
              You may share videos for non-commercial educational purposes. The Orbital name, 
              logo, and technology remain our property.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">8. Video Retention</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              Generated videos are stored for <strong>48 hours</strong> after creation. 
              After this period, videos are automatically deleted from our servers. 
              We email you a copy of each video, which you may keep indefinitely.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">9. Disclaimer of Warranties</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              The Service is provided "as is" without warranties of any kind. We do not guarantee 
              that AI-generated solutions are always correct. Users should verify important 
              mathematical work independently.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">10. Limitation of Liability</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              To the maximum extent permitted by law, Orbital shall not be liable for any 
              indirect, incidental, special, or consequential damages arising from your use 
              of the Service.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">11. Changes to Terms</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              We may modify these terms at any time. Continued use of the Service after 
              changes constitutes acceptance of the new terms.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">12. Contact</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              For questions about these Terms, contact us at:{" "}
              <a href="mailto:legal@orbitalsolver.io" className="text-violet-400 hover:text-violet-300">
                legal@orbitalsolver.io
              </a>
            </p>
          </section>

        </div>

        <div className={`mt-12 pt-8 border-t ${isDark ? "border-white/10" : "border-gray-200"}`}>
          <Link 
            href="/privacy"
            className={`text-sm ${isDark ? "text-violet-400 hover:text-violet-300" : "text-violet-600 hover:text-violet-500"}`}
          >
            Read our Privacy Policy →
          </Link>
        </div>
      </div>
    </div>
  );
}
