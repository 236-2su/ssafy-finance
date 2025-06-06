<template>
  <div class="recommendation-page">
    <div class="container">
      <!-- Header -->
      <div class="page-header">
        <h1 class="page-title">맞춤형 투자 추천</h1>
        <p class="page-subtitle">
          설문조사 결과를 바탕으로 추천된 투자 상품입니다.
        </p>
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
            <p class="section-subtitle">
              투자 성향에 맞는 주식을 추천해드립니다.
            </p>
          </div>

          <div v-if="stockRecommendations.length > 0" class="row g-4">
            <div
              v-for="stock in stockRecommendations"
              :key="stock.id"
              class="col-lg-6"
            >
              <div class="recommendation-card stock-card">
                <div class="card-header">
                  <div class="stock-info">
                    <h3 class="stock-name">{{ stock.stock_name }}</h3>
                    <span class="stock-code">{{ stock.stock_code }}</span>
                  </div>
                  <div class="confidence-score">
                    <span class="score-label">신뢰도</span>
                    <div class="score-bar">
                      <div
                        class="score-fill"
                        :style="{ width: stock.confidence_score * 100 + '%' }"
                      ></div>
                    </div>
                    <span class="score-value"
                      >{{ Math.round(stock.confidence_score * 100) }}%</span
                    >
                  </div>
                </div>
                <div class="card-body">
                  <p class="recommendation-reason">
                    {{ stock.recommendation_reason }}
                  </p>
                  <div class="card-actions">
                    <button
                      @click="addToInterested(stock)"
                      class="btn btn-outline-primary btn-sm"
                    >
                      <i class="fas fa-heart me-1"></i>관심주식 추가
                    </button>
                    <button
                      @click="viewStockDetail(stock)"
                      class="btn btn-primary btn-sm"
                    >
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
            <router-link to="/survey" class="btn btn-primary"
              >설문조사 하기</router-link
            >
          </div>
        </div>

        <!-- Saving Recommendations -->
        <div class="recommendation-section">
          <div class="section-header">
            <h2 class="section-title">
              <i class="fas fa-piggy-bank me-2"></i>
              추천 예적금
            </h2>
            <p class="section-subtitle">
              안전하고 수익성 높은 예적금 상품을 추천해드립니다.
            </p>
          </div>

          <div v-if="savingRecommendations.length > 0" class="row g-4">
            <div
              v-for="saving in savingRecommendations"
              :key="saving.id"
              class="col-lg-6"
            >
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
                    <span
                      class="type-badge"
                      :class="
                        saving.product_type === 'deposit'
                          ? 'deposit-badge'
                          : 'saving-badge'
                      "
                    >
                      {{ saving.product_type === "deposit" ? "예금" : "적금" }}
                    </span>
                  </div>
                  <p class="recommendation-reason">
                    {{ saving.recommendation_reason }}
                  </p>
                  <div class="card-actions">
                    <button
                      @click="viewSavingDetail(saving)"
                      class="btn btn-primary btn-sm"
                    >
                      <i class="fas fa-info-circle me-1"></i>상세 정보
                    </button>
                    <button
                      @click="goToBank(saving)"
                      class="btn btn-outline-primary btn-sm"
                    >
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
            <router-link to="/survey" class="btn btn-primary"
              >설문조사 하기</router-link
            >
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-section">
          <div class="row g-3">
            <div class="col-md-6">
              <router-link
                to="/survey"
                class="btn btn-outline-primary btn-lg w-100"
              >
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
              <span
                >{{ Math.round(selectedStock.confidence_score * 100) }}%</span
              >
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
            @click="addToInterested(selectedStock)"
            class="btn btn-primary"
          >
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
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

const loading = ref(true);
const stockRecommendations = ref([]);
const savingRecommendations = ref([]);
const showStockModal = ref(false);
const selectedStock = ref({});

const fetchRecommendations = async () => {
  loading.value = true;
  try {
    const response = await axios.get("/api/accounts/recommendations/");
    stockRecommendations.value = response.data.stock_recommendations || [];
    savingRecommendations.value = response.data.saving_recommendations || [];
  } catch (error) {
    console.error("Error fetching recommendations:", error);
    if (error.response?.status === 401) {
      router.push("/login");
    }
  } finally {
    loading.value = false;
  }
};

const addToInterested = async (stock) => {
  try {
    await axios.post("/api/accounts/stocks/", {
      type: "interested",
      stock_data: {
        code: stock.stock_code,
        name: stock.stock_name,
      },
    });
    alert(`${stock.stock_name}이(가) 관심주식에 추가되었습니다.`);
  } catch (error) {
    console.error("Error adding to interested stocks:", error);
    alert("관심주식 추가 중 오류가 발생했습니다.");
  }
};

const viewStockDetail = (stock) => {
  selectedStock.value = stock;
  showStockModal.value = true;
};

const closeStockModal = () => {
  showStockModal.value = false;
  selectedStock.value = {};
};

const viewSavingDetail = (saving) => {
  // 예적금 상세 페이지로 이동 (구현 필요)
  router.push(`/saving/${saving.id}`);
};

const goToBank = (saving) => {
  // 은행 지점 찾기 페이지로 이동
  router.push("/bank");
};

onMounted(() => {
  fetchRecommendations();
});
</script>

<style scoped>
.recommendation-page {
  min-height: 100vh;
  background-color: #f4f6f8; /* 이미지와 유사한 배경색 */
  padding: 2rem 0;
  font-family: "Noto Sans KR", sans-serif; /* 전체 폰트 적용 (필요시) */
}

.container {
  max-width: 1000px; /* 콘텐츠 최대 너비 조정 */
}

.page-header {
  text-align: center;
  margin-bottom: 2.5rem; /* 여백 조정 */
}

.page-title {
  font-size: 2.2rem; /* 폰트 크기 조정 */
  font-weight: 700; /* 폰트 굵기 조정 */
  color: #2c3e50; /* 제목 색상 변경 */
  margin-bottom: 0.75rem; /* 여백 조정 */
}

.page-subtitle {
  font-size: 1rem; /* 폰트 크기 조정 */
  color: #555; /* 부제목 색상 변경 */
  max-width: 600px;
  margin: 0 auto;
}

.recommendation-section {
  margin-bottom: 3rem; /* 섹션 간 여백 조정 */
}

.section-header {
  text-align: center;
  margin-bottom: 1.5rem; /* 섹션 헤더 여백 조정 */
}

.section-title {
  font-size: 1.8rem; /* 섹션 제목 폰트 크기 조정 */
  font-weight: 600; /* 폰트 굵기 조정 */
  color: #34495e; /* 섹션 제목 색상 변경 */
  margin-bottom: 0.5rem;
}

.section-title i {
  margin-right: 0.5rem; /* 아이콘과 텍스트 간격 */
}

.section-subtitle {
  color: #777; /* 섹션 부제목 색상 변경 */
  font-size: 0.9rem; /* 폰트 크기 조정 */
}

.recommendation-card {
  background: white;
  border-radius: 12px; /* 테두리 둥글기 조정 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08); /* 그림자 효과 조정 */
  overflow: hidden;
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.recommendation-card:hover {
  transform: translateY(-4px); /* 호버 효과 조정 */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.12); /* 호버 시 그림자 조정 */
}

.card-header {
  color: white;
  padding: 1.25rem; /* 패딩 조정 */
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.stock-card .card-header {
  /* 이미지 기반 보라색 그라데이션 */
  background: linear-gradient(135deg, #8e44ad 0%, #9b59b6 100%);
}

.saving-card .card-header {
  /* 이미지 기반 녹색 그라데이션 */
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
}

.stock-info,
.saving-info {
  margin-bottom: 0; /* 내부 여백 조정 */
}

.stock-name,
.saving-name {
  font-size: 1.2rem; /* 폰트 크기 조정 */
  font-weight: 600; /* 폰트 굵기 조정 */
  margin-bottom: 0.15rem; /* 여백 조정 */
}

.stock-code,
.bank-name {
  font-size: 0.85rem; /* 폰트 크기 조정 */
  opacity: 0.9; /* 투명도 조정 */
}

.confidence-score {
  display: flex;
  align-items: center;
  gap: 0.4rem; /* 간격 조정 */
  margin-top: 0.25rem; /* 상단 여백 추가 */
}

.score-label {
  font-size: 0.75rem; /* 폰트 크기 조정 */
  opacity: 0.9;
}

.score-bar {
  flex-grow: 1; /* 자동으로 너비 채우도록 */
  min-width: 80px; /* 최소 너비 설정 */
  height: 8px; /* 높이 조정 */
  background: rgba(255, 255, 255, 0.25); /* 배경 투명도 조정 */
  border-radius: 4px; /* 둥글기 조정 */
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: white;
  border-radius: 4px; /* 내부 채움도 둥글게 */
  transition: width 0.5s cubic-bezier(0.25, 0.1, 0.25, 1); /* 부드러운 전환 효과 */
}

.score-value {
  font-size: 0.85rem; /* 폰트 크기 조정 */
  font-weight: 600; /* 폰트 굵기 조정 */
}

.interest-rate {
  text-align: right;
}

.rate-value {
  font-size: 1.6rem; /* 폰트 크기 조정 */
  font-weight: 700; /* 폰트 굵기 조정 */
  display: block;
  line-height: 1.2; /* 줄 간격 조정 */
}

.rate-label {
  font-size: 0.75rem; /* 폰트 크기 조정 */
  opacity: 0.9;
}

.card-body {
  padding: 1.25rem; /* 패딩 조정 */
  flex-grow: 1; /* 내용이 적어도 카드 높이 채우도록 */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 내부 요소 간격 균등하게 */
}

.product-type {
  margin-bottom: 0.75rem; /* 여백 조정 */
}

.type-badge {
  padding: 0.3rem 0.8rem; /* 패딩 조정 */
  border-radius: 15px; /* 둥글기 조정 */
  font-size: 0.75rem; /* 폰트 크기 조정 */
  font-weight: 500; /* 폰트 굵기 조정 */
  color: white;
  display: inline-block; /* 인라인 블록으로 변경 */
}

.deposit-badge {
  background-color: #3498db; /* 예금 뱃지 색상 변경 */
}

.saving-badge {
  background-color: #1abc9c; /* 적금 뱃지 색상 변경 */
}

.recommendation-reason {
  color: #555; /* 본문 텍스트 색상 변경 */
  font-size: 0.9rem; /* 폰트 크기 조정 */
  line-height: 1.5; /* 줄 간격 조정 */
  margin-bottom: 1.25rem; /* 여백 조정 */
  flex-grow: 1; /* 추천 이유 텍스트가 공간을 채우도록 */
}

.card-actions {
  display: flex;
  gap: 0.75rem; /* 버튼 간 간격 조정 */
  margin-top: auto; /* 버튼들을 하단에 정렬 */
}

.card-actions .btn {
  flex: 1;
  padding: 0.5rem 0.75rem; /* 버튼 패딩 조정 */
  font-size: 0.85rem; /* 버튼 폰트 크기 조정 */
  border-radius: 8px; /* 버튼 둥글기 조정 */
  font-weight: 500;
  transition: all 0.2s ease;
}

/* 이미지 기반 버튼 스타일 */
.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
}
.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.btn-outline-primary {
  background-color: white;
  border-color: #007bff;
  color: #007bff;
}
.btn-outline-primary:hover {
  background-color: #007bff;
  color: white;
}

.card-actions .btn i {
  margin-right: 0.3rem; /* 아이콘과 텍스트 간격 */
}

.empty-state {
  text-align: center;
  padding: 2.5rem; /* 패딩 조정 */
  color: #777; /* 텍스트 색상 변경 */
  background-color: #fff; /* 배경색 추가 */
  border-radius: 12px; /* 둥글기 추가 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); /* 그림자 추가 */
}

.empty-icon {
  font-size: 3.5rem; /* 아이콘 크기 조정 */
  color: #e0e0e0; /* 아이콘 색상 변경 */
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.3rem; /* 제목 폰트 크기 조정 */
  color: #444; /* 제목 색상 변경 */
  margin-bottom: 0.75rem; /* 여백 조정 */
}

.empty-state p {
  font-size: 0.9rem; /* 본문 폰트 크기 조정 */
  margin-bottom: 1.25rem; /* 여백 조정 */
}

.action-section {
  margin-top: 2.5rem; /* 상단 여백 조정 */
  padding-top: 1.5rem; /* 패딩 조정 */
  border-top: 1px solid #dee2e6; /* 구분선 색상 변경 */
}

.action-section .btn {
  padding: 0.75rem 1rem; /* 버튼 패딩 조정 */
  font-size: 1rem; /* 버튼 폰트 크기 조정 */
  font-weight: 500;
  border-radius: 8px; /* 버튼 둥글기 조정 */
}

.action-section .btn i {
  margin-right: 0.5rem; /* 아이콘과 텍스트 간격 */
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6); /* 배경 어둡게 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050; /* 부트스트랩 모달 z-index 와 유사하게 */
}

.detail-modal {
  background: white;
  border-radius: 12px; /* 둥글기 조정 */
  max-width: 550px; /* 최대 너비 조정 */
  width: 90%;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15); /* 그림자 추가 */
  max-height: 85vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem; /* 패딩 조정 */
  border-bottom: 1px solid #e9ecef;
  background-color: #f8f9fa; /* 헤더 배경색 추가 */
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}

.modal-header h3 {
  margin: 0;
  color: #343a40; /* 제목 색상 변경 */
  font-size: 1.25rem; /* 폰트 크기 조정 */
  font-weight: 600;
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 1.5rem; /* 아이콘 크기 조정 */
  color: #6c757d;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  line-height: 1;
  opacity: 0.7;
}

.btn-close:hover {
  opacity: 1;
  color: #000;
}

.modal-body {
  padding: 1.5rem; /* 패딩 조정 */
  flex-grow: 1;
}

.stock-detail {
  display: flex;
  flex-direction: column;
  gap: 1.25rem; /* 항목 간 간격 조정 */
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem; /* 라벨과 값 사이 간격 조정 */
}

.detail-item label {
  font-weight: 600; /* 폰트 굵기 조정 */
  color: #495057; /* 라벨 색상 변경 */
  font-size: 0.9rem;
}

.detail-item span,
.detail-item p {
  color: #555; /* 값 텍스트 색상 변경 */
  font-size: 0.95rem; /* 폰트 크기 조정 */
  margin: 0;
  line-height: 1.5;
}

.modal-footer {
  display: flex;
  gap: 0.75rem; /* 버튼 간 간격 조정 */
  padding: 1.25rem; /* 패딩 조정 */
  border-top: 1px solid #e9ecef;
  background-color: #f8f9fa; /* 푸터 배경색 추가 */
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}

.modal-footer .btn {
  flex: 1;
  padding: 0.6rem 1rem; /* 버튼 패딩 조정 */
  font-size: 0.9rem; /* 버튼 폰트 크기 조정 */
  font-weight: 500;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .recommendation-page {
    padding: 1.5rem 0.5rem; /* 모바일 패딩 조정 */
  }

  .page-title {
    font-size: 1.8rem; /* 모바일 제목 폰트 크기 */
  }

  .section-title {
    font-size: 1.4rem; /* 모바일 섹션 제목 폰트 크기 */
  }

  .card-actions {
    flex-direction: column; /* 모바일에서 버튼 세로 정렬 */
    gap: 0.5rem;
  }

  .card-actions .btn {
    width: 100%; /* 버튼 너비 100% */
  }

  .action-section .row {
    flex-direction: column;
    gap: 0.75rem; /* 모바일에서 하단 버튼 간격 */
  }
  .action-section .btn {
    width: 100%;
  }

  .modal-header h3 {
    font-size: 1.1rem;
  }
  .modal-body {
    padding: 1rem;
  }
  .modal-footer {
    padding: 1rem;
    flex-direction: column; /* 모달 푸터 버튼 세로 정렬 */
  }
}
</style>
