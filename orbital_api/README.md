# Orbital Solver API

FastAPI backend for generating step-by-step math tutorial videos.

## Quick Start

1. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API:**
   ```bash
   ./run.sh
   # Or: python3 -m uvicorn main:app --reload
   ```

4. **Open docs:** http://localhost:8000/docs

## API Endpoints

### POST /solve
Submit a math problem to solve.

**Request:**
```json
{
  "problem": "Solve for x: 2x + 5 = 11",
  "voice": "allison"
}
```

**Or with image:**
```json
{
  "image": "base64-encoded-image-data",
  "voice": "sarah"
}
```

**Response:**
```json
{
  "job_id": "abc12345",
  "status": "pending",
  "message": "Problem received. Generating video..."
}
```

### GET /job/{job_id}
Check job status.

**Response (processing):**
```json
{
  "job_id": "abc12345",
  "status": "processing",
  "problem": "Solve for x: 2x + 5 = 11",
  "steps": [...]
}
```

**Response (complete):**
```json
{
  "job_id": "abc12345",
  "status": "complete",
  "video_url": "/videos/abc12345.mp4",
  "steps": [...]
}
```

### GET /health
Health check.

## Available Voices

- `allison` - Female, warm (default)
- `sarah` - Female, professional  
- `alice` - Female, friendly
- `daniel` - Male, clear
- `george` - Male, authoritative

## Architecture

```
POST /solve
    │
    ├─► Parser (GPT-4) ──► JSON steps
    │
    ├─► Pipeline
    │       ├─► ElevenLabs (audio)
    │       ├─► Manim (animation)
    │       └─► FFmpeg (compose)
    │
    └─► /videos/{job_id}.mp4
```
