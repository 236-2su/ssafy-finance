import os
import django
from datetime import datetime, timedelta

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_pjt.settings')
django.setup()

from news_crawler.models import NewsArticle

def update_news_with_images():
    """뉴스 기사에 이미지를 추가합니다."""
    
    # 뉴스 이미지 매핑
    news_images = {
        '코스피, 외국인 매수세에 상승 마감...2,600선 회복': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400&h=250&fit=crop',
        '한국은행, 기준금리 동결...경제 불확실성 고려': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400&h=250&fit=crop',
        '비트코인, 5만 달러 돌파...기관투자자 유입 지속': 'https://images.unsplash.com/photo-1518546305927-5a555bb7020d?w=400&h=250&fit=crop',
        '삼성전자, 3분기 실적 시장 예상치 상회...반도체 회복세': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=250&fit=crop',
        'SK하이닉스, HBM 수요 급증으로 주가 강세...목표가 상향': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=250&fit=crop',
        '미국 연준, 금리 인하 신호...국내 증시에 호재': 'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=400&h=250&fit=crop',
        '원달러 환율 1,300원대 중반...수출기업 수혜 기대': 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400&h=250&fit=crop',
        '국내 부동산 시장, 금리 인하 기대감으로 거래량 증가': 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&h=250&fit=crop',
        '테슬라 주가 급등, 국내 2차전지 관련주도 동반 상승': 'https://images.unsplash.com/photo-1593941707882-a5bac6861d75?w=400&h=250&fit=crop',
        '국내 금값, 온스당 2,000달러 돌파...안전자산 선호': 'https://images.unsplash.com/photo-1610375461246-83df859d849d?w=400&h=250&fit=crop',
        '카카오뱅크, 3분기 순이익 전년 동기 대비 30% 증가': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=250&fit=crop'
    }
    
    updated_count = 0
    
    for title, image_url in news_images.items():
        try:
            articles = NewsArticle.objects.filter(title__icontains=title.split(',')[0])
            for article in articles:
                if not article.image_url:  # 이미지가 없는 경우에만 업데이트
                    article.image_url = image_url
                    article.save()
                    updated_count += 1
                    print(f"이미지 추가됨: {article.title[:50]}...")
                    
        except Exception as e:
            print(f"이미지 업데이트 오류: {e}")
    
    print(f"\n총 {updated_count}개의 뉴스에 이미지가 추가되었습니다.")
    
    # 전체 뉴스 확인
    all_articles = NewsArticle.objects.all()
    print(f"데이터베이스 총 뉴스 개수: {all_articles.count()}")
    
    # 이미지가 있는 뉴스 개수 확인
    articles_with_images = NewsArticle.objects.exclude(image_url__isnull=True).exclude(image_url='')
    print(f"이미지가 있는 뉴스 개수: {articles_with_images.count()}")

if __name__ == "__main__":
    update_news_with_images()
