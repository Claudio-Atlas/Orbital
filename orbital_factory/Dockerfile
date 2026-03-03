# ============================================
# Orbital Video Pipeline Worker
# ============================================
# Renders math tutorial videos using Manim + ElevenLabs TTS
# Polls Supabase job queue for work
#
# Build:  docker build -t orbital-worker .
# Run:    docker run --env-file .env orbital-worker
# ============================================

# Use official Manim image (includes Python 3.11, LaTeX, ffmpeg, Cairo)
FROM manimcommunity/manim:v0.18.1

# Switch to root for installs
USER root

# Install additional system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy worker code + scene generators
COPY worker.py .
COPY scene_v3.py .
COPY scene_v2.py .
COPY contracts/ contracts/

# Create output directories
RUN mkdir -p output scripts logs media

# Drop back to non-root user
USER manimuser

# Health check — verify manim works
HEALTHCHECK --interval=60s --timeout=10s \
    CMD python -c "import manim; print('ok')" || exit 1

# Run the worker
CMD ["python", "worker.py"]
