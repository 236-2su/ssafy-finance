<template>
  <div class="recommendation-page">
    <div class="container">
      <!-- Header -->
      <div class="page-header">
        <h1 class="page-title">맞춤형 투자 추천</h1>
        <p class="page-subtitle">설문조사 결과를 바탕으로 추천된 투자 상품입니다.</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">추천 상품을 불러오는 중...</p>
      </div>

      <!-- Recommendations Content -->
      <div v-else class="recommendations-content">
        <!-- Stock Recommendations -->
        <div class="recommendation-section">
          <div class="section-header">
            <h2 class="section-title">
              <i class="fas fa-chart-line me-2"></i>
              추천 주식
            </h2>
            <p class="section-subtitle">투자 성향에 맞는 주식을 추천해드립니다.</p>
          </div>

          <div v-if="stockRecommendations.length > 0" class="row g-4">
            <div v-for="stock in stockRecommendations" :key="stock.id" class="col-lg-6">
              <div class="recommendation-card stock-card">
                <div class="card-header">
                  <div class="stock-info">
                    <h3 class="stock-name">{{ stock.stock_name }}</h3>
                    <span class="stock-code">{{ stock.stock_code }}</span>
                  </div>
                  <div class="confidence-score">
                    <span class="score-label">신뢰도</span>
                    <div class="score-bar">
                      <div class="score-fill" :style="{ width: (stock.confidence_score * 100) + '%' }"></div>
                    </div>
                    <span class="score-value">{{ Math.round(stock.confidence_score * 100) }}%</span>
                  </div>
                </div>
                <div class="card-body">
                  <p class="recommendation-reason">{{ stock.recommendation_reason }}</p>
                  <div class="card-actions">
                    <button @click="addToInterested(stock)" class="btn btn-outline-primary btn-sm">
                      <i class="fas fa-heart me-1"></i>관심주식 추가
                    </button>
                    <button @click="viewStockDetail(stock)" class="btn btn-primary btn-sm">
                      <i class="fas fa-info-circle me-1"></i>상세 정보
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="empty-state">
            <i class="fas fa-chart-line empty-icon"></i>
            <h3>추천 주식이 없습니다</h3>
            <p>설문조사를 다시 진행해보세요.</p>
            <router-link to="/survey" class="btn btn-primary">설문조사 하기</router-link>
          </div>
        </div>

        <!-- Saving Recommendations -->
        <div class="recommendation-section">
          <div class="section-header">
            <h2 class="section-title">
              <i class="fas fa-piggy-bank me-2"></i>
              추천 예적금
            </h2>
            <p class="section-subtitle">안전하고 수익성 높은 예적금 상품을 추천해드립니다.</p>
          </div>

          <div v-if="savingRecommendations.length > 0" class="row g-4">
            <div v-for="saving in savingRecommendations" :key="saving.id" class="col-lg-6">
              <div class="recommendation-card saving-card">
                <div class="card-header">
                  <div class="saving-info">
                    <h3 class="saving-name">{{ saving.product_name }}</h3>
                    <span class="bank-name">{{ saving.bank_name }}</span>
                  </div>
                  <div class="interest-rate">
                    <span class="rate-value">{{ saving.interest_rate }}%</span>
                    <span class="rate-label">연 이율</span>
                  </div>
                </div>
                <div class="card-body">
                  <div class="product-type">
                    <span class="type-badge" :class="saving.product_type === 'deposit' ? 'deposit-badge' : 'saving-badge'">
                      {{ saving.product_type === 'deposit' ? '예금' : '적금' }}
                    </span>
                  </div>
                  <p class="recommendation-reason">{{ saving.recommendation_reason }}</p>
                  <div class="card-actions">
                    <button @click="viewSavingDetail(saving)" class="btn btn-primary btn-sm">
                      <i class="fas fa-info-circle me-1"></i>상세 정보
                    </button>
                    <button @click="goToBank(saving)" class="btn btn-outline-primary btn-sm">
                      <i class="fas fa-map-marker-alt me-1"></i>지점 찾기
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="empty-state">
            <i class="fas fa-piggy-bank empty-icon"></i>
            <h3>추천 예적금이 없습니다</h3>
            <p>설문조사를 다시 진행해보세요.</p>
            <router-link to="/survey" class="btn btn-primary">설문조사 하기</router-link>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-section">
          <div class="row g-3">
            <div class="col-md-6">
              <router-link to="/survey" class="btn btn-outline-primary btn-lg w-100">
                <i class="fas fa-redo me-2"></i>설문조사 다시하기
              </router-link>
            </div>
            <div class="col-md-6">
              <router-link to="/profile" class="btn btn-primary btn-lg w-100">
                <i class="fas fa-user me-2"></i>프로필로 이동
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stock Detail Modal -->
    <div v-if="showStockModal" class="modal-overlay" @click="closeStockModal">
      <div class="detail-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedStock.stock_name }} 상세 정보</h3>
          <button @click="closeStockModal" class="btn-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="stock-detail">
            <div class="detail-item">
              <label>주식 코드:</label>
              <span>{{ selectedStock.stock_code }}</span>
            </div>
            <div class="detail-item">
              <label>추천 이유:</label>
              <p>{{ selectedStock.recommendation_reason }}</p>
            </div>
            <div class="detail-item">
              <label>신뢰도:</label>
              <span>{{ Math.round(selectedStock.confidence_score * 100) }}%</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="addToInterested(selectedStock)" class="btn btn-primary">
            관심주식 추가
          </button>
          <button @click="closeStockModal" class="btn btn-outline-secondary">
            닫기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const loading = ref(true)
const stockRecommendations = ref([])
const savingRecommendations = ref([])
const showStockModal = ref(false)
const selectedStock = ref({})

const fetchRecommendations = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/accounts/recommendations/')
    stockRecommendations.value = response.data.stock_recommendations || []
    savingRecommendations.value = response.data.saving_recommendations || []
  } catch (error) {
    console.error('Error fetching recommendations:', error)
    if (error.response?.status === 401) {
      router.push('/login')
    }
  } finally {
    loading.value = false
  }
}

const addToInterested = async (stock) => {
  try {
    await axios.post('/api/accounts/stocks/', {
      type: 'interested',
      stock_data: {
        code: stock.stock_code,
        name: stock.stock_name
      }
    })
    alert(`${stock.stock_name}이(가) 관심주식에 추가되었습니다.`)
  } catch (error) {
    console.error('Error adding to interested stocks:', error)
    alert('관심주식 추가 중 오류가 발생했습니다.')
  }
}

const viewStockDetail = (stock) => {
  selectedStock.value = stock
  showStockModal.value = true
}

const closeStockModal = () => {
  showStockModal.value = false
  selectedStock.value = {}
}

const viewSavingDetail = (saving) => {
  // 예적금 상세 페이지로 이동 (구현 필요)
  router.push(`/saving/${saving.id}`)
}

const goToBank = (saving) => {
  // 은행 지점 찾기 페이지로 이동
  router.push('/bank')
}

onMounted(() => {
  fetchRecommendations()
})
</script>

<style scoped>
.recommendation-page {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 2rem 0;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 1rem;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

.recommendation-section {
  margin-bottom: 4rem;
}

.section-header {
  text-align: center;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.section-subtitle {
  color: #666;
  font-size: 1rem;
}

.recommendation-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  height: 100%;
}

.recommendation-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.stock-card .card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
}

.saving-card .card-header {
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
  color: white;
  padding: 1.5rem;
}

.stock-info, .saving-info {
  margin-bottom: 1rem;
}

.stock-name, .saving-name {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.stock-code, .bank-name {
  font-size: 0.9rem;
  opacity: 0.8;
}

.confidence-score {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.score-label {
  font-size: 0.8rem;
  opacity: 0.8;
}

.score-bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: white;
  transition: width 0.3s ease;
}

.score-value {
  font-size: 0.9rem;
  font-weight: bold;
}

.interest-rate {
  text-align: right;
}

.rate-value {
  font-size: 1.5rem;
  font-weight: bold;
  display: block;
}

.rate-label {
  font-size: 0.8rem;
  opacity: 0.8;
}

.card-body {
  padding: 1.5rem;
}

.product-type {
  margin-bottom: 1rem;
}

.type-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
}

.deposit-badge {
  background: #007bff;
}

.saving-badge {
  background: #28a745;
}

.recommendation-reason {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.card-actions .btn {
  flex: 1;
  min-width: 120px;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  color: #ddd;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin-bottom: 1rem;
}

.action-section {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.detail-modal {
  background: white;
  border-radius: 15px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #666;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.btn-close:hover {
  background: #f8f9fa;
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.stock-detail {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item label {
  font-weight: bold;
  color: #333;
  font-size: 0.9rem;
}

.detail-item span,
.detail-item p {
  color: #666;
  margin: 0;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.modal-footer .btn {
  flex: 1;
}

@media (max-width: 768px) {
  .recommendation-page {
    padding: 1rem 0;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
  
  .card-actions {
    flex-direction: column;
  }
  
  .card-actions .btn {
    min-width: auto;
  }
  
  .action-section .row {
    flex-direction: column;
  }
}
</style>
