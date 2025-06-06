import threading
import time
from django.core.management import call_command
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class NewsScheduler:
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.thread.start()
            logger.info("News scheduler started")
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("News scheduler stopped")
    
    def _run_scheduler(self):
        # Initial crawl
        self._crawl_news()
        
        # Schedule every hour (3600 seconds)
        while self.running:
            time.sleep(3600)  # 1 hour
            if self.running:
                self._crawl_news()
    
    def _crawl_news(self):
        try:
            call_command('crawl_news')
            logger.info("News crawling completed successfully")
        except Exception as e:
            logger.error(f"Error during news crawling: {e}")

# Global scheduler instance
news_scheduler = NewsScheduler()
