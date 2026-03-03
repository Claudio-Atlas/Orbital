-- Pipeline Job Queue
CREATE TABLE IF NOT EXISTS video_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    problem TEXT NOT NULL,
    detail_level TEXT DEFAULT 'standard' CHECK (detail_level IN ('quick', 'standard', 'detailed')),
    path TEXT NOT NULL CHECK (path IN ('full_ai', 'ai_review', 'professor_source')),
    lean_requested BOOLEAN DEFAULT false,
    notes TEXT,
    
    -- Pipeline status
    status TEXT DEFAULT 'queued' CHECK (status IN (
        'queued', 'stage_1', 'stage_2', 'stage_3', 'stage_4', 'stage_5', 'stage_6',
        'awaiting_review', 'complete', 'failed'
    )),
    stage_detail TEXT,
    
    -- Script data
    script_json JSONB,
    revised_script_json JSONB,
    professor_steps JSONB,           -- Path C: professor-provided steps
    professor_images TEXT[],         -- Path C: image URLs for OCR
    
    -- Verification
    verification_method TEXT CHECK (verification_method IN ('lean4', 'circle', 'teacher', 'skipped')),
    verification_badge TEXT CHECK (verification_badge IN ('lean4_verified', 'ai_verified', 'teacher_verified')),
    circle_log TEXT,
    lean_file TEXT,
    
    -- Output
    video_url TEXT,
    youtube_id TEXT,
    youtube_url TEXT,
    thumbnail_url TEXT,
    duration_seconds INT,
    visibility TEXT DEFAULT 'unlisted' CHECK (visibility IN ('unlisted', 'public')),
    
    -- Tags
    tags TEXT[] DEFAULT '{}',
    
    -- Cost tracking
    cost_script DECIMAL(10,4) DEFAULT 0,
    cost_circle DECIMAL(10,4) DEFAULT 0,
    cost_lean DECIMAL(10,4) DEFAULT 0,
    cost_tts DECIMAL(10,4) DEFAULT 0,
    cost_total DECIMAL(10,4) DEFAULT 0,
    
    -- Errors
    error TEXT,
    retry_count INT DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

-- API Keys (encrypted via Supabase Vault in production, plaintext for now)
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) UNIQUE,
    deepseek_key TEXT,
    anthropic_key TEXT,
    elevenlabs_key TEXT,
    youtube_oauth_token JSONB,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Courses / Playlists
CREATE TABLE IF NOT EXISTS courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    youtube_playlist_id TEXT,
    visibility TEXT DEFAULT 'unlisted' CHECK (visibility IN ('unlisted', 'public')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Course items (video ordering)
CREATE TABLE IF NOT EXISTS course_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    video_job_id UUID REFERENCES video_jobs(id) ON DELETE CASCADE,
    position INT NOT NULL,
    youtube_playlist_item_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(course_id, video_job_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_video_jobs_user ON video_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_video_jobs_status ON video_jobs(status);
CREATE INDEX IF NOT EXISTS idx_courses_user ON courses(user_id);
CREATE INDEX IF NOT EXISTS idx_course_items_course ON course_items(course_id);

-- RLS Policies
ALTER TABLE video_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_items ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users see own video_jobs" ON video_jobs
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users see own api_keys" ON api_keys
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users see own courses" ON courses
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users see own course_items" ON course_items
    FOR ALL USING (
        course_id IN (SELECT id FROM courses WHERE user_id = auth.uid())
    );

-- Enable realtime for video_jobs (live status updates)
ALTER PUBLICATION supabase_realtime ADD TABLE video_jobs;
