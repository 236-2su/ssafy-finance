import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from .models import NewsArticle
import re
import time
import urllib.parse


class NaverFinanceCrawler:
    def __init__(self):
        self.base_url = "https://finance.naver.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    def get_news_list(self, max_pages=2):
        """네이버 뉴스에서 경제/금융 뉴스를 가져옵니다."""
        news_articles = []

        try:
            # 네이버 금융 메인 페이지에서 직접 크롤링
            news_urls = ["https://finance.naver.com/"]  # 네이버 금융 메인 페이지

            for news_url in news_urls:
                try:
                    print(f"크롤링 중: {news_url}")
                    response = requests.get(news_url, headers=self.headers)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, "html.parser")

                    # 네이버 금융 메인 페이지의 뉴스 섹션 선택자
                    news_selectors = [
                        ".news_area .news_list li",  # 뉴스 영역
                        ".section_news .news_list li",  # 섹션 뉴스
                        ".today_news .news_list li",  # 오늘의 뉴스
                        ".news_wrap .news_item",  # 뉴스 래퍼
                        ".news_section .news_list li",  # 뉴스 섹션
                        ".news_list li",  # 일반 뉴스 리스트
                        ".news_item",  # 뉴스 아이템
                        'a[href*="news"]',  # 뉴스 링크
                    ]

                    news_items = []
                    for selector in news_selectors:
                        items = soup.select(selector)
                        news_items.extend(items)

                    print(f"페이지에서 {len(news_items)}개의 뉴스 항목을 찾았습니다.")

                    for item in news_items:
                        try:
                            # 제목과 링크 추출 (다양한 선택자 시도)
                            title_elem = (
                                item.select_one("a") or item
                                if item.name == "a"
                                else None
                            )
                            if not title_elem:
                                continue

                            title = title_elem.get_text(strip=True)
                            if not title or len(title) < 10:
                                continue

                            href = title_elem.get("href")
                            if not href:
                                continue

                            # 네이버 뉴스 URL 정규화 (JavaScript 변환 로직 반영)
                            full_url = ""
                            parsed_href = urllib.parse.urlparse(
                                href
                            )  # requests.utils.urlparse -> urllib.parse.urlparse

                            if href.startswith(
                                "/news/news_read.naver"
                            ) or href.startswith("/news/newsRead.naver"):
                                query_params = urllib.parse.parse_qs(  # requests.utils.parse_qs -> urllib.parse.parse_qs
                                    parsed_href.query
                                )
                                office_id = (
                                    query_params.get("office_id", [None])[0]
                                    or query_params.get("officeId", [None])[0]
                                )
                                article_id = (
                                    query_params.get("article_id", [None])[0]
                                    or query_params.get("articleId", [None])[0]
                                )
                                if office_id and article_id:
                                    full_url = f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}"
                                else:
                                    print(
                                        f"office_id 또는 article_id를 찾을 수 없음: {href}"
                                    )
                                    continue
                            elif href.startswith("http"):
                                if (
                                    "news.naver.com/article/" in href
                                    or "n.news.naver.com/article/" in href
                                    or href.startswith(
                                        "https://finance.naver.com/item/news_read.naver"
                                    )
                                ):
                                    full_url = href
                            elif href.startswith("/item/news_read.naver"):
                                full_url = self.base_url + href
                            elif href.startswith(
                                "/article/"
                            ):  # n.news.naver.com 또는 news.naver.com
                                full_url = (
                                    "https://n.news.naver.com" + href
                                )  # n.news.naver.com 우선

                            if not full_url:
                                # print(f"유효한 URL로 변환 실패, 건너뜀: {href}")
                                continue

                            # 중복 제거 (news_articles 리스트 내에서)
                            if any(
                                article["url"] == full_url for article in news_articles
                            ):
                                # print(f"이미 수집된 URL 건너뜀: {full_url}")
                                continue

                            # 요약 추출
                            summary = ""
                            summary_elem = item.select_one("dd, .news_dsc")
                            if summary_elem:
                                summary = summary_elem.get_text(strip=True)

                            if not summary:
                                summary = (
                                    title[:100] + "..." if len(title) > 100 else title
                                )

                            # 썸네일 이미지 추출
                            image_url = ""
                            img_elem = item.select_one("img")
                            if img_elem:
                                img_src = img_elem.get("src") or img_elem.get(
                                    "data-src"
                                )
                                if img_src:
                                    if img_src.startswith("//"):
                                        image_url = "https:" + img_src
                                    elif img_src.startswith("/"):
                                        image_url = "https://news.naver.com" + img_src
                                    elif img_src.startswith("http"):
                                        image_url = img_src

                            # 날짜 추출
                            date_elem = item.select_one(".date")
                            published_date = timezone.now()
                            if date_elem:
                                date_text = date_elem.get_text(strip=True)
                                published_date = self.parse_date(date_text)

                            # 카테고리 결정
                            category = "경제"
                            if "258" in news_url:
                                category = "증권"
                            elif "259" in news_url:
                                category = "금융"
                            elif "260" in news_url:
                                category = "산업"
                            elif "261" in news_url:
                                category = "벤처"
                            elif "771" in news_url:
                                category = "부동산"

                            news_articles.append(
                                {
                                    "title": title,
                                    "url": full_url,
                                    "published_date": published_date,
                                    "summary": summary,
                                    "category": category,
                                    "image_url": image_url,
                                }
                            )

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

        # URL 기준으로 최종 중복 제거
        unique_articles_by_url = {article["url"]: article for article in news_articles}
        final_news_articles = list(unique_articles_by_url.values())

        print(f"중복 제거 후 {len(final_news_articles)}개의 뉴스를 수집했습니다.")
        return final_news_articles[:20]  # 최대 20개 뉴스만 반환

    def get_article_content_and_image(self, url):
        """개별 뉴스 기사의 내용과 이미지를 가져옵니다."""
        try:
            # URL 유효성 검사 (네이버 뉴스 도메인 확인)
            if not (
                url.startswith("https://news.naver.com/")
                or url.startswith("https://n.news.naver.com/")
                or url.startswith("https://finance.naver.com/item/news_read.naver")
            ):
                print(f"유효하지 않은 뉴스 URL입니다 (도메인 불일치): {url}")
                return {"content": "유효하지 않은 URL입니다.", "image_url": ""}

            session = requests.Session()
            session.headers.update(self.headers)

            # finance.naver.com/item/news_read.naver 형태의 URL 처리
            if url.startswith("https://finance.naver.com/item/news_read.naver"):
                print(f"종목 뉴스 페이지 처리 시도: {url}")
                try:
                    response = session.get(url, timeout=15, allow_redirects=True)
                    response.raise_for_status()
                    soup_finance_item = BeautifulSoup(response.content, "html.parser")

                    # 이 페이지에서 실제 기사 링크를 찾음 (더 다양한 선택자 시도)
                    # 1. news_read_default 클래스 내부의 news_read_tit a 태그
                    # 2. news_read_default 클래스 내부의 news_read_btn a 태그 (기사원문보기)
                    # 3. news_end_area 내부의 btn_news_origin 클래스를 가진 a 태그
                    # 4. iframe#news_frame 의 src 속성
                    actual_article_link = None
                    link_selectors = [
                        '.news_read_default .news_read_tit a[href*="news.naver.com"]',
                        '.news_read_default .news_read_tit a[href*="n.news.naver.com"]',
                        '.news_read_default .news_read_btn a[href*="news.naver.com"]',
                        '.news_read_default .news_read_btn a[href*="n.news.naver.com"]',
                        '.news_end_area a.btn_news_origin[href*="news.naver.com"]',
                        '.news_end_area a.btn_news_origin[href*="n.news.naver.com"]',
                        '#content .section_news .news_read a[href*="news.naver.com"]',  # 기존 선택자 유지
                        '#content .section_news .news_read a[href*="n.news.naver.com"]',  # 기존 선택자 유지
                    ]
                    for selector in link_selectors:
                        elem = soup_finance_item.select_one(selector)
                        if elem and elem.get("href"):
                            actual_article_link = elem["href"]
                            break

                    if actual_article_link:
                        print(
                            f"종목 뉴스 페이지에서 실제 기사 URL 발견 (a태그): {actual_article_link}"
                        )
                        url = actual_article_link
                    else:
                        iframe_elem = soup_finance_item.select_one("iframe#news_frame")
                        if iframe_elem and iframe_elem.get("src"):
                            iframe_src = iframe_elem["src"]
                            if iframe_src.startswith("http") and (
                                "news.naver.com" in iframe_src
                                or "n.news.naver.com" in iframe_src
                            ):
                                print(
                                    f"종목 뉴스 페이지에서 iframe src 발견: {iframe_src}"
                                )
                                url = iframe_src
                            else:
                                print(
                                    f"종목 뉴스 페이지에서 유효한 실제 기사 링크 또는 iframe src를 찾지 못했습니다: {url}"
                                )
                                return {
                                    "content": "종목 뉴스에서 실제 기사 링크/iframe을 찾지 못했습니다.",
                                    "image_url": "",
                                }
                        else:
                            print(
                                f"종목 뉴스 페이지에서 유효한 실제 기사 링크 또는 iframe을 찾지 못했습니다: {url}"
                            )
                            return {
                                "content": "종목 뉴스에서 실제 기사 링크/iframe을 찾지 못했습니다.",
                                "image_url": "",
                            }

                    # 추출된 URL이 네이버 뉴스 도메인이 아니면 실패 처리
                    if not (
                        url.startswith("https://news.naver.com/")
                        or url.startswith("https://n.news.naver.com/")
                    ):
                        print(f"추출된 실제 기사 URL이 유효하지 않음 (도메인): {url}")
                        return {
                            "content": "종목 뉴스에서 유효한 실제 기사 링크를 찾지 못했습니다.",
                            "image_url": "",
                        }
                except requests.exceptions.RequestException as e:
                    print(f"종목 뉴스 페이지 요청 실패 ({url}): {e}")
                    return {
                        "content": f"종목 뉴스 페이지 접근 실패: {e}",
                        "image_url": "",
                    }

            # 실제 기사 페이지 (또는 종목 뉴스에서 추출된 URL)에 대한 요청
            try:
                response = session.get(url, timeout=15, allow_redirects=True)
                response.raise_for_status()
                final_url = response.url
                if url != final_url:
                    print(f"URL 리디렉션됨: {url} -> {final_url}")
                    if not (
                        final_url.startswith("https://news.naver.com/")
                        or final_url.startswith("https://n.news.naver.com/")
                    ):  # finance.naver.com/item/news_read.naver는 이미 위에서 처리됨
                        print(f"리디렉션된 최종 URL이 유효하지 않음: {final_url}")
                        return {
                            "content": "리디렉션 후 유효하지 않은 URL입니다.",
                            "image_url": "",
                        }
                    url = final_url
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"404 Not Found 오류 발생 (최종 URL: {url})")
                    # 모바일 재시도 로직은 finance.naver.com/item/news_read.naver 에 대해서만 유효했으므로,
                    # 일반 news.naver.com 이나 n.news.naver.com 에서 404면 그냥 실패 처리.
                    return {
                        "content": f"404 오류로 내용을 가져올 수 없습니다: {e.response.status_code}",
                        "image_url": "",
                    }
                else:
                    raise

            soup = BeautifulSoup(response.content, "html.parser")

            # 이미지 추출 (메타 태그 우선 확인: og:image, twitter:image)
            image_url = ""
            meta_image_selectors = [
                'meta[property="og:image"]',
                'meta[name="twitter:image"]',
            ]
            for meta_selector in meta_image_selectors:
                meta_tag = soup.select_one(meta_selector)
                if meta_tag and meta_tag.get("content"):
                    image_url = meta_tag["content"]
                    if self.is_valid_image(image_url):
                        print(
                            f"메타 태그에서 이미지 발견 ({meta_selector}): {image_url}"
                        )
                        break  # 유효한 이미지 찾으면 중단
                    else:
                        image_url = ""  # 유효하지 않으면 다음 메타 태그 시도
                if image_url:
                    break  # 첫번째 메타태그에서 찾았으면 두번째는 시도 안함

            if (
                not image_url
            ):  # 메타 태그에서 이미지를 못 찾거나 유효하지 않으면 다른 선택자 시도
                print(
                    "메타 태그에서 유효한 이미지를 찾지 못했습니다. 본문 이미지 검색 중..."
                )
                image_selectors = [
                    "#img1",
                    ".end_photo_org img",
                    ".newsct_body .newsct_article img",  # 뉴스 본문 내 이미지 (좀 더 구체적)
                    "#articleBodyContents img",
                    "._article_content img",
                    ".article_photo img",
                    ".news_photo img",
                    ".photo img",
                    "article img",
                    ".content img",
                    'img[src*="phinf.pstatic.net"]',
                    'img[src*="imgnews.pstatic.net"]',
                    "img",
                ]

                for selector in image_selectors:
                    img_elem = soup.select_one(selector)
                    if img_elem:
                        img_src = img_elem.get("src") or img_elem.get("data-src")
                        if img_src:
                            parsed_url = requests.utils.urlparse(url)
                            base_article_url = (
                                f"{parsed_url.scheme}://{parsed_url.netloc}"
                            )
                            if img_src.startswith("//"):
                                image_url = "https:" + img_src
                            elif img_src.startswith("/"):
                                image_url = base_article_url + img_src
                            elif img_src.startswith("http"):
                                image_url = img_src

                            if image_url and self.is_valid_image(image_url):
                                print(
                                    f"본문 선택자 '{selector}'에서 이미지 발견: {image_url}"
                                )
                                break
                            else:
                                image_url = ""
            if not image_url:
                print(f"기사에서 유효한 이미지를 찾지 못했습니다: {url}")

            # 본문 내용 추출
            content = ""
            content_selectors = [
                "#dic_area",
                "#newsct_article",
                "#articleBody",  # 연합뉴스 등 일부 언론사
                ".article_view",  # 일반적인 기사 뷰 클래스
                "#articleBodyContents",
                "._article_content",
                ".article_body",
                ".news_body",
                ".article_content",
                ".content",
                ".news_content",
                "article",  # article 태그 전체 (최후의 수단)
            ]

            print(f"본문 내용 추출 시도: {url}")
            for idx, selector in enumerate(content_selectors):
                content_elem = soup.select_one(selector)
                if content_elem:
                    print(
                        f"본문 선택자 '{selector}' (시도 {idx+1}/{len(content_selectors)}) 사용됨."
                    )
                    for tag_selector in [
                        "script",
                        "style",
                        ".ad",
                        ".advertisement",
                        ".related",
                        ".comment",
                        ".byline",
                        ".journalist_area",
                        ".copyright",
                        "figure",
                        "figcaption",
                        ".embed_photo",
                        ".vod_player",  # 이미지/비디오 관련 태그 제외
                        ".promotion_area",
                        ".link_news",
                        ".social_bt_area",  # 프로모션, 관련뉴스, 소셜버튼 제외
                    ]:
                        for tag in content_elem.select(tag_selector):
                            tag.decompose()

                    text_parts = [
                        elem.get_text(strip=True)
                        for elem in content_elem.find_all(["p", "div"], recursive=True)
                        if elem.get_text(strip=True)
                    ]

                    if not text_parts:  # p, div 에서 못찾으면 전체 텍스트 시도
                        text_parts = [
                            element.strip()
                            for element in content_elem.find_all(
                                string=True, recursive=True
                            )
                            if element.strip()
                        ]

                    content = "\n\n".join(text_parts)  # 문단 구분을 위해 \n\n 사용
                    content = re.sub(r"\n\s*\n", "\n\n", content)  # 중복 줄바꿈 제거

                    if len(content) > 30:  # 최소 내용 길이 30자로 줄임
                        print(f"본문 내용 추출 성공 (길이: {len(content)}).")
                        break
                    else:
                        print(
                            f"선택자 '{selector}'로 추출된 내용이 너무 짧습니다 (길이: {len(content)}). 다음 선택자 시도..."
                        )
                        content = ""  # 짧으면 다음 선택자 위해 초기화
                else:
                    print(
                        f"본문 선택자 '{selector}' (시도 {idx+1}/{len(content_selectors)}) 찾을 수 없음."
                    )

            if not content:
                print(f"모든 선택자로 본문 내용을 가져오지 못했습니다: {url}")
                # 최후의 수단으로 body 전체 텍스트 시도 (매우 지저분할 수 있음)
                body_text = (
                    soup.body.get_text(separator="\n", strip=True) if soup.body else ""
                )
                if len(body_text) > 100:  # 최소 길이 만족하면
                    content = body_text[:1000] + "..."  # 너무 길면 자르기
                    print(
                        f"최후의 수단으로 body 텍스트 일부 사용 (길이: {len(content)})"
                    )

            final_content = content if content else "기사 본문을 가져올 수 없습니다."
            print(f"최종 추출된 내용 길이: {len(final_content)} (URL: {url})")
            return {
                "content": final_content,
                "image_url": image_url,
            }

        except requests.exceptions.RequestException as e:
            print(f"기사 내용 및 이미지 추출 중 네트워크 오류 ({url}): {e}")
            return {
                "content": f"네트워크 오류로 내용을 가져올 수 없습니다: {e}",
                "image_url": "",
            }
        except Exception as e:
            print(f"기사 내용 및 이미지 추출 중 예기치 않은 오류 ({url}): {e}")
            return {
                "content": f"오류로 내용을 가져올 수 없습니다: {e}",
                "image_url": "",
            }

    def is_valid_image(self, image_url):
        """이미지 URL이 유효한지 확인합니다."""
        try:
            # 너무 작은 이미지나 아이콘 제외
            if any(
                keyword in image_url.lower()
                for keyword in ["icon", "logo", "btn", "arrow", "bullet"]
            ):
                return False

            # 이미지 크기 확인 (HEAD 요청으로 빠르게 체크)
            # User-Agent를 명시해야 차단 방지 가능성 높임
            img_headers = self.headers.copy()
            response = requests.head(
                image_url, headers=img_headers, timeout=5, allow_redirects=True
            )
            response.raise_for_status()  # 오류 발생 시 예외 처리

            content_type = response.headers.get("content-type", "").lower()

            # 이미지 타입인지 확인 (다양한 이미지 타입 허용)
            if not any(
                img_type in content_type
                for img_type in ["image/jpeg", "image/png", "image/gif", "image/webp"]
            ):
                print(f"유효하지 않은 이미지 타입: {content_type} ({image_url})")
                return False

            # 파일 크기 확인 (너무 작으면 아이콘일 가능성, 3KB 미만 제외)
            content_length = response.headers.get("content-length")
            if content_length and int(content_length) < 3000:  # 3KB 미만은 제외
                print(f"너무 작은 이미지 파일: {content_length} bytes ({image_url})")
                return False

            return True

        except requests.exceptions.RequestException as e:
            print(f"이미지 유효성 검사 중 네트워크 오류: {e} ({image_url})")
            return False
        except Exception as e:
            print(f"이미지 유효성 검사 중 일반 오류: {e} ({image_url})")
            return False

    def parse_date(self, date_text):
        """날짜 텍스트를 파싱합니다."""
        try:
            # "2024.01.15" 형식
            if re.match(r"\d{4}\.\d{2}\.\d{2}", date_text):
                date_part = re.search(r"\d{4}\.\d{2}\.\d{2}", date_text).group()
                return datetime.strptime(date_part, "%Y.%m.%d")

            # "01.15" 형식 (올해)
            if re.match(r"\d{2}\.\d{2}", date_text):
                current_year = datetime.now().year
                date_with_year = f"{current_year}.{date_text}"
                return datetime.strptime(date_with_year, "%Y.%m.%d")

            # "오늘", "어제" 등
            if "오늘" in date_text:
                return datetime.now()
            elif "어제" in date_text:
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
        if any(
            keyword in title_lower
            for keyword in ["코스피", "코스닥", "상승", "하락", "급등", "급락"]
        ):
            stock_images = [
                "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400&h=300&fit=crop&auto=format",  # 주식 차트
                "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=400&h=300&fit=crop&auto=format",  # 주식 그래프
                "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=400&h=300&fit=crop&auto=format",  # 주식 데이터
            ]
            return stock_images[hash(title) % len(stock_images)]

        # ETF/펀드 관련
        elif any(
            keyword in title_lower
            for keyword in ["etf", "펀드", "투자", "수익률", "배당"]
        ):
            fund_images = [
                "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=400&h=300&fit=crop&auto=format",  # 투자 차트
                "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop&auto=format",  # 비즈니스 차트
                "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=300&fit=crop&auto=format",  # 데이터 분석
            ]
            return fund_images[hash(title) % len(fund_images)]

        # 은행/금리 관련
        elif any(
            keyword in title_lower
            for keyword in ["은행", "금리", "대출", "예금", "적금"]
        ):
            bank_images = [
                "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400&h=300&fit=crop&auto=format",  # 은행 건물
                "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=300&fit=crop&auto=format",  # 금융 서비스
                "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=400&h=300&fit=crop&auto=format",  # 은행 내부
            ]
            return bank_images[hash(title) % len(bank_images)]

        # 암호화폐 관련
        elif any(
            keyword in title_lower
            for keyword in ["비트코인", "이더리움", "암호화폐", "코인", "블록체인"]
        ):
            crypto_images = [
                "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400&h=300&fit=crop&auto=format",  # 비트코인
                "https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=400&h=300&fit=crop&auto=format",  # 암호화폐
                "https://images.unsplash.com/photo-1518546305927-5a555bb7020d?w=400&h=300&fit=crop&auto=format",  # 블록체인
            ]
            return crypto_images[hash(title) % len(crypto_images)]

        # 부동산 관련
        elif any(
            keyword in title_lower
            for keyword in ["부동산", "아파트", "주택", "임대", "전세", "매매"]
        ):
            real_estate_images = [
                "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&h=300&fit=crop&auto=format",  # 부동산
                "https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=400&h=300&fit=crop&auto=format",  # 아파트
                "https://images.unsplash.com/photo-1448630360428-65456885c650?w=400&h=300&fit=crop&auto=format",  # 주택
            ]
            return real_estate_images[hash(title) % len(real_estate_images)]

        # 기업/산업 관련
        elif any(
            keyword in title_lower
            for keyword in ["기업", "회사", "산업", "제조", "서비스", "매출"]
        ):
            business_images = [
                "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop&auto=format",  # 비즈니스 미팅
                "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400&h=300&fit=crop&auto=format",  # 오피스 빌딩
                "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&h=300&fit=crop&auto=format",  # 비즈니스 데스크
            ]
            return business_images[hash(title) % len(business_images)]

        # 경제/환율 관련
        elif any(
            keyword in title_lower
            for keyword in ["경제", "물가", "gdp", "인플레이션", "환율", "달러"]
        ):
            economy_images = [
                "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400&h=300&fit=crop&auto=format",  # 경제 지표
                "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=400&h=300&fit=crop&auto=format",  # 달러
                "https://images.unsplash.com/photo-1633158829585-23ba8f7c8caf?w=400&h=300&fit=crop&auto=format",  # 글로벌 경제
            ]
            return economy_images[hash(title) % len(economy_images)]

        # 기본 금융 이미지들
        else:
            default_images = [
                "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400&h=300&fit=crop&auto=format",  # 일반 금융
                "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400&h=300&fit=crop&auto=format",  # 차트
                "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=400&h=300&fit=crop&auto=format",  # 비즈니스
            ]
            return default_images[hash(title) % len(default_images)]

    def save_news_to_db(self, news_articles):
        """뉴스 기사를 데이터베이스에 저장합니다."""
        saved_count = 0
        processed_urls = set()  # 한 번의 crawl_and_save 호출 내에서 중복 처리 방지

        for article_data in news_articles:
            try:
                # 현재 세션에서 이미 처리된 URL인지 확인
                if article_data["url"] in processed_urls:
                    print(
                        f"현재 세션에서 이미 처리된 URL 건너뜀: {article_data['url']}"
                    )
                    continue

                # DB 중복 체크 (URL만으로 체크)
                if NewsArticle.objects.filter(url=article_data["url"]).exists():
                    print(f"DB에 이미 존재하는 URL 건너뜀: {article_data['url']}")
                    processed_urls.add(
                        article_data["url"]
                    )  # DB에 있어도 현재 세션에서는 처리한 것으로 간주
                    continue

                processed_urls.add(
                    article_data["url"]
                )  # 현재 세션에서 처리할 URL로 등록

                # 개별 뉴스 페이지에서 상세 내용과 이미지 가져오기
                article_details = self.get_article_content_and_image(
                    article_data["url"]
                )

                # 내용이 없거나 오류 메시지인 경우 저장하지 않음
                error_messages = [
                    "내용을 가져올 수 없습니다",
                    "유효하지 않은 URL입니다",
                    "종목 뉴스에서 실제 기사 링크를 찾지 못했습니다",
                    "네트워크 오류",
                    "404 오류",
                ]
                if (
                    not article_details["content"]
                    or any(msg in article_details["content"] for msg in error_messages)
                    or len(article_details["content"]) < 50
                ):  # 내용이 너무 짧은 경우도 제외
                    print(
                        f"내용이 없거나 오류, 또는 너무 짧아 저장하지 않음: {article_data['url']} (내용: {article_details['content'][:100]}...)"
                    )
                    continue

                # 이미지 URL 결정 (개별 페이지에서 가져온 것을 우선, 없으면 목록에서 가져온 것 사용)
                final_image_url = article_details["image_url"] or article_data.get(
                    "image_url", ""
                )

                # 실제 뉴스 사이트에서 이미지를 찾지 못하면 금융 관련 이미지 사용
                if not final_image_url:
                    final_image_url = self.get_finance_related_image(
                        article_data["title"], article_data["category"]
                    )

                # 데이터베이스에 저장
                NewsArticle.objects.create(
                    title=article_data["title"],
                    content=article_details["content"],
                    summary=article_data["summary"],
                    url=article_data["url"],
                    published_date=article_data["published_date"],
                    category=article_data["category"],
                    image_url=final_image_url,
                )

                saved_count += 1
                print(
                    f"저장됨: {article_data['title']} (이미지: {'있음' if final_image_url else '없음'})"
                )

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
                "title": "코스피, 외국인 매수세에 상승 마감...2,600선 회복",
                "content": "코스피가 외국인의 순매수세에 힘입어 상승 마감했다. 반도체와 자동차 업종이 상승을 주도했으며, 개인투자자들의 매도세는 지속됐다.",
                "summary": "코스피가 외국인 매수세에 힘입어 2,600선을 회복하며 상승 마감했다.",
                "url": "https://finance.naver.com/news/sample1",
                "category": "주식",
                "image_url": self.get_finance_related_image(
                    "코스피, 외국인 매수세에 상승 마감...2,600선 회복", "주식"
                ),
            },
            {
                "title": "한국은행, 기준금리 동결...경제 불확실성 고려",
                "content": "한국은행이 기준금리를 현 수준에서 동결하기로 결정했다. 글로벌 경제 불확실성과 국내 물가 상황을 종합적으로 고려한 결과다.",
                "summary": "한국은행이 경제 불확실성을 고려해 기준금리를 동결했다.",
                "url": "https://finance.naver.com/news/sample2",
                "category": "금융",
                "image_url": self.get_finance_related_image(
                    "한국은행, 기준금리 동결...경제 불확실성 고려", "금융"
                ),
            },
            {
                "title": "비트코인, 5만 달러 돌파...기관투자자 유입 지속",
                "content": "비트코인이 5만 달러를 돌파하며 강세를 이어가고 있다. 기관투자자들의 지속적인 유입이 상승 동력으로 작용하고 있다.",
                "summary": "비트코인이 기관투자자 유입에 힘입어 5만 달러를 돌파했다.",
                "url": "https://finance.naver.com/news/sample3",
                "category": "투자",
                "image_url": self.get_finance_related_image(
                    "비트코인, 5만 달러 돌파...기관투자자 유입 지속", "투자"
                ),
            },
        ]

        saved_count = 0
        for news_data in sample_news:
            try:
                article, created = NewsArticle.objects.get_or_create(
                    url=news_data["url"],
                    defaults={
                        "title": news_data["title"],
                        "content": news_data["content"],
                        "summary": news_data["summary"],
                        "published_date": timezone.now() - timedelta(hours=saved_count),
                        "category": news_data["category"],
                        "image_url": news_data.get("image_url", ""),
                    },
                )
                if created:
                    saved_count += 1
                    print(f"샘플 뉴스 생성: {news_data['title']}")
            except Exception as e:
                print(f"샘플 뉴스 생성 오류: {e}")

        return saved_count
