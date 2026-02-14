"""
Celery Worker Entry Point
=========================
This is like "hiring chefs" for your kitchen.

Run with:
    celery -A celery_app worker --loglevel=info

For production (multiple workers):
    celery -A celery_app worker --loglevel=info --concurrency=4

To monitor tasks (flower dashboard):
    pip install flower
    celery -A celery_app flower --port=5555
"""

# Import the celery app and tasks to register them
from celery_app import celery_app
import tasks  # This registers the tasks with Celery

if __name__ == "__main__":
    # This allows running: python worker.py
    # But typically you'd use: celery -A celery_app worker
    celery_app.start()
