from django.core.management.base import BaseCommand
from news_crawler.crawler import NaverFinanceCrawler

class Command(BaseCommand):
    help = 'Crawl financial news from various sources'

    def handle(self, *args, **options):
        crawler = NaverFinanceCrawler()
        saved_count = crawler.crawl_and_save()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully crawled and saved {saved_count} news articles')
        )
