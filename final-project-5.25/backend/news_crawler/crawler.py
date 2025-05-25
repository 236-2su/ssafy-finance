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
        """네이버 뉴스에서 경제/금융 뉴스를 가져옵니다."""
        news_articles = []
        
        try:
            # 네이버 금융 메인 페이지에서 직접 크롤링
            news_urls = [
                "https://finance.naver.com/"  # 네이버 금융 메인 페이지
            ]
            
            for news_url in news_urls:
                try:
                    print(f"크롤링 중: {news_url}")
                    response = requests.get(news_url, headers=self.headers)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # 네이버 금융 메인 페이지의 뉴스 섹션 선택자
                    news_selectors = [
                        '.news_area .news_list li',  # 뉴스 영역
                        '.section_news .news_list li',  # 섹션 뉴스
                        '.today_news .news_list li',  # 오늘의 뉴스
                        '.news_wrap .news_item',  # 뉴스 래퍼
                        '.news_section .news_list li',  # 뉴스 섹션
                        '.news_list li',  # 일반 뉴스 리스트
                        '.news_item',  # 뉴스 아이템
                        'a[href*="news"]'  # 뉴스 링크
                    ]
                    
                    news_items = []
                    for selector in news_selectors:
                        items = soup.select(selector)
                        news_items.extend(items)
                    
                    print(f"페이지에서 {len(news_items)}개의 뉴스 항목을 찾았습니다.")
                    
                    for item in news_items:
                        try:
                            # 제목과 링크 추출 (다양한 선택자 시도)
                            title_elem = item.select_one('a') or item if item.name == 'a' else None
                            if not title_elem:
                                continue
                                
                            title = title_elem.get_text(strip=True)
                            if not title or len(title) < 10:
                                continue
                                
                            href = title_elem.get('href')
                            if not href:
                                continue
                                
                            # 네이버 뉴스 URL 정규화
                            if href.startswith('/'):
                                full_url = 'https://news.naver.com' + href
                            elif href.startswith('http'):
                                full_url = href
                            else:
                                continue
                            
                            # 중복 제거
                            if any(article['url'] == full_url for article in news_articles):
                                continue
                            
                            # 요약 추출
                            summary = ""
                            summary_elem = item.select_one('dd, .news_dsc')
                            if summary_elem:
                                summary = summary_elem.get_text(strip=True)
                            
                            if not summary:
                                summary = title[:100] + "..." if len(title) > 100 else title
                            
                            # 썸네일 이미지 추출
                            image_url = ""
                            img_elem = item.select_one('img')
                            if img_elem:
                                img_src = img_elem.get('src') or img_elem.get('data-src')
                                if img_src:
                                    if img_src.startswith('//'):
                                        image_url = 'https:' + img_src
                                    elif img_src.startswith('/'):
                                        image_url = 'https://news.naver.com' + img_src
                                    elif img_src.startswith('http'):
                                        image_url = img_src
                            
                            # 날짜 추출
                            date_elem = item.select_one('.date')
                            published_date = timezone.now()
                            if date_elem:
                                date_text = date_elem.get_text(strip=True)
                                published_date = self.parse_date(date_text)
                            
                            # 카테고리 결정
                            category = '경제'
                            if '258' in news_url:
                                category = '증권'
                            elif '259' in news_url:
                                category = '금융'
                            elif '260' in news_url:
                                category = '산업'
                            elif '261' in news_url:
                                category = '벤처'
                            elif '771' in news_url:
                                category = '부동산'
                            
                            news_articles.append({
                                'title': title,
                                'url': full_url,
                                'published_date': published_date,
                                'summary': summary,
                                'category': category,
                                'image_url': image_url
                            })
                            
                            print(f"뉴스 발견: {title[:50]}...")
                            
                        except Exception as e:
                            print(f"뉴스 항목 처리 중 오류: {e}")
                            continue
                    
                    time.sleep(1)  # 요청 간 딜레이
                    
                except Exception as e:
                    print(f"뉴스 페이지 크롤링 중 오류: {e}")
                    continue
                
        except Exception as e:
            print(f"뉴스 크롤링 중 전체 오류: {e}")
        
        print(f"총 {len(news_articles)}개의 뉴스를 수집했습니다.")
        return news_articles[:20]  # 최대 20개 뉴스만 반환
    
    def get_article_content_and_image(self, url):
        """개별 뉴스 기사의 내용과 이미지를 가져옵니다."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 이미지 추출 (우선순위 순서)
            image_url = ""
            image_selectors = [
                '#img1',  # 네이버 뉴스 메인 이미지
                '.end-photo img',  # 네이버 뉴스 본문 이미지
                '.article_photo img',  # 기사 사진
                '.news_photo img',  # 뉴스 사진
                '.photo img',  # 일반 사진
                'article img',  # 기사 내 이미지
                '.content img',  # 컨텐츠 이미지
                'img[src*="phinf.pstatic.net"]',  # 네이버 이미지 서버
                'img[src*="imgnews.pstatic.net"]',  # 네이버 뉴스 이미지 서버
                'img'  # 모든 이미지 (마지막 수단)
            ]
            
            for selector in image_selectors:
                img_elem = soup.select_one(selector)
                if img_elem:
                    img_src = img_elem.get('src') or img_elem.get('data-src')
                    if img_src:
                        # 이미지 URL 정규화
                        if img_src.startswith('//'):
                            image_url = 'https:' + img_src
                        elif img_src.startswith('/'):
                            image_url = 'https://finance.naver.com' + img_src
                        elif img_src.startswith('http'):
                            image_url = img_src
                        
                        # 유효한 이미지인지 확인 (크기 체크)
                        if image_url and self.is_valid_image(image_url):
                            break
                        else:
                            image_url = ""
            
            # 본문 내용 추출
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
            
            return {
                'content': content if content else "내용을 가져올 수 없습니다.",
                'image_url': image_url
            }
            
        except Exception as e:
            print(f"기사 내용 및 이미지 추출 중 오류: {e}")
            return {
                'content': "내용을 가져올 수 없습니다.",
                'image_url': ""
            }
    
    def is_valid_image(self, image_url):
        """이미지 URL이 유효한지 확인합니다."""
        try:
            # 너무 작은 이미지나 아이콘 제외
            if any(keyword in image_url.lower() for keyword in ['icon', 'logo', 'btn', 'arrow', 'bullet']):
                return False
            
            # 이미지 크기 확인 (HEAD 요청으로 빠르게 체크)
            response = requests.head(image_url, headers=self.headers, timeout=5)
            content_type = response.headers.get('content-type', '')
            
            # 이미지 타입인지 확인
            if not content_type.startswith('image/'):
                return False
            
            # 파일 크기 확인 (너무 작으면 아이콘일 가능성)
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) < 5000:  # 5KB 미만은 제외
                return False
            
            return True
            
        except Exception:
            return False
    
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
    
    def get_finance_related_image(self, title, category):
        """뉴스 제목과 카테고리에 따라 금융 관련 이미지를 반환합니다."""
        title_lower = title.lower()
        
        # 더 세밀한 키워드 분석으로 다양한 이미지 제공
        
        # 주식 관련 세부 키워드
        if any(keyword in title_lower for keyword in ['코스피', '코스닥', '상승', '하락', '급등', '급락']):
            stock_images = [
                'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400&h=300&fit=crop&auto=format',  # 주식 차트
                'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=400&h=300&fit=crop&auto=format',  # 주식 그래프
                'https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=400&h=300&fit=crop&auto=format',  # 주식 데이터
            ]
            return stock_images[hash(title) % len(stock_images)]
        
        # ETF/펀드 관련
        elif any(keyword in title_lower for keyword in ['etf', '펀드', '투자', '수익률', '배당']):
            fund_images = [
                'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=400&h=300&fit=crop&auto=format',  # 투자 차트
                'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop&auto=format',  # 비즈니스 차트
                'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=300&fit=crop&auto=format',  # 데이터 분석
            ]
            return fund_images[hash(title) % len(fund_images)]
        
        # 은행/금리 관련
        elif any(keyword in title_lower for keyword in ['은행', '금리', '대출', '예금', '적금']):
            bank_images = [
                'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400&h=300&fit=crop&auto=format',  # 은행 건물
                'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=300&fit=crop&auto=format',  # 금융 서비스
                'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=400&h=300&fit=crop&auto=format',  # 은행 내부
            ]
            return bank_images[hash(title) % len(bank_images)]
        
        # 암호화폐 관련
        elif any(keyword in title_lower for keyword in ['비트코인', '이더리움', '암호화폐', '코인', '블록체인']):
            crypto_images = [
                'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=300&fit=crop&auto=format',  # 비트코인
                'https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=400&h=300&fit=crop&auto=format',  # 암호화폐
                'https://images.unsplash.com/photo-1518546305927-5a555bb7020d?w=400&h=300&fit=crop&auto=format',  # 블록체인
            ]
            return crypto_images[hash(title) % len(crypto_images)]
        
        # 부동산 관련
        elif any(keyword in title_lower for keyword in ['부동산', '아파트', '주택', '임대', '전세', '매매']):
            real_estate_images = [
                'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&h=300&fit=crop&auto=format',  # 부동산
                'https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=400&h=300&fit=crop&auto=format',  # 아파트
                'https://images.unsplash.com/photo-1448630360428-65456885c650?w=400&h=300&fit=crop&auto=format',  # 주택
            ]
            return real_estate_images[hash(title) % len(real_estate_images)]
        
        # 기업/산업 관련
        elif any(keyword in title_lower for keyword in ['기업', '회사', '산업', '제조', '서비스', '매출']):
            business_images = [
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop&auto=format',  # 비즈니스 미팅
                'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400&h=300&fit=crop&auto=format',  # 오피스 빌딩
                'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&h=300&fit=crop&auto=format',  # 비즈니스 데스크
            ]
            return business_images[hash(title) % len(business_images)]
        
        # 경제/환율 관련
        elif any(keyword in title_lower for keyword in ['경제', '물가', 'gdp', '인플레이션', '환율', '달러']):
            economy_images = [
                'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400&h=300&fit=crop&auto=format',  # 경제 지표
                'https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=400&h=300&fit=crop&auto=format',  # 달러
                'https://images.unsplash.com/photo-1633158829585-23ba8f7c8caf?w=400&h=300&fit=crop&auto=format',  # 글로벌 경제
            ]
            return economy_images[hash(title) % len(economy_images)]
        
        # 기본 금융 이미지들
        else:
            default_images = [
                'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400&h=300&fit=crop&auto=format',  # 일반 금융
                'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400&h=300&fit=crop&auto=format',  # 차트
                'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=400&h=300&fit=crop&auto=format',  # 비즈니스
            ]
            return default_images[hash(title) % len(default_images)]
    
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
                
                # 개별 뉴스 페이지에서 상세 내용과 이미지 가져오기
                article_details = self.get_article_content_and_image(article_data['url'])
                
                # 이미지 URL 결정 (개별 페이지에서 가져온 것을 우선, 없으면 목록에서 가져온 것 사용)
                final_image_url = article_details['image_url'] or article_data.get('image_url', '')
                
                # 실제 뉴스 사이트에서 이미지를 찾지 못하면 금융 관련 이미지 사용
                if not final_image_url:
                    final_image_url = self.get_finance_related_image(article_data['title'], article_data['category'])
                
                # 데이터베이스에 저장
                NewsArticle.objects.create(
                    title=article_data['title'],
                    content=article_details['content'],
                    summary=article_data['summary'],
                    url=article_data['url'],
                    published_date=article_data['published_date'],
                    category=article_data['category'],
                    image_url=final_image_url
                )
                
                saved_count += 1
                print(f"저장됨: {article_data['title']} (이미지: {'있음' if final_image_url else '없음'})")
                
                # 요청 간 딜레이 (서버 부하 방지)
                time.sleep(0.5)
                
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
                'category': '주식',
                'image_url': self.get_finance_related_image('코스피, 외국인 매수세에 상승 마감...2,600선 회복', '주식')
            },
            {
                'title': '한국은행, 기준금리 동결...경제 불확실성 고려',
                'content': '한국은행이 기준금리를 현 수준에서 동결하기로 결정했다. 글로벌 경제 불확실성과 국내 물가 상황을 종합적으로 고려한 결과다.',
                'summary': '한국은행이 경제 불확실성을 고려해 기준금리를 동결했다.',
                'url': 'https://finance.naver.com/news/sample2',
                'category': '금융',
                'image_url': self.get_finance_related_image('한국은행, 기준금리 동결...경제 불확실성 고려', '금융')
            },
            {
                'title': '비트코인, 5만 달러 돌파...기관투자자 유입 지속',
                'content': '비트코인이 5만 달러를 돌파하며 강세를 이어가고 있다. 기관투자자들의 지속적인 유입이 상승 동력으로 작용하고 있다.',
                'summary': '비트코인이 기관투자자 유입에 힘입어 5만 달러를 돌파했다.',
                'url': 'https://finance.naver.com/news/sample3',
                'category': '투자',
                'image_url': self.get_finance_related_image('비트코인, 5만 달러 돌파...기관투자자 유입 지속', '투자')
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
                        'category': news_data['category'],
                        'image_url': news_data.get('image_url', '')
                    }
                )
                if created:
                    saved_count += 1
                    print(f"샘플 뉴스 생성: {news_data['title']}")
            except Exception as e:
                print(f"샘플 뉴스 생성 오류: {e}")
        
        return saved_count
