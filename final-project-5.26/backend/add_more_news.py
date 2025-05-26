import os
import django
from datetime import datetime, timedelta

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_pjt.settings')
django.setup()

from news_crawler.models import NewsArticle
from django.utils import timezone

def add_sample_news():
    """더 많은 샘플 뉴스를 추가합니다."""
    
    sample_news = [
        {
            'title': '삼성전자, 3분기 실적 시장 예상치 상회...반도체 회복세',
            'content': '삼성전자가 3분기 실적에서 시장 예상치를 상회하는 성과를 기록했다. 메모리 반도체 시장의 회복세와 함께 스마트폰 사업부문도 견조한 실적을 보였다.',
            'summary': '삼성전자가 3분기 실적에서 시장 예상치를 상회하며 반도체 회복세를 보였다.',
            'url': 'https://finance.naver.com/news/sample4',
            'category': '주식',
            'hours_ago': 1
        },
        {
            'title': 'SK하이닉스, HBM 수요 급증으로 주가 강세...목표가 상향',
            'content': 'SK하이닉스가 고대역폭메모리(HBM) 수요 급증에 힘입어 주가 강세를 보이고 있다. 증권사들은 잇따라 목표주가를 상향 조정하고 있다.',
            'summary': 'SK하이닉스가 HBM 수요 급증으로 주가 강세를 보이며 목표가가 상향되고 있다.',
            'url': 'https://finance.naver.com/news/sample5',
            'category': '주식',
            'hours_ago': 2
        },
        {
            'title': '미국 연준, 금리 인하 신호...국내 증시에 호재',
            'content': '미국 연방준비제도가 금리 인하 신호를 보내면서 국내 증시에 호재로 작용하고 있다. 외국인 투자자들의 신흥국 투자 심리가 개선되고 있다.',
            'summary': '미국 연준의 금리 인하 신호가 국내 증시에 호재로 작용하고 있다.',
            'url': 'https://finance.naver.com/news/sample6',
            'category': '금융',
            'hours_ago': 3
        },
        {
            'title': '원달러 환율 1,300원대 중반...수출기업 수혜 기대',
            'content': '원달러 환율이 1,300원대 중반에서 안정세를 보이면서 수출기업들의 수혜가 기대되고 있다. 특히 자동차와 조선업계의 실적 개선이 예상된다.',
            'summary': '원달러 환율 안정으로 수출기업들의 수혜가 기대되고 있다.',
            'url': 'https://finance.naver.com/news/sample7',
            'category': '경제',
            'hours_ago': 4
        },
        {
            'title': '국내 부동산 시장, 금리 인하 기대감으로 거래량 증가',
            'content': '금리 인하 기대감이 높아지면서 국내 부동산 시장의 거래량이 증가하고 있다. 서울 아파트 매매가격도 상승세를 보이고 있다.',
            'summary': '금리 인하 기대감으로 부동산 시장 거래량이 증가하고 있다.',
            'url': 'https://finance.naver.com/news/sample8',
            'category': '부동산',
            'hours_ago': 5
        },
        {
            'title': '테슬라 주가 급등, 국내 2차전지 관련주도 동반 상승',
            'content': '테슬라 주가가 급등하면서 국내 2차전지 관련주들도 동반 상승하고 있다. LG에너지솔루션과 삼성SDI 등이 강세를 보이고 있다.',
            'summary': '테슬라 주가 급등으로 국내 2차전지 관련주들이 동반 상승하고 있다.',
            'url': 'https://finance.naver.com/news/sample9',
            'category': '주식',
            'hours_ago': 6
        },
        {
            'title': '국내 금값, 온스당 2,000달러 돌파...안전자산 선호',
            'content': '국내 금값이 온스당 2,000달러를 돌파하며 사상 최고치를 경신했다. 글로벌 불확실성 증가로 안전자산에 대한 선호가 높아지고 있다.',
            'summary': '국내 금값이 온스당 2,000달러를 돌파하며 사상 최고치를 기록했다.',
            'url': 'https://finance.naver.com/news/sample10',
            'category': '투자',
            'hours_ago': 7
        },
        {
            'title': '카카오뱅크, 3분기 순이익 전년 동기 대비 30% 증가',
            'content': '카카오뱅크가 3분기 순이익에서 전년 동기 대비 30% 증가한 실적을 발표했다. 대출 잔액 증가와 수수료 수익 확대가 주요 요인으로 분석된다.',
            'summary': '카카오뱅크가 3분기 순이익에서 전년 동기 대비 30% 증가를 기록했다.',
            'url': 'https://finance.naver.com/news/sample11',
            'category': '금융',
            'hours_ago': 8
        }
    ]
    
    saved_count = 0
    for news_data in sample_news:
        try:
            # 중복 체크
            if NewsArticle.objects.filter(url=news_data['url']).exists():
                print(f"이미 존재하는 뉴스: {news_data['title']}")
                continue
                
            # 시간 계산
            published_date = timezone.now() - timedelta(hours=news_data['hours_ago'])
            
            article = NewsArticle.objects.create(
                title=news_data['title'],
                content=news_data['content'],
                summary=news_data['summary'],
                url=news_data['url'],
                published_date=published_date,
                category=news_data['category']
            )
            
            saved_count += 1
            print(f"뉴스 추가됨: {news_data['title']}")
            
        except Exception as e:
            print(f"뉴스 추가 오류: {e}")
    
    print(f"\n총 {saved_count}개의 새로운 뉴스가 추가되었습니다.")
    
    # 전체 뉴스 개수 확인
    total_count = NewsArticle.objects.count()
    print(f"데이터베이스 총 뉴스 개수: {total_count}")

if __name__ == "__main__":
    add_sample_news()
