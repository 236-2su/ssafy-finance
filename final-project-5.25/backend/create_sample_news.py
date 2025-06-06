import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_pjt.settings')
django.setup()

from news_crawler.models import NewsArticle
from django.utils import timezone
from datetime import timedelta

# Create sample news articles
sample_news = [
    {
        'title': 'Market Volatility Continues Amidst Economic Uncertainty',
        'content': 'Global markets experienced another day of fluctuations as investors reacted to mixed economic signals and geopolitical developments. The volatility reflects ongoing concerns about inflation, interest rates, and global economic stability.',
        'summary': 'Global markets experienced fluctuations due to mixed economic signals and geopolitical developments.',
        'url': 'https://example.com/news/1',
        'published_date': timezone.now() - timedelta(hours=2),
        'category': '금융'
    },
    {
        'title': 'Central Bank Holds Steady on Interest Rates',
        'content': 'The Central Bank announced today that it would maintain current interest rates, citing a need to balance inflation concerns with supporting economic growth. This decision was widely expected by market analysts.',
        'summary': 'Central Bank maintains current interest rates to balance inflation concerns with economic growth.',
        'url': 'https://example.com/news/2',
        'published_date': timezone.now() - timedelta(hours=4),
        'category': '경제'
    },
    {
        'title': 'Tech Sector Leads Market Gains',
        'content': 'The technology sector outperformed other industries today, driven by strong earnings reports and optimism about future innovation. Major tech companies saw significant gains in their stock prices.',
        'summary': 'Technology sector outperformed other industries driven by strong earnings and innovation optimism.',
        'url': 'https://example.com/news/3',
        'published_date': timezone.now() - timedelta(hours=6),
        'category': '주식'
    },
    {
        'title': 'Cryptocurrency Market Shows Signs of Recovery',
        'content': 'Major cryptocurrencies have shown positive momentum this week, with Bitcoin and Ethereum leading the charge in market recovery. Institutional adoption continues to drive investor confidence.',
        'summary': 'Major cryptocurrencies show positive momentum with Bitcoin and Ethereum leading market recovery.',
        'url': 'https://example.com/news/4',
        'published_date': timezone.now() - timedelta(hours=8),
        'category': '투자'
    },
    {
        'title': 'Global Supply Chain Disruptions Impact Markets',
        'content': 'Ongoing supply chain disruptions continue to affect global markets, with shipping delays and material shortages impacting various industries. Companies are adapting their strategies to mitigate these challenges.',
        'summary': 'Supply chain disruptions continue affecting global markets with shipping delays and material shortages.',
        'url': 'https://example.com/news/5',
        'published_date': timezone.now() - timedelta(hours=10),
        'category': '금융'
    }
]

# Create news articles
created_count = 0
for news_data in sample_news:
    article, created = NewsArticle.objects.get_or_create(
        url=news_data['url'],
        defaults=news_data
    )
    if created:
        created_count += 1

print(f"Created {created_count} new news articles")
print(f"Total news articles in database: {NewsArticle.objects.count()}")
