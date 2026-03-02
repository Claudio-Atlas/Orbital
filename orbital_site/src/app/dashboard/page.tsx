"use client";

import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import DashboardClient from "./DashboardClient";

export default function DashboardPage() {
  const { user, profile, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
    if (!loading && profile?.role === "professor") {
      router.push("/professor/dashboard");
    }
  }, [loading, user, profile, router]);

  // Show nothing while checking role
  if (loading || profile?.role === "professor") {
    return null;
  }

  return <DashboardClient />;
}
