from django.apps import AppConfig


class NewsCrawlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_crawler'
    
    def ready(self):
        # Start the news scheduler when Django starts
        from .tasks import news_scheduler
        news_scheduler.start()
