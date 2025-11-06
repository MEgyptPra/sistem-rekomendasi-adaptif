"""
Background Scheduler for Incremental Learning Maintenance
Handles periodic cleanup and optional full model retraining
"""
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.services.incremental_learner import incremental_learner


class LearningScheduler:
    """
    Manages background tasks for ML system maintenance.
    
    Tasks:
    1. Hourly: Clear old cache (already handled by incremental_learner)
    2. Daily: Cleanup old interaction data (optional)
    3. Weekly: Full model retrain (optional, for deep learning models)
    """
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    def start(self):
        """Start the scheduler"""
        if self.is_running:
            return
        
        # Task 1: Cache cleanup (setiap 6 jam)
        self.scheduler.add_job(
            self.cleanup_old_data,
            CronTrigger(hour='*/6'),  # Every 6 hours
            id='cleanup_cache',
            name='Clean up old cache data',
            replace_existing=True
        )
        
        # Task 2: Optional - Full model retrain (setiap Minggu jam 2 pagi)
        # UNCOMMENT jika ingin auto retrain model ML lengkap
        # self.scheduler.add_job(
        #     self.full_model_retrain,
        #     CronTrigger(day_of_week='sun', hour=2),  # Minggu pagi jam 2
        #     id='full_retrain',
        #     name='Full ML model retraining',
        #     replace_existing=True
        # )
        
        self.scheduler.start()
        self.is_running = True
        print("✅ Learning Scheduler started!")
        print("   - Cache cleanup: Every 6 hours")
        print("   - Full retrain: Disabled (uncomment to enable)")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.is_running = False
            print("🛑 Learning Scheduler stopped")
    
    async def cleanup_old_data(self):
        """Clean up old cached data"""
        try:
            print(f"🧹 [{datetime.now()}] Running cache cleanup...")
            await incremental_learner.schedule_cleanup()
            print(f"✅ [{datetime.now()}] Cache cleanup completed")
        except Exception as e:
            print(f"❌ Cache cleanup failed: {e}")
    
    async def full_model_retrain(self):
        """
        Optional: Full model retraining for deep learning models.
        WARNING: This is resource-intensive!
        """
        try:
            print(f"🔄 [{datetime.now()}] Starting full model retrain...")
            
            # Import ML service
            from app.services.ml_service import ml_service
            
            # Get database session
            async for db in get_db_session():
                # Train all algorithms
                result = await ml_service.train_model(
                    algorithm='hybrid',
                    force_retrain=True,
                    db=db
                )
                
                print(f"✅ [{datetime.now()}] Full model retrain completed")
                print(f"   Result: {result}")
                break
                
        except Exception as e:
            print(f"❌ Full model retrain failed: {e}")


# Global scheduler instance
learning_scheduler = LearningScheduler()


def start_scheduler():
    """Start the learning scheduler"""
    learning_scheduler.start()


def stop_scheduler():
    """Stop the learning scheduler"""
    learning_scheduler.stop()
