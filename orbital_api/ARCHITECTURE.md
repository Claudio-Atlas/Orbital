# Orbital API Architecture

## 🍕 The Pizza Shop Model

Think of video generation like running a pizza shop:

```
┌─────────────────────────────────────────────────────────────────┐
│                        PIZZA SHOP                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Customer ──► Waiter ──► Order Rail ──► Chefs ──► Pickup Window │
│     │           │           │             │            │         │
│     │           │           │             │            │         │
│   User        API        Redis         Celery       Video       │
│                          Queue        Workers       Ready!       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Components Explained

| Pizza Shop | Orbital | What It Does |
|------------|---------|--------------|
| Customer | User | Submits a math problem |
| Waiter | FastAPI | Takes the order, gives a ticket number |
| Order ticket | Job Record | Tracks status (pending → processing → complete) |
| Order rail | Redis Queue | Holds jobs waiting to be processed |
| Chefs | Celery Workers | Actually make the videos (Manim + audio) |
| Kitchen timer | Task tracking | Shows progress (30%... 60%... done!) |
| Pickup window | R2 Storage | Where finished videos are stored |
| "Order #42 ready!" | Webhook/Poll | Notifies user their video is done |

---

## Request Flow

### 1. User Submits Problem
```
POST /solve
{
  "problem": "Solve 2x + 5 = 11",
  "voice": "allison"
}
```

### 2. API (Waiter) Processes Order
```python
# Parse the problem (validate the order)
script_data = parse_problem(problem)

# Create job record (write the ticket)
job_store.create(job_id, user_id, problem, steps)

# Queue the task (put ticket on rail)
generate_video.delay(job_id, script_data, voice, user_id)

# Return ticket number to customer
return {"job_id": "abc123", "status": "pending"}
```

### 3. Worker (Chef) Picks Up Job
```python
# Worker grabs next job from queue
@celery_app.task
def generate_video(job_id, script_data, voice, user_id):
    # Update status: "Chef started working on order"
    self.update_state(state="PROCESSING", meta={"progress": 30})
    
    # Render with Manim
    subprocess.run(["python", "pipeline.py", script_path])
    
    # Upload to R2 (put in pickup window)
    video_url = upload_to_r2(video_path)
    
    return {"status": "complete", "video_url": video_url}
```

### 4. User Polls for Status
```
GET /job/abc123

{
  "job_id": "abc123",
  "status": "processing",
  "progress": 60,
  "progress_message": "Rendering video..."
}
```

### 5. Video Ready
```
GET /job/abc123

{
  "job_id": "abc123", 
  "status": "complete",
  "video_url": "https://r2.orbital.../abc123.mp4"
}
```

---

## Scaling

### The Magic: Independent Scaling

```
                    ┌──────────────────┐
                    │   Load Balancer  │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         ┌────────┐    ┌────────┐    ┌────────┐
         │  API   │    │  API   │    │  API   │
         │ (web)  │    │ (web)  │    │ (web)  │
         └────┬───┘    └────┬───┘    └────┬───┘
              │             │             │
              └──────────┬──┴─────────────┘
                         ▼
                  ┌─────────────┐
                  │    Redis    │
                  │   (Queue)   │
                  └──────┬──────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Worker  │    │ Worker  │    │ Worker  │
    │ (chef)  │    │ (chef)  │    │ (chef)  │
    └─────────┘    └─────────┘    └─────────┘
```

**Scale API instances** when you have lots of concurrent users submitting problems.

**Scale Workers** when the queue is backing up (jobs waiting too long).

They're independent! Add more chefs without changing how orders are taken.

---

## Environment Variables

### Required
```bash
# Redis (the order rail)
REDIS_URL=redis://...

# Enable Celery mode (vs local dev mode)
CELERY_ENABLED=true

# Supabase (persistent job storage)
USE_SUPABASE_JOBS=true
SUPABASE_URL=https://...
SUPABASE_SERVICE_KEY=...

# AI APIs
OPENAI_API_KEY=sk-...
FISH_AUDIO_API_KEY=...  # or ELEVENLABS_API_KEY
```

### Optional
```bash
# Cloudflare R2 (video storage)
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET=orbital-videos
R2_ENDPOINT=https://...r2.cloudflarestorage.com
```

---

## Local Development

### Without Celery (simple mode)
```bash
# Just run the API - uses background threads
cd orbital_api
python -m uvicorn main:app --reload --port 8002
```

### With Celery (production-like)
```bash
# Terminal 1: Redis (using Docker)
docker run -p 6379:6379 redis

# Terminal 2: API
CELERY_ENABLED=true python -m uvicorn main:app --reload --port 8002

# Terminal 3: Worker
celery -A celery_app worker --loglevel=info
```

---

## Railway Deployment

### Services Needed

1. **orbital-api** (web)
   - Runs: `uvicorn main:app`
   - Env: `CELERY_ENABLED=true`

2. **orbital-worker** (worker)
   - Runs: `celery -A celery_app worker --loglevel=info`
   - Same env vars as API

3. **Redis** (Railway plugin or Upstash)
   - Provides `REDIS_URL`

4. **Cloudflare R2** (external)
   - Video storage with CDN

---

## Database Schema

### Supabase Table: `video_jobs`

```sql
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

-- Indexes for common queries
CREATE INDEX idx_video_jobs_user ON video_jobs(user_id);
CREATE INDEX idx_video_jobs_status ON video_jobs(status);
CREATE INDEX idx_video_jobs_created ON video_jobs(created_at DESC);

-- RLS: Users can only see their own jobs
ALTER TABLE video_jobs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own jobs"
ON video_jobs FOR SELECT
USING (auth.uid() = user_id);
```

---

## Monitoring

### Flower (Celery Dashboard)
```bash
pip install flower
celery -A celery_app flower --port=5555
```

Opens a web UI at http://localhost:5555 showing:
- Active workers
- Task queue length
- Task success/failure rates
- Individual task details

### Health Check
```
GET /health

{
  "status": "healthy",
  "celery_enabled": true,
  "job_store": "SupabaseJobStore"
}
```
