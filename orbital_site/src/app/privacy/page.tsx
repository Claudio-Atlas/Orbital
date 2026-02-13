"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

type Theme = "dark" | "light";

export default function PrivacyPage() {
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

        <h1 className="text-3xl font-bold mb-2">Privacy Policy</h1>
        <p className={`text-sm mb-8 ${isDark ? "text-gray-500" : "text-gray-400"}`}>
          Last updated: February 11, 2026
        </p>

        <div className={`prose prose-lg max-w-none ${isDark ? "prose-invert" : ""}`}>
          
          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">1. Introduction</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              Orbital ("we", "our", or "us") is committed to protecting your privacy. 
              This Privacy Policy explains how we collect, use, and safeguard your information 
              when you use our service.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">2. Information We Collect</h2>
            
            <h3 className={`text-lg font-medium mt-4 mb-2 ${isDark ? "text-gray-200" : "text-gray-800"}`}>
              Account Information
            </h3>
            <ul className={`list-disc pl-6 space-y-1 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li>Email address</li>
              <li>Display name (optional)</li>
              <li>Authentication data (securely hashed passwords or OAuth tokens)</li>
            </ul>

            <h3 className={`text-lg font-medium mt-4 mb-2 ${isDark ? "text-gray-200" : "text-gray-800"}`}>
              Usage Data
            </h3>
            <ul className={`list-disc pl-6 space-y-1 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li>Math problems you submit</li>
              <li>Generated videos (temporarily stored for 48 hours)</li>
              <li>Minutes balance and purchase history</li>
              <li>Voice preferences</li>
            </ul>

            <h3 className={`text-lg font-medium mt-4 mb-2 ${isDark ? "text-gray-200" : "text-gray-800"}`}>
              Technical Data
            </h3>
            <ul className={`list-disc pl-6 space-y-1 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li>IP address</li>
              <li>Browser type and version</li>
              <li>Device information</li>
              <li>Usage patterns and analytics</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">3. How We Use Your Information</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              We use collected information to:
            </p>
            <ul className={`list-disc pl-6 mt-2 space-y-1 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li>Provide and maintain the Service</li>
              <li>Process payments and manage your account</li>
              <li>Generate math tutorial videos based on your submissions</li>
              <li>Send you video files via email</li>
              <li>Improve our AI models and service quality</li>
              <li>Detect and prevent fraud or abuse</li>
              <li>Communicate with you about your account or the Service</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">4. Data Retention</h2>
            <div className={`p-4 rounded-lg mb-4 ${isDark ? "bg-blue-500/10 border border-blue-500/20" : "bg-blue-50 border border-blue-200"}`}>
              <p className={isDark ? "text-blue-300" : "text-blue-700"}>
                <strong>Videos:</strong> Automatically deleted 48 hours after generation
              </p>
            </div>
            <ul className={`list-disc pl-6 space-y-1 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li><strong>Account data:</strong> Retained while your account is active</li>
              <li><strong>Purchase history:</strong> Retained for legal and tax purposes</li>
              <li><strong>Problem submissions:</strong> May be retained in anonymized form to improve our AI</li>
              <li><strong>Videos:</strong> Deleted 48 hours after creation (you receive an email copy)</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">5. Data Sharing</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              We do <strong>not</strong> sell your personal information. We may share data with:
            </p>
            <ul className={`list-disc pl-6 mt-2 space-y-1 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li><strong>Payment processors:</strong> Stripe, to process purchases</li>
              <li><strong>Email providers:</strong> Resend, to deliver video emails</li>
              <li><strong>Cloud infrastructure:</strong> Supabase, Vercel, for hosting</li>
              <li><strong>AI providers:</strong> DeepSeek, for problem parsing (without personal data)</li>
              <li><strong>Legal requirements:</strong> When required by law</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">6. Your Rights</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              You have the right to:
            </p>
            <ul className={`list-disc pl-6 mt-2 space-y-1 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li><strong>Access:</strong> Request a copy of your data</li>
              <li><strong>Correction:</strong> Update inaccurate information</li>
              <li><strong>Deletion:</strong> Delete your account and associated data</li>
              <li><strong>Export:</strong> Receive your data in a portable format</li>
            </ul>
            <p className={`mt-4 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              To exercise these rights, use the Settings page or contact us at{" "}
              <a href="mailto:privacy@orbitalsolver.io" className="text-violet-400 hover:text-violet-300">
                privacy@orbitalsolver.io
              </a>
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">7. Security</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              We implement industry-standard security measures including:
            </p>
            <ul className={`list-disc pl-6 mt-2 space-y-1 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li>HTTPS encryption for all data in transit</li>
              <li>Encrypted password storage</li>
              <li>Row-level security for database access</li>
              <li>Regular security audits</li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">8. Cookies</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              We use minimal cookies for:
            </p>
            <ul className={`list-disc pl-6 mt-2 space-y-1 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              <li>Authentication (session management)</li>
              <li>Preferences (theme, voice selection)</li>
            </ul>
            <p className={`mt-2 ${isDark ? "text-gray-300" : "text-gray-600"}`}>
              We do not use tracking or advertising cookies.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">9. Children's Privacy</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              Orbital is intended for users 13 years and older. We do not knowingly collect 
              information from children under 13. If you believe a child has provided us with 
              personal information, please contact us.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">10. Changes to This Policy</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              We may update this Privacy Policy periodically. We will notify you of significant 
              changes via email or a notice on our website.
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">11. Contact Us</h2>
            <p className={isDark ? "text-gray-300" : "text-gray-600"}>
              For privacy-related questions or concerns:{" "}
              <a href="mailto:privacy@orbitalsolver.io" className="text-violet-400 hover:text-violet-300">
                privacy@orbitalsolver.io
              </a>
            </p>
          </section>

        </div>

        <div className={`mt-12 pt-8 border-t ${isDark ? "border-white/10" : "border-gray-200"}`}>
          <Link 
            href="/terms"
            className={`text-sm ${isDark ? "text-violet-400 hover:text-violet-300" : "text-violet-600 hover:text-violet-500"}`}
          >
            Read our Terms of Service →
          </Link>
        </div>
      </div>
    </div>
  );
}
