<template>
  <div class="main-page">
    <!-- Hero Section -->
    <section class="hero-section" @click="goToSurvey">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <h1 class="hero-title">맞춤형 투자 추천 서비스</h1>
            <p class="hero-subtitle">설문조사를 통해 당신에게 맞는 투자 상품과 주식을 추천해드립니다</p>
            <div class="hero-cta">
              <span class="cta-text">클릭하여 설문조사 시작하기</span>
              <i class="fas fa-arrow-right cta-arrow"></i>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="hero-image">
              <div class="placeholder-image">
                <i class="fas fa-chart-line fa-5x text-primary"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Explore Our Services Section -->
    <section class="services-section">
      <div class="container">
        <h2 class="section-title">Explore Our Services</h2>
        
        <!-- Services Carousel -->
        <div id="servicesCarousel" class="carousel slide" data-bs-ride="carousel">
          <div class="carousel-inner">
            <!-- First slide - 3 services -->
            <div class="carousel-item active">
              <div class="row g-4">
                <div class="col-md-4">
                  <div class="service-card" @click="navigateToService('/saving')">
                    <div class="service-image">
                      <div class="service-icon plant-icon">
                        <i class="fas fa-seedling fa-3x"></i>
                      </div>
                    </div>
                    <div class="service-content">
                      <h5>Compare Deposit/Savings Interest Rates</h5>
                      <p>Find the best interest rates for your deposits and savings accounts.</p>
                    </div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="service-card" @click="navigateToService('/metal')">
                    <div class="service-image">
                      <div class="service-icon chart-icon">
                        <i class="fas fa-chart-line fa-3x"></i>
                      </div>
                    </div>
                    <div class="service-content">
                      <h5>Check Stock Prices</h5>
                      <p>Track stock market trends and individual stock performance.</p>
                    </div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="service-card" @click="navigateToService('/metal')">
                    <div class="service-image">
                      <div class="service-icon coins-icon">
                        <i class="fas fa-coins fa-3x"></i>
                      </div>
                    </div>
                    <div class="service-content">
                      <h5>Check Commodity Prices</h5>
                      <p>Stay updated on the latest prices for various commodities.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Second slide - 2 services -->
            <div class="carousel-item">
              <div class="row g-4 justify-content-center">
                <div class="col-md-4">
                  <div class="service-card" @click="navigateToService('/youtube')">
                    <div class="service-image">
                      <div class="service-icon video-icon">
                        <i class="fas fa-play-circle fa-3x"></i>
                      </div>
                    </div>
                    <div class="service-content">
                      <h5>Search Videos of Interest</h5>
                      <p>Explore videos related to your interests in finance and investment.</p>
                    </div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="service-card" @click="navigateToService('/bank')">
                    <div class="service-image">
                      <div class="service-icon bank-icon">
                        <i class="fas fa-university fa-3x"></i>
                      </div>
                    </div>
                    <div class="service-content">
                      <h5>Find Nearby Banks</h5>
                      <p>Locate banks and ATMs in your area for convenient banking.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Carousel Controls -->
          <button class="carousel-control-prev" type="button" data-bs-target="#servicesCarousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon"></span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#servicesCarousel" data-bs-slide="next">
            <span class="carousel-control-next-icon"></span>
          </button>
          
          <!-- Carousel Indicators -->
          <div class="carousel-indicators">
            <button type="button" data-bs-target="#servicesCarousel" data-bs-slide-to="0" class="active"></button>
            <button type="button" data-bs-target="#servicesCarousel" data-bs-slide-to="1"></button>
          </div>
        </div>
      </div>
    </section>

    <!-- Today's Financial News Section -->
    <section class="news-section">
      <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="section-title mb-0">Today's Financial News</h2>
          <router-link to="/news" class="btn btn-outline-primary">
            View All News <i class="fas fa-arrow-right ms-1"></i>
          </router-link>
        </div>
        
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-3">{{ crawlingMessage || 'Loading latest news...' }}</p>
        </div>
        
        <div v-else class="row g-4">
          <!-- Dynamic News Articles -->
          <div v-for="(news, index) in displayNews" :key="news.id || index" class="col-lg-4">
            <div class="news-card" @click="openNewsLink(news)">
              <div class="news-image">
                <img 
                  v-if="news.image_url" 
                  :src="news.image_url" 
                  :alt="news.title"
                  class="news-img"
                  @error="handleImageError"
                />
                <div v-else class="news-placeholder" :class="getNewsImageClass(news.category || 'default', index)">
                  <i :class="getNewsIcon(news.category || 'default', index)" class="fa-3x"></i>
                </div>
              </div>
              <div class="news-content">
                <h5>{{ news.title }}</h5>
                <p>{{ truncateText(news.summary || news.content || 'No summary available', 120) }}</p>
                <small class="text-muted">{{ formatDate(news.published_date) }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const newsList = ref([])
const loading = ref(false)
const crawlingMessage = ref('')

// Fallback news data
const fallbackNews = [
  {
    title: "Market Volatility Continues Amidst Economic Uncertainty",
    summary: "Global markets experienced another day of fluctuations as investors reacted to mixed economic signals and geopolitical developments.",
    published_date: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 hours ago
    category: "market"
  },
  {
    title: "Central Bank Holds Steady on Interest Rates",
    summary: "The Central Bank announced today that it would maintain current interest rates, citing a need to balance inflation concerns with supporting economic growth.",
    published_date: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(), // 4 hours ago
    category: "central-bank"
  },
  {
    title: "Tech Sector Leads Market Gains",
    summary: "The technology sector outperformed other industries today, driven by strong earnings reports and optimism about future innovation.",
    published_date: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(), // 6 hours ago
    category: "tech"
  }
]

const displayNews = ref(fallbackNews)

const navigateToService = (path) => {
  router.push(path)
}

const goToSurvey = () => {
  router.push('/survey')
}

const crawlAndFetchNews = async () => {
  loading.value = true
  crawlingMessage.value = 'Fetching latest financial news...'
  
  try {
    // First, trigger news crawling
    const crawlResponse = await axios.post('/api/news/crawl/')
    console.log('Crawl response:', crawlResponse.data)
    
    crawlingMessage.value = 'Loading news articles...'
    
    // Then fetch the updated news
    const response = await axios.get('/api/news/')
    if (response.data && response.data.length > 0) {
      newsList.value = response.data
      displayNews.value = response.data.slice(0, 3) // Show only first 3 news
    } else {
      displayNews.value = fallbackNews
    }
    
    crawlingMessage.value = ''
  } catch (error) {
    console.error('Error crawling/fetching news:', error)
    crawlingMessage.value = 'Error loading news. Showing cached articles...'
    
    // Fallback to just fetching existing news
    try {
      const response = await axios.get('/api/news/')
      if (response.data && response.data.length > 0) {
        newsList.value = response.data
        displayNews.value = response.data.slice(0, 3)
      } else {
        displayNews.value = fallbackNews
      }
    } catch (fetchError) {
      console.error('Error fetching cached news:', fetchError)
      displayNews.value = fallbackNews
    }
  } finally {
    loading.value = false
    setTimeout(() => {
      crawlingMessage.value = ''
    }, 3000)
  }
}

const fetchNews = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/news/')
    if (response.data && response.data.length > 0) {
      newsList.value = response.data
      displayNews.value = response.data.slice(0, 3) // Show only first 3 news
    } else {
      displayNews.value = fallbackNews
    }
  } catch (error) {
    console.error('Error fetching news:', error)
    displayNews.value = fallbackNews
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffHours = Math.floor(diffTime / (1000 * 60 * 60))
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffHours < 1) {
    return 'Just now'
  } else if (diffHours < 24) {
    return `${diffHours} hours ago`
  } else if (diffDays < 7) {
    return `${diffDays} days ago`
  } else {
    return date.toLocaleDateString()
  }
}

const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const getNewsImageClass = (category, index) => {
  const classes = {
    '금융': 'market-chart',
    '주식': 'tech-sector',
    '경제': 'central-bank',
    '투자': 'market-chart',
    'market': 'market-chart',
    'central-bank': 'central-bank',
    'tech': 'tech-sector',
    'default': ['market-chart', 'central-bank', 'tech-sector'][index % 3]
  }
  return classes[category] || classes.default
}

const getNewsIcon = (category, index) => {
  const icons = {
    '금융': 'fas fa-chart-area',
    '주식': 'fas fa-microchip',
    '경제': 'fas fa-landmark',
    '투자': 'fas fa-chart-line',
    'market': 'fas fa-chart-area',
    'central-bank': 'fas fa-landmark',
    'tech': 'fas fa-microchip',
    'default': ['fas fa-chart-area', 'fas fa-landmark', 'fas fa-microchip'][index % 3]
  }
  return icons[category] || icons.default
}

const openNewsLink = (news) => {
  if (news.id) {
    router.push(`/news/${news.id}`)
  }
}

const handleImageError = (event) => {
  event.target.style.display = 'none'
}

onMounted(() => {
  // Automatically crawl and fetch fresh news when page loads
  crawlAndFetchNews()
})
</script>

<style scoped>
.main-page {
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.hero-section:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  transform: translateY(-2px);
}

.hero-cta {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 255, 255, 0.2);
  padding: 15px 25px;
  border-radius: 50px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  display: inline-flex;
}

.hero-section:hover .hero-cta {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateX(5px);
}

.cta-text {
  font-weight: 600;
  font-size: 1.1rem;
}

.cta-arrow {
  transition: transform 0.3s ease;
}

.hero-section:hover .cta-arrow {
  transform: translateX(5px);
}

.hero-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-image {
  text-align: center;
}

.placeholder-image {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 60px;
  backdrop-filter: blur(10px);
}

/* Services Section */
.services-section {
  padding: 80px 0;
  background-color: #f8f9fa;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 3rem;
  color: #333;
}

.service-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  border: none;
}

.service-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.service-image {
  margin-bottom: 1.5rem;
}

.service-icon {
  width: 120px;
  height: 120px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  color: white;
}

.plant-icon {
  background: linear-gradient(135deg, #4CAF50, #2E7D32);
}

.chart-icon {
  background: linear-gradient(135deg, #2196F3, #1565C0);
}

.coins-icon {
  background: linear-gradient(135deg, #FF9800, #E65100);
}

.video-icon {
  background: linear-gradient(135deg, #9C27B0, #6A1B9A);
}

.bank-icon {
  background: linear-gradient(135deg, #607D8B, #37474F);
}

.service-content h5 {
  font-weight: bold;
  margin-bottom: 1rem;
  color: #333;
}

.service-content p {
  color: #666;
  line-height: 1.6;
}

/* Carousel Controls */
.carousel-control-prev,
.carousel-control-next {
  width: 5%;
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  width: 40px;
  height: 40px;
}

.carousel-indicators {
  margin-bottom: -50px;
}

.carousel-indicators button {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #007bff;
}

/* News Section */
.news-section {
  padding: 80px 0;
  background-color: white;
}

.news-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  height: 100%;
  cursor: pointer;
}

.news-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
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

.market-chart {
  background: linear-gradient(135deg, #1e3c72, #2a5298);
}

.central-bank {
  background: linear-gradient(135deg, #8360c3, #2ebf91);
}

.tech-sector {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.news-content {
  padding: 1.5rem;
}

.news-content h5 {
  font-weight: bold;
  margin-bottom: 1rem;
  color: #333;
  line-height: 1.4;
}

.news-content p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .service-card {
    margin-bottom: 2rem;
  }
  
  .carousel-control-prev,
  .carousel-control-next {
    display: none;
  }
}
</style>
