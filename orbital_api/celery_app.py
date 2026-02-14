"""
Celery Configuration
====================
This is the "ticket rail" - configures how jobs flow through the system.

Components:
- Broker (Redis): Where job tickets wait in line
- Backend (Redis): Where job results/status are stored
- Worker: Separate process that picks up tickets and does the work
"""

import os
from celery import Celery

# Redis URL from environment (Railway provides this, or use local)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create the Celery app
# - broker: where tasks wait in queue (the "order rail")
# - backend: where results are stored (so we can check status)
celery_app = Celery(
    "orbital",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks"]  # Import our task definitions
)

# Configuration
celery_app.conf.update(
    # Serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    
    # Timezone
    timezone="UTC",
    enable_utc=True,
    
    # Task settings
    task_track_started=True,  # Track when task starts (not just queued)
    task_time_limit=600,      # Hard limit: 10 minutes per video
    task_soft_time_limit=540, # Soft limit: 9 minutes (raises exception, allows cleanup)
    
    # Result settings  
    result_expires=86400,     # Results expire after 24 hours
    
    # Worker settings
    worker_prefetch_multiplier=1,  # Only grab 1 task at a time (videos are heavy)
    worker_concurrency=2,          # 2 concurrent tasks per worker (tune based on CPU)
    
    # Retry settings
    task_acks_late=True,           # Only acknowledge task after completion
    task_reject_on_worker_lost=True,  # Re-queue if worker crashes
)

# Optional: Route different task types to different queues
# (for future: could have "fast" queue for parsing, "slow" queue for rendering)
celery_app.conf.task_routes = {
    "tasks.generate_video": {"queue": "video_render"},
    "tasks.parse_problem_task": {"queue": "default"},
}
