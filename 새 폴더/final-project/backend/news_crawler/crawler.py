import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from .models import NewsArticle
import re
import time

class NaverFinanceCrawler:
    def __init__(self):
        self.base_url = "https://finance.naver.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def get_news_list(self, max_pages=2):
        """네이버 금융 메인 페이지에서 뉴스를 가져옵니다."""
        news_articles = []
        
        try:
            # 네이버 금융 메인 페이지에서 뉴스 추출
            main_url = "https://finance.naver.com/"
            response = requests.get(main_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 다양한 뉴스 섹션에서 뉴스 추출
            news_selectors = [
                '.news_area .news_list li',
                '.section_news .news_list li', 
                '.today_news .news_list li',
                '.news_wrap .news_item',
                '.news_section .news_list li'
            ]
            
            for selector in news_selectors:
                news_items = soup.select(selector)
                for item in news_items:
                    try:
                        # 제목과 링크 추출
                        title_elem = item.select_one('a')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text(strip=True)
                        if not title or len(title) < 10:  # 너무 짧은 제목 제외
                            continue
                            
                        href = title_elem.get('href')
                        if not href:
                            continue
                            
                        # 상대 URL을 절대 URL로 변환
                        if href.startswith('/'):
                            full_url = self.base_url + href
                        elif href.startswith('http'):
                            full_url = href
                        else:
                            continue
                        
                        # 중복 제거
                        if any(article['url'] == full_url for article in news_articles):
                            continue
                        
                        # 요약 추출
                        summary = ""
                        summary_elem = item.select_one('.news_desc, .desc, .summary')
                        if summary_elem:
                            summary = summary_elem.get_text(strip=True)
                        
                        if not summary:
                            summary = title[:100] + "..." if len(title) > 100 else title
                        
                        news_articles.append({
                            'title': title,
                            'url': full_url,
                            'published_date': timezone.now(),
                            'summary': summary,
                            'category': '금융'
                        })
                        
                    except Exception as e:
                        print(f"뉴스 항목 처리 중 오류: {e}")
                        continue
            
            # 추가로 뉴스 리스트 페이지에서도 가져오기
            news_list_urls = [
                "https://finance.naver.com/news/news_list.naver?mode=LSS2D&section_id=101&section_id2=258",
                "https://finance.naver.com/news/news_list.naver?mode=LSS2D&section_id=101&section_id2=259"
            ]
            
            for news_url in news_list_urls:
                try:
                    response = requests.get(news_url, headers=self.headers)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    news_items = soup.select('.type5 tr')
                    
                    for item in news_items:
                        try:
                            title_elem = item.select_one('.title a')
                            if not title_elem:
                                continue
                                
                            title = title_elem.get_text(strip=True)
                            if not title or len(title) < 10:
                                continue
                                
                            href = title_elem.get('href')
                            if not href:
                                continue
                                
                            if href.startswith('/'):
                                full_url = self.base_url + href
                            else:
                                full_url = href
                            
                            # 중복 제거
                            if any(article['url'] == full_url for article in news_articles):
                                continue
                            
                            # 날짜 추출
                            date_elem = item.select_one('.date')
                            published_date = timezone.now()
                            if date_elem:
                                date_text = date_elem.get_text(strip=True)
                                published_date = self.parse_date(date_text)
                            
                            news_articles.append({
                                'title': title,
                                'url': full_url,
                                'published_date': published_date,
                                'summary': title[:100] + "..." if len(title) > 100 else title,
                                'category': '금융'
                            })
                            
                        except Exception as e:
                            print(f"뉴스 리스트 항목 처리 중 오류: {e}")
                            continue
                    
                    time.sleep(1)  # 요청 간 딜레이
                    
                except Exception as e:
                    print(f"뉴스 리스트 페이지 크롤링 중 오류: {e}")
                    continue
                
        except Exception as e:
            print(f"메인 페이지 크롤링 중 오류: {e}")
        
        return news_articles[:20]  # 최대 20개 뉴스만 반환
    
    def get_article_content(self, url):
        """개별 뉴스 기사의 내용을 가져옵니다."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 다양한 뉴스 사이트의 본문 선택자
            content_selectors = [
                '#newsct_article',
                '.news_end',
                '.article_body',
                '.news_body',
                '.article_content',
                '.content',
                '.news_content'
            ]
            
            content = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # 불필요한 태그 제거
                    for tag in content_elem.select('script, style, .ad, .advertisement, .related, .comment'):
                        tag.decompose()
                    
                    content = content_elem.get_text(strip=True)
                    if len(content) > 100:  # 충분한 내용이 있으면 사용
                        break
            
            return content if content else "내용을 가져올 수 없습니다."
            
        except Exception as e:
            print(f"기사 내용 추출 중 오류: {e}")
            return "내용을 가져올 수 없습니다."
    
    def parse_date(self, date_text):
        """날짜 텍스트를 파싱합니다."""
        try:
            # "2024.01.15" 형식
            if re.match(r'\d{4}\.\d{2}\.\d{2}', date_text):
                date_part = re.search(r'\d{4}\.\d{2}\.\d{2}', date_text).group()
                return datetime.strptime(date_part, '%Y.%m.%d')
            
            # "01.15" 형식 (올해)
            if re.match(r'\d{2}\.\d{2}', date_text):
                current_year = datetime.now().year
                date_with_year = f"{current_year}.{date_text}"
                return datetime.strptime(date_with_year, '%Y.%m.%d')
            
            # "오늘", "어제" 등
            if '오늘' in date_text:
                return datetime.now()
            elif '어제' in date_text:
                return datetime.now() - timedelta(days=1)
            
            # 기본값: 현재 시간
            return timezone.now()
            
        except Exception as e:
            print(f"날짜 파싱 오류: {e}")
            return timezone.now()
    
    def save_news_to_db(self, news_articles):
        """뉴스 기사를 데이터베이스에 저장합니다."""
        saved_count = 0
        
        for article_data in news_articles:
            try:
                # 중복 체크 (URL과 제목으로 체크)
                if NewsArticle.objects.filter(
                    models.Q(url=article_data['url']) | 
                    models.Q(title=article_data['title'])
                ).exists():
                    continue
                
                # 기사 내용 가져오기 (시간이 오래 걸릴 수 있으므로 선택적으로)
                content = article_data['summary']  # 일단 요약을 내용으로 사용
                
                # 데이터베이스에 저장
                NewsArticle.objects.create(
                    title=article_data['title'],
                    content=content,
                    summary=article_data['summary'],
                    url=article_data['url'],
                    published_date=article_data['published_date'],
                    category=article_data['category']
                )
                
                saved_count += 1
                print(f"저장됨: {article_data['title']}")
                
            except Exception as e:
                print(f"뉴스 저장 중 오류: {e}")
                continue
        
        return saved_count
    
    def crawl_and_save(self, max_pages=2):
        """뉴스를 크롤링하고 데이터베이스에 저장합니다."""
        print("네이버 금융 뉴스 크롤링 시작...")
        
        # 뉴스 목록 가져오기
        news_articles = self.get_news_list(max_pages=max_pages)
        print(f"총 {len(news_articles)}개의 뉴스를 찾았습니다.")
        
        if not news_articles:
            print("뉴스를 찾을 수 없습니다. 샘플 뉴스를 생성합니다.")
            return self.create_sample_news()
        
        # 데이터베이스에 저장
        saved_count = self.save_news_to_db(news_articles)
        print(f"{saved_count}개의 새로운 뉴스를 저장했습니다.")
        
        return saved_count
    
    def create_sample_news(self):
        """샘플 뉴스를 생성합니다."""
        sample_news = [
            {
                'title': '코스피, 외국인 매수세에 상승 마감...2,600선 회복',
                'content': '코스피가 외국인의 순매수세에 힘입어 상승 마감했다. 반도체와 자동차 업종이 상승을 주도했으며, 개인투자자들의 매도세는 지속됐다.',
                'summary': '코스피가 외국인 매수세에 힘입어 2,600선을 회복하며 상승 마감했다.',
                'url': 'https://finance.naver.com/news/sample1',
                'category': '주식'
            },
            {
                'title': '한국은행, 기준금리 동결...경제 불확실성 고려',
                'content': '한국은행이 기준금리를 현 수준에서 동결하기로 결정했다. 글로벌 경제 불확실성과 국내 물가 상황을 종합적으로 고려한 결과다.',
                'summary': '한국은행이 경제 불확실성을 고려해 기준금리를 동결했다.',
                'url': 'https://finance.naver.com/news/sample2',
                'category': '금융'
            },
            {
                'title': '비트코인, 5만 달러 돌파...기관투자자 유입 지속',
                'content': '비트코인이 5만 달러를 돌파하며 강세를 이어가고 있다. 기관투자자들의 지속적인 유입이 상승 동력으로 작용하고 있다.',
                'summary': '비트코인이 기관투자자 유입에 힘입어 5만 달러를 돌파했다.',
                'url': 'https://finance.naver.com/news/sample3',
                'category': '투자'
            }
        ]
        
        saved_count = 0
        for news_data in sample_news:
            try:
                article, created = NewsArticle.objects.get_or_create(
                    url=news_data['url'],
                    defaults={
                        'title': news_data['title'],
                        'content': news_data['content'],
                        'summary': news_data['summary'],
                        'published_date': timezone.now() - timedelta(hours=saved_count),
                        'category': news_data['category']
                    }
                )
                if created:
                    saved_count += 1
                    print(f"샘플 뉴스 생성: {news_data['title']}")
            except Exception as e:
                print(f"샘플 뉴스 생성 오류: {e}")
        
        return saved_count
