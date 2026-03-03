# Stage 6: Delivery — Contract
**Owner:** Pipeline Controller
**Last Updated:** 2026-03-02

---

## Purpose
Deliver the final video to the requesting user (professor or student), store it for caching/reuse, and update the dashboard with status and metadata.

## Process

### Step 1: Post-Processing
After Stage 5 produces the final MP4:

```python
delivery = {
    "video_path": f"output/{slug}_final.mp4",
    "thumbnail_path": f"output/{slug}_thumb.png",  # auto-generated
    "metadata": {
        "problem": problem_text,
        "course": course,
        "detail_level": detail_level,
        "steps": len(script["steps"]),
        "duration_s": video_duration,
        "badge": verification["badge"],  # "lean4_verified" | "ai_verified"
        "generated_at": datetime.utcnow().isoformat(),
        "cost": total_pipeline_cost,
    }
}
```

**Auto-thumbnail:** Extract frame at 40% of video duration (usually shows the core content, not intro/outro):
```bash
ffmpeg -y -i "$FINAL_VIDEO" -ss "$THUMB_TIME" -vframes 1 -q:v 2 "$THUMB_PATH"
```

### Step 2: Storage

| Storage Layer | Purpose | Location |
|---|---|---|
| **Local filesystem** | Immediate access, rendering cache | `orbital_factory/output/` |
| **Supabase Storage** | Persistent storage, CDN delivery | `videos/{user_id}/{slug}/` |
| **Cache index** | Deduplication, fast lookup | `videos_cache` table in Supabase |

**Cache strategy:** When a professor generates a video, hash the problem + detail level. If an identical video already exists in cache, serve the cached version instantly (cost: $0).

```sql
CREATE TABLE videos_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    problem_hash TEXT NOT NULL,          -- SHA-256 of normalized problem text
    detail_level TEXT NOT NULL,          -- quick | standard | detailed
    video_url TEXT NOT NULL,             -- Supabase Storage URL
    thumbnail_url TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES profiles(id),
    view_count INT DEFAULT 0,
    UNIQUE(problem_hash, detail_level)
);
```

### Step 3: Dashboard Update
Update the professor's dashboard in real-time during generation:

| Pipeline Stage | Dashboard Status |
|---|---|
| Stage 1: Script | "Generating script..." |
| Stage 2: Circle | "Verifying mathematics..." |
| Stage 3: Lean | "Formally proving..." (or skipped) |
| Stage 4: TTS | "Generating narration..." |
| Stage 5: Render | "Rendering video..." |
| Stage 6: Delivery | "✅ Ready to watch" |

**Implementation:** Supabase Realtime subscriptions on a `video_jobs` table:
```sql
CREATE TABLE video_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id),
    problem TEXT NOT NULL,
    detail_level TEXT DEFAULT 'standard',
    lean_requested BOOLEAN DEFAULT false,
    status TEXT DEFAULT 'queued',        -- queued | stage_1 | stage_2 | ... | complete | failed
    stage_detail TEXT,                   -- human-readable status message
    video_url TEXT,                      -- populated on completion
    thumbnail_url TEXT,
    metadata JSONB,
    cost DECIMAL(10,4),
    error TEXT,                          -- populated on failure
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);
```

### Step 4: Notification
When video is complete:
- Dashboard auto-updates (Supabase Realtime)
- Optional: email notification (future)
- Video appears in professor's Library tab

### Step 5: Usage Tracking
Log the generation for billing:
```sql
CREATE TABLE usage_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id),
    video_job_id UUID REFERENCES video_jobs(id),
    cost_script DECIMAL(10,4),
    cost_circle DECIMAL(10,4),
    cost_lean DECIMAL(10,4),
    cost_tts DECIMAL(10,4),
    cost_total DECIMAL(10,4),
    cached BOOLEAN DEFAULT false,        -- true if served from cache
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Input

From Stage 5:
```json
{
  "video": {
    "path": "output/{slug}_final.mp4",
    "duration_s": 232,
    "file_size_mb": 6.1
  },
  "verification": { ... },
  "metadata": { ... }
}
```

## Output

To user (via dashboard):
```json
{
  "status": "complete",
  "video_url": "https://supabase.co/storage/v1/.../video.mp4",
  "thumbnail_url": "https://supabase.co/storage/v1/.../thumb.png",
  "duration_s": 232,
  "badge": "lean4_verified",
  "steps": 21,
  "cost": 0.98
}
```

## Caching as Differentiator

This is a key business advantage: **common problems are generated once, served to all.**

- "Find the derivative of x²" — generated once, cached, served to 10,000 professors for free
- Only works when WE control the API keys (default billing mode)
- BYOK users don't benefit from the shared cache (their keys, their costs)
- Over time, the cache grows → marginal cost per video approaches $0

**Cache hit rate projections:**
| Month | Estimated cache hit rate |
|---|---|
| Month 1 | ~5% (mostly unique problems) |
| Month 6 | ~20-30% (common calc/algebra problems cached) |
| Year 1 | ~40-50% (large corpus of standard problems) |

## Updated Per-Video Cost Breakdown

| Stage | Cost |
|-------|------|
| 1. Script (DeepSeek V3) | ~$0.001 |
| 2. Circle (3 Opus + 1 Sonnet) | ~$0.60 |
| 3. Lean (Opus, when enabled) | ~$0.10 |
| 4. TTS (ElevenLabs Turbo) | ~$0.12-0.56 |
| 5. Manim Render | $0.00 (local) |
| 6. Delivery + Storage | ~$0.001 |
| **Total (with Lean)** | **$0.82-1.26** |
| **Total (without Lean)** | **$0.72-1.16** |
| **Cached video** | **$0.00** |

## Cloud Rendering Roadmap

Local rendering works for demo and early users, but won't scale. The migration path:

### Phase 1: Now → March 27 Demo
- **Local only** (current Mac Mini)
- 1 video at a time, ~3-5 min render
- Sufficient for demo + early professors

### Phase 2: Mac Mini #2 Arrives (~March 30)
- **Two local machines** — pipeline controller on Mini #1, rendering on Mini #2
- 2 concurrent renders
- Mini #2 also runs local AI (Goedel for Lean, Piper for TTS)

### Phase 3: Early Customers (Month 2-3)
- **Hybrid:** Local + cloud overflow
- Use **Render.com** or **Railway** with Docker container running Manim + ffmpeg
- Spin up cloud instance when queue > 2 jobs
- Estimated cloud cost: ~$0.02-0.05/video (compute time on $7/mo instance)

### Phase 4: Scale (Month 6+)
- **Full cloud rendering** via containerized Manim workers
- **Options:**
  - AWS Lambda + EFS (serverless, pay per render)
  - Railway/Render with auto-scaling Docker
  - GPU instances for 3D scenes (if we add 3d_surface type)
- Pre-baked Manim Docker image with all dependencies + LaTeX
- Target: <60s render time for standard videos

### Cloud Rendering Architecture (Future)
```
Professor submits problem
    ↓
Pipeline controller (always-on, lightweight)
    ↓
Stages 1-4 run (API calls, fast)
    ↓
Stage 5: Render Job Queue
    ├── Local worker (if available)
    └── Cloud worker (Docker, auto-scaled)
         ├── Pull script + audio from S3/Supabase
         ├── Render with Manim
         ├── ffmpeg merge
         └── Upload final MP4 to Supabase Storage
    ↓
Stage 6: Delivery (same as now)
```

### Docker Image Spec (Future)
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    texlive-full ffmpeg libcairo2-dev
RUN pip install manim pydub
COPY scene_v3.py /app/
COPY orbital_colors.py /app/
ENTRYPOINT ["python", "/app/render_worker.py"]
```

## Cost Estimate

| Component | Cost |
|-----------|------|
| Supabase Storage | Free tier: 1GB, then $0.021/GB |
| Auto-thumbnail | Free (ffmpeg) |
| Cache lookup | Free (Supabase query) |
| Cloud render (future) | ~$0.02-0.05/video |
| **Total (local phase)** | **~$0.001** |

---

## Integration Notes

- Stage 6 receives: final MP4 + metadata from Stage 5
- Stage 6 outputs to: user dashboard + Supabase Storage + cache
- Supabase Realtime keeps dashboard in sync during generation
- Cache deduplication is by problem_hash + detail_level
- Usage logging enables future billing (post-demo)
- Cloud rendering migration is non-breaking — same input/output, different execution environment
