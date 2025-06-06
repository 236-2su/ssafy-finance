<template>
  <div class="news-page">
    <div class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">금융 뉴스</h1>
          <p class="hero-subtitle">실시간 금융 정보와 시장 동향을 확인하세요</p>
          <div class="refresh-button-container">
            <button
              @click="refreshNews"
              :disabled="loading"
              class="refresh-btn"
            >
              <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
              {{ loading ? "업데이트 중..." : "뉴스 새로고침" }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="content-wrapper">
        <!-- Featured News -->
        <div class="featured-section">
          <h2 class="section-title">주요 뉴스</h2>

          <div v-if="loading" class="loading-container">
            <div class="loading-spinner"></div>
            <p class="loading-text">
              {{ crawlingMessage || "최신 뉴스를 불러오는 중..." }}
            </p>
          </div>

          <div
            v-else-if="featuredNews"
            class="featured-card"
            @click="openNewsDetail(featuredNews)"
          >
            <div class="featured-image">
              <img
                v-if="featuredNews.image_url"
                :src="featuredNews.image_url"
                :alt="featuredNews.title"
                class="featured-img"
                @error="handleImageError"
              />
              <div v-else class="news-placeholder featured-placeholder">
                <i class="fas fa-newspaper fa-4x"></i>
              </div>
              <div class="featured-overlay">
                <span class="featured-badge">Breaking</span>
              </div>
            </div>
            <div class="featured-content">
              <h3 class="featured-title">{{ featuredNews.title }}</h3>
              <p class="featured-summary">
                {{ featuredNews.summary || "요약 정보가 없습니다." }}
              </p>
              <div class="featured-meta">
                <span class="meta-item">
                  <i class="fas fa-clock"></i>
                  {{ formatDate(featuredNews.published_date) }}
                </span>
                <span class="meta-item">
                  <i class="fas fa-user"></i>
                  {{ featuredNews.source }}
                </span>
              </div>
            </div>
          </div>

          <div v-else class="featured-card">
            <div class="featured-image">
              <div class="news-placeholder featured-placeholder">
                <i class="fas fa-chart-line fa-4x"></i>
              </div>
              <div class="featured-overlay">
                <span class="featured-badge">Breaking</span>
              </div>
            </div>
            <div class="featured-content">
              <h3 class="featured-title">
                시장 변동성이 경제 불확실성 속에서 지속
              </h3>
              <p class="featured-summary">
                글로벌 시장은 혼재된 경제 신호와 지정학적 발전에 대한 투자자들의
                반응으로 또 다른 변동의 하루를 경험했습니다.
              </p>
              <div class="featured-meta">
                <span class="meta-item">
                  <i class="fas fa-clock"></i>
                  2시간 전
                </span>
                <span class="meta-item">
                  <i class="fas fa-user"></i>
                  Financial Times
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="main-content">
          <!-- Recent News -->
          <div class="news-section">
            <h2 class="section-title">최신 뉴스</h2>

            <div v-if="!loading && newsList.length > 0" class="news-grid">
              <div
                v-for="news in newsList"
                :key="news.id"
                class="news-card"
                @click="openNewsDetail(news)"
              >
                <div class="news-image">
                  <img
                    v-if="news.image_url"
                    :src="news.image_url"
                    :alt="news.title"
                    class="news-img"
                    @error="handleImageError"
                  />
                  <div
                    v-else
                    class="news-placeholder"
                    :class="getNewsImageClass(news.category)"
                  >
                    <i :class="getNewsIcon(news.category)" class="fa-2x"></i>
                  </div>
                </div>
                <div class="news-content">
                  <h4 class="news-title">{{ news.title }}</h4>
                  <p class="news-summary">
                    {{ news.summary || "요약 정보가 없습니다." }}
                  </p>
                  <div class="news-meta">
                    <span class="meta-date">{{
                      formatDate(news.published_date)
                    }}</span>
                    <span class="read-more">자세히 보기 →</span>
                  </div>
                </div>
              </div>
            </div>

            <div v-else-if="!loading" class="news-grid">
              <div class="news-card">
                <div class="news-image">
                  <div class="news-placeholder central-bank">
                    <i class="fas fa-landmark fa-2x"></i>
                  </div>
                </div>
                <div class="news-content">
                  <h4 class="news-title">중앙은행, 금리 동결 결정</h4>
                  <p class="news-summary">
                    중앙은행은 오늘 인플레이션 우려와 경제 성장 지원 사이의
                    균형을 맞춰야 한다며 현재 금리를 유지하겠다고 발표했습니다.
                  </p>
                  <div class="news-meta">
                    <span class="meta-date">4시간 전</span>
                    <span class="read-more">자세히 보기 →</span>
                  </div>
                </div>
              </div>

              <div class="news-card">
                <div class="news-image">
                  <div class="news-placeholder tech-sector">
                    <i class="fas fa-microchip fa-2x"></i>
                  </div>
                </div>
                <div class="news-content">
                  <h4 class="news-title">기술주가 시장 상승 주도</h4>
                  <p class="news-summary">
                    기술 부문이 강력한 실적 보고서와 미래 혁신에 대한 낙관론에
                    힘입어 오늘 다른 산업을 앞섰습니다.
                  </p>
                  <div class="news-meta">
                    <span class="meta-date">6시간 전</span>
                    <span class="read-more">자세히 보기 →</span>
                  </div>
                </div>
              </div>

              <div class="news-card">
                <div class="news-image">
                  <div class="news-placeholder crypto">
                    <i class="fab fa-bitcoin fa-2x"></i>
                  </div>
                </div>
                <div class="news-content">
                  <h4 class="news-title">암호화폐 시장 회복 조짐</h4>
                  <p class="news-summary">
                    주요 암호화폐들이 이번 주 긍정적인 모멘텀을 보이며,
                    비트코인과 이더리움이 시장 회복을 주도하고 있습니다.
                  </p>
                  <div class="news-meta">
                    <span class="meta-date">8시간 전</span>
                    <span class="read-more">자세히 보기 →</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="sidebar">
            <!-- Market Summary -->
            <div class="widget market-widget">
              <h4 class="widget-title">시장 현황</h4>
              <div class="market-summary">
                <div class="market-item">
                  <div class="market-info">
                    <span class="market-name">코스피</span>
                    <span class="market-value up"
                      >2,485.47 <i class="fas fa-arrow-up"></i
                    ></span>
                  </div>
                  <div class="market-change up">+1.2%</div>
                </div>
                <div class="market-item">
                  <div class="market-info">
                    <span class="market-name">코스닥</span>
                    <span class="market-value down"
                      >843.81 <i class="fas fa-arrow-down"></i
                    ></span>
                  </div>
                  <div class="market-change down">-0.8%</div>
                </div>
                <div class="market-item">
                  <div class="market-info">
                    <span class="market-name">원/달러</span>
                    <span class="market-value up"
                      >1,345.40 <i class="fas fa-arrow-up"></i
                    ></span>
                  </div>
                  <div class="market-change up">+0.3%</div>
                </div>
              </div>
            </div>

            <!-- Newsletter -->
            <div class="widget newsletter-widget">
              <h4 class="widget-title">뉴스레터 구독</h4>
              <p class="newsletter-desc">
                최신 금융 뉴스를 이메일로 받아보세요.
              </p>
              <div class="newsletter-form">
                <input
                  type="email"
                  class="newsletter-input"
                  placeholder="이메일 주소 입력"
                />
                <button class="newsletter-btn">구독하기</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const newsList = ref([]);
const featuredNews = ref(null);
const loading = ref(false);
const crawlingMessage = ref("");

const crawlAndFetchNews = async () => {
  loading.value = true;
  crawlingMessage.value = "최신 뉴스를 수집하는 중...";

  try {
    const crawlResponse = await axios.post("/api/news/crawl/");
    console.log("Crawl response:", crawlResponse.data);

    crawlingMessage.value = "뉴스 기사를 불러오는 중...";

    const response = await axios.get("/api/news/");
    newsList.value = response.data.slice(1);
    featuredNews.value = response.data[0] || null;

    crawlingMessage.value = "";
  } catch (error) {
    console.error("Error crawling/fetching news:", error);
    crawlingMessage.value =
      "뉴스 로딩 중 오류가 발생했습니다. 캐시된 기사를 표시합니다...";

    try {
      const response = await axios.get("/api/news/");
      newsList.value = response.data.slice(1);
      featuredNews.value = response.data[0] || null;
    } catch (fetchError) {
      console.error("Error fetching cached news:", fetchError);
    }
  } finally {
    loading.value = false;
    setTimeout(() => {
      crawlingMessage.value = "";
    }, 3000);
  }
};

const fetchNews = async () => {
  loading.value = true;
  try {
    const response = await axios.get("/api/news/");
    newsList.value = response.data.slice(1);
    featuredNews.value = response.data[0] || null;
  } catch (error) {
    console.error("Error fetching news:", error);
  } finally {
    loading.value = false;
  }
};

const refreshNews = () => {
  crawlAndFetchNews();
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

  if (diffHours < 1) {
    return "방금 전";
  } else if (diffHours < 24) {
    return `${diffHours}시간 전`;
  } else if (diffDays < 7) {
    return `${diffDays}일 전`;
  } else {
    return date.toLocaleDateString("ko-KR");
  }
};

const getNewsImageClass = (category) => {
  const classes = {
    금융: "market-volatility",
    주식: "tech-sector",
    경제: "central-bank",
    투자: "crypto",
  };
  return classes[category] || "market-volatility";
};

const getNewsIcon = (category) => {
  const icons = {
    금융: "fas fa-chart-line",
    주식: "fas fa-chart-area",
    경제: "fas fa-landmark",
    투자: "fas fa-coins",
  };
  return icons[category] || "fas fa-newspaper";
};

const openNewsDetail = (news) => {
  if (news.id) {
    router.push(`/news/${news.id}`);
  }
};

const handleImageError = (event) => {
  event.target.style.display = "none";
};

onMounted(() => {
  crawlAndFetchNews();
});
</script>

<style scoped>
.news-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-section {
  padding: 80px 0 60px;
  text-align: center;
}

.hero-content {
  max-width: 600px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: white;
  margin-bottom: 20px;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 40px;
  line-height: 1.6;
}

.refresh-button-container {
  margin-bottom: 20px;
}

.refresh-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 12px 30px;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.refresh-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.content-wrapper {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 30px 30px 0 0;
  padding: 40px;
  margin-top: -20px;
  backdrop-filter: blur(10px);
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 30px;
  position: relative;
  padding-bottom: 10px;
}

.section-title::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

.featured-section {
  margin-bottom: 50px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(102, 126, 234, 0.3);
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-text {
  color: #666;
  font-size: 1.1rem;
}

.featured-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.featured-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
}

.featured-image {
  height: 400px;
  position: relative;
  overflow: hidden;
}

.featured-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.featured-card:hover .featured-img {
  transform: scale(1.05);
}

.featured-placeholder {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.featured-overlay {
  position: absolute;
  top: 20px;
  left: 20px;
}

.featured-badge {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.featured-content {
  padding: 30px;
}

.featured-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.4;
}

.featured-summary {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.featured-meta {
  display: flex;
  gap: 20px;
  color: #888;
  font-size: 0.9rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.news-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
}

.news-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
}

.news-image {
  height: 200px;
  overflow: hidden;
}

.news-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.news-card:hover .news-img {
  transform: scale(1.05);
}

.news-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.market-volatility {
  background: linear-gradient(135deg, #1e3c72, #2a5298);
}

.central-bank {
  background: linear-gradient(135deg, #8360c3, #2ebf91);
}

.tech-sector {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.crypto {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.news-content {
  padding: 20px;
}

.news-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.4;
}

.news-summary {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta-date {
  color: #888;
  font-size: 0.85rem;
}

.read-more {
  color: #667eea;
  font-weight: 600;
  font-size: 0.9rem;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.widget {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.widget-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
}

.market-widget {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.market-widget .widget-title {
  color: white;
}

.market-summary {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.market-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.market-item:last-child {
  border-bottom: none;
}

.market-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.market-name {
  font-size: 0.9rem;
  opacity: 0.9;
}

.market-value {
  font-weight: 700;
  font-size: 1.1rem;
}

.market-value.up {
  color: #4ade80;
}

.market-value.down {
  color: #f87171;
}

.market-change {
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 0.85rem;
}

.market-change.up {
  background: rgba(74, 222, 128, 0.2);
  color: #4ade80;
}

.market-change.down {
  background: rgba(248, 113, 113, 0.2);
  color: #f87171;
}

.trending-topics {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.topic-tag {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.newsletter-widget {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.newsletter-desc {
  color: #8b4513;
  margin-bottom: 15px;
  font-size: 0.9rem;
}

.newsletter-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.newsletter-input {
  padding: 12px;
  border: 2px solid rgba(139, 69, 19, 0.2);
  border-radius: 8px;
  font-size: 0.9rem;
  background: rgba(255, 255, 255, 0.8);
}

.newsletter-input:focus {
  outline: none;
  border-color: #8b4513;
}

.newsletter-btn {
  background: #8b4513;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.newsletter-btn:hover {
  background: #a0522d;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .content-wrapper {
    padding: 20px;
  }

  .main-content {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .news-grid {
    grid-template-columns: 1fr;
  }

  .featured-image {
    height: 250px;
  }

  .featured-content {
    padding: 20px;
  }

  .featured-title {
    font-size: 1.5rem;
  }
}
</style>
