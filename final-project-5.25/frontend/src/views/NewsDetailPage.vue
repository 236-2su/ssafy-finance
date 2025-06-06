<template>
  <div class="news-detail-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3">뉴스를 불러오는 중...</p>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="alert alert-danger" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>
            {{ error }}
          </div>

          <!-- News Article -->
          <article v-else-if="article" class="news-article">
            <!-- Back Button -->
            <div class="mb-4">
              <button @click="goBack" class="btn btn-outline-secondary">
                <i class="fas fa-arrow-left me-2"></i>
                뉴스 목록으로 돌아가기
              </button>
            </div>

            <!-- Article Header -->
            <header class="article-header mb-4">
              <div class="category-badge mb-3">
                <span class="badge bg-primary">{{ article.category }}</span>
              </div>
              
              <h1 class="article-title">{{ article.title }}</h1>
              
              <div class="article-meta">
                <div class="meta-item">
                  <i class="fas fa-calendar-alt me-2"></i>
                  {{ formatDate(article.published_date) }}
                </div>
                <div class="meta-item">
                  <i class="fas fa-building me-2"></i>
                  {{ article.source }}
                </div>
              </div>
            </header>

            <!-- Article Image -->
            <div v-if="article.image_url" class="article-image mb-4">
              <img 
                :src="article.image_url" 
                :alt="article.title"
                class="img-fluid rounded"
                @error="handleImageError"
              />
            </div>

            <!-- Article Summary -->
            <div v-if="article.summary" class="article-summary mb-4">
              <div class="summary-box">
                <h3 class="summary-title">
                  <i class="fas fa-info-circle me-2"></i>
                  요약
                </h3>
                <p class="summary-text">{{ article.summary }}</p>
              </div>
            </div>

            <!-- Article Content -->
            <div class="article-content">
              <div class="content-text">
                {{ article.content }}
              </div>
            </div>

            <!-- Article Footer -->
            <footer class="article-footer mt-5">
              <div class="row">
                <div class="col-md-6">
                  <div class="source-info">
                    <small class="text-muted">
                      출처: {{ article.source }}
                    </small>
                  </div>
                </div>
                <div class="col-md-6 text-md-end">
                  <small class="text-muted">
                    {{ formatDate(article.published_date) }} 발행
                  </small>
                </div>
              </div>
            </footer>
          </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const article = ref(null)
const loading = ref(true)
const error = ref('')

const fetchArticle = async () => {
  try {
    loading.value = true
    const response = await axios.get(`/api/news/${route.params.id}/`)
    article.value = response.data
  } catch (err) {
    console.error('뉴스 상세 정보 가져오기 실패:', err)
    error.value = '뉴스를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleImageError = (event) => {
  event.target.style.display = 'none'
}

const goBack = () => {
  router.push('/news')
}

onMounted(() => {
  fetchArticle()
})
</script>

<style scoped>
.news-detail-page {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 2rem 0;
}

.news-article {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.article-header {
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 1.5rem;
}

.category-badge .badge {
  font-size: 0.875rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
}

.article-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  line-height: 1.3;
  margin-bottom: 1rem;
}

.article-meta {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.meta-item {
  color: #666;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.meta-item i {
  color: #007bff;
}

.article-image img {
  width: 100%;
  height: auto;
  max-height: 400px;
  object-fit: cover;
}

.article-summary {
  background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
  border-radius: 10px;
  padding: 1.5rem;
  border-left: 4px solid #007bff;
}

.summary-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
}

.summary-title i {
  color: #007bff;
}

.summary-text {
  font-size: 1rem;
  line-height: 1.6;
  color: #555;
  margin: 0;
}

.article-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
}

.content-text {
  white-space: pre-line;
}

.article-footer {
  border-top: 1px solid #e9ecef;
  padding-top: 1.5rem;
}

.source-info {
  font-style: italic;
}

.btn-outline-secondary {
  border-radius: 25px;
  padding: 0.5rem 1.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-outline-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .news-detail-page {
    padding: 1rem 0;
  }
  
  .news-article {
    margin: 0 1rem;
    padding: 1.5rem;
  }
  
  .article-title {
    font-size: 1.5rem;
  }
  
  .article-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .article-content {
    font-size: 1rem;
  }
}
</style>
