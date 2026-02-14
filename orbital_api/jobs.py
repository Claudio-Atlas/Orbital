"""
Job Storage
===========
Persistent storage for job status and metadata.

Think of this as the "order tracking system":
- Customer can check "where's my order?"
- Kitchen updates "order #42 is in the oven"
- System remembers orders even if the restaurant closes and reopens

Two modes:
1. In-memory (local dev): Fast, but lost on restart
2. Supabase (production): Persistent, survives restarts/deploys
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

# Check if we should use Supabase
USE_SUPABASE = os.getenv("USE_SUPABASE_JOBS", "false").lower() == "true"


class JobStore(ABC):
    """Abstract base for job storage."""
    
    @abstractmethod
    def create(self, job_id: str, user_id: str, problem: str, steps: list) -> Dict:
        pass
    
    @abstractmethod
    def get(self, job_id: str) -> Optional[Dict]:
        pass
    
    @abstractmethod
    def update(self, job_id: str, **kwargs) -> bool:
        pass
    
    @abstractmethod
    def get_user_jobs(self, user_id: str, limit: int = 20) -> list:
        pass


class InMemoryJobStore(JobStore):
    """
    Simple in-memory storage for local development.
    Fast but not persistent.
    """
    
    def __init__(self):
        self._jobs: Dict[str, Dict] = {}
    
    def create(self, job_id: str, user_id: str, problem: str, steps: list) -> Dict:
        job = {
            "job_id": job_id,
            "user_id": user_id,
            "status": "pending",
            "problem": problem,
            "steps": steps,
            "video_url": None,
            "error": None,
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None,
            "celery_task_id": None,
        }
        self._jobs[job_id] = job
        return job
    
    def get(self, job_id: str) -> Optional[Dict]:
        return self._jobs.get(job_id)
    
    def update(self, job_id: str, **kwargs) -> bool:
        if job_id not in self._jobs:
            return False
        self._jobs[job_id].update(kwargs)
        return True
    
    def get_user_jobs(self, user_id: str, limit: int = 20) -> list:
        user_jobs = [j for j in self._jobs.values() if j["user_id"] == user_id]
        # Sort by created_at desc
        user_jobs.sort(key=lambda x: x["created_at"], reverse=True)
        return user_jobs[:limit]


class SupabaseJobStore(JobStore):
    """
    Persistent storage using Supabase.
    Survives restarts and deploys.
    
    Table schema (create in Supabase):
    
    CREATE TABLE video_jobs (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        job_id TEXT UNIQUE NOT NULL,
        user_id UUID REFERENCES auth.users(id),
        status TEXT NOT NULL DEFAULT 'pending',
        problem TEXT,
        steps JSONB,
        video_url TEXT,
        error TEXT,
        celery_task_id TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        started_at TIMESTAMPTZ,
        completed_at TIMESTAMPTZ
    );
    
    CREATE INDEX idx_video_jobs_user ON video_jobs(user_id);
    CREATE INDEX idx_video_jobs_status ON video_jobs(status);
    """
    
    def __init__(self):
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")  # Use service key for backend
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY required")
        self._client = create_client(url, key)
        self._table = "video_jobs"
    
    def create(self, job_id: str, user_id: str, problem: str, steps: list) -> Dict:
        job = {
            "job_id": job_id,
            "user_id": user_id,
            "status": "pending",
            "problem": problem,
            "steps": steps,
        }
        result = self._client.table(self._table).insert(job).execute()
        return result.data[0] if result.data else job
    
    def get(self, job_id: str) -> Optional[Dict]:
        result = self._client.table(self._table)\
            .select("*")\
            .eq("job_id", job_id)\
            .single()\
            .execute()
        return result.data if result.data else None
    
    def update(self, job_id: str, **kwargs) -> bool:
        result = self._client.table(self._table)\
            .update(kwargs)\
            .eq("job_id", job_id)\
            .execute()
        return len(result.data) > 0 if result.data else False
    
    def get_user_jobs(self, user_id: str, limit: int = 20) -> list:
        result = self._client.table(self._table)\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        return result.data if result.data else []


# Global instance - picks the right backend based on environment
def get_job_store() -> JobStore:
    """
    Factory function to get the appropriate job store.
    
    Set USE_SUPABASE_JOBS=true in production.
    """
    if USE_SUPABASE:
        return SupabaseJobStore()
    return InMemoryJobStore()


# Singleton for convenience
_store: Optional[JobStore] = None

def job_store() -> JobStore:
    global _store
    if _store is None:
        _store = get_job_store()
    return _store
