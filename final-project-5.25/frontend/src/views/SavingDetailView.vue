<template>
  <div class="saving-detail-container">
    <!-- 로딩 인디케이터 -->
    <div v-if="loading" class="status-indicator loading-indicator">
      <div class="spinner"></div>
      <p>상품 상세 정보를 불러오는 중입니다. 잠시만 기다려주세요...</p>
    </div>

    <!-- 상품 정보 표시 -->
    <div v-else-if="productDetail && optionList.length" class="content-wrapper">
      <header class="product-header">
        <div class="bank-logo-wrapper">
          <!-- 은행 로고 (가상) -->
          <i class="fas fa-landmark fa-2x bank-icon"></i>
        </div>
        <h1 class="product-name">{{ productDetail.fin_prdt_nm }}</h1>
        <p class="bank-name">
          <i class="fas fa-university"></i> {{ productDetail.kor_co_nm }}
        </p>
      </header>

      <div class="details-grid">
        <!-- 상품 개요 -->
        <section class="detail-card product-summary">
          <h2 class="section-title">
            <i class="fas fa-info-circle"></i> 상품 개요
          </h2>
          <ul class="info-list">
            <li>
              <strong>가입 방법:</strong>
              <span>{{ productDetail.join_way }}</span>
            </li>
            <li>
              <strong>가입 대상:</strong>
              <span>{{ productDetail.join_member }}</span>
            </li>
            <li>
              <strong>가입 제한:</strong>
              <span>{{ joinDenyText(productDetail.join_deny) }}</span>
            </li>
          </ul>
        </section>

        <!-- 금리 정보 -->
        <section class="detail-card interest-options">
          <h2 class="section-title">
            <i class="fas fa-percent"></i> 금리 정보
          </h2>
          <div class="options-table-wrapper">
            <table class="options-table">
              <thead>
                <tr>
                  <th>저축 기간</th>
                  <th>금리 유형</th>
                  <th>기본 금리</th>
                  <th>최고 우대금리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="opt in sortedOptionList" :key="opt.id">
                  <td>{{ opt.save_trm }}개월</td>
                  <td>{{ opt.intr_rate_type_nm }}</td>
                  <td>{{ opt.intr_rate ?? "N/A" }}%</td>
                  <td class="rate-highlight">{{ opt.intr_rate2 ?? "N/A" }}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- 우대 조건 -->
        <section
          v-if="productDetail.spcl_cnd"
          class="detail-card special-conditions"
        >
          <h2 class="section-title"><i class="fas fa-star"></i> 우대 조건</h2>
          <div class="content-box">
            <p>{{ productDetail.spcl_cnd }}</p>
          </div>
        </section>

        <!-- 기타 유의사항 -->
        <section v-if="productDetail.etc_note" class="detail-card etc-notes">
          <h2 class="section-title">
            <i class="fas fa-sticky-note"></i> 기타 유의사항
          </h2>
          <div class="content-box">
            <p>{{ productDetail.etc_note }}</p>
          </div>
        </section>
      </div>

      <div class="actions">
        <button @click="goBack" class="btn btn-outline">
          <i class="fas fa-arrow-left"></i> 목록으로 돌아가기
        </button>
        <!-- <button @click="applyProduct" class="btn btn-primary">가입하기 (예시)</button> -->
      </div>
    </div>

    <!-- 에러 인디케이터 -->
    <div
      v-else-if="!loading && (!productDetail || !optionList.length)"
      class="status-indicator error-indicator"
    >
      <i class="fas fa-exclamation-triangle fa-3x error-icon"></i>
      <h2>정보를 불러올 수 없습니다.</h2>
      <p>
        요청하신 상품 정보를 가져오는 데 실패했습니다. 네트워크 연결을
        확인하거나 잠시 후 다시 시도해 주세요.
      </p>
      <button @click="goBack" class="btn btn-outline">
        <i class="fas fa-arrow-left"></i> 목록으로 돌아가기
      </button>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const fin_prdt_cd = route.params.fin_prdt_cd;
const productDetail = ref(null);
const optionList = ref([]);
const loading = ref(true);

const fetchSavingDetail = async () => {
  loading.value = true;
  try {
    const [optionsRes, productRes] = await Promise.all([
      axios.get(
        `http://127.0.0.1:8000/saving/saving-products-options/${fin_prdt_cd}/`
      ),
      axios.get(
        `http://127.0.0.1:8000/saving/saving-products-detail/${fin_prdt_cd}/`
      ),
    ]);

    optionList.value = optionsRes.data;
    productDetail.value = productRes.data;
  } catch (err) {
    console.error("상품 상세 정보 조회 실패:", err);
    // 사용자에게 보여줄 에러 메시지 처리를 위한 상태 설정도 고려할 수 있습니다.
    productDetail.value = null;
    optionList.value = [];
  } finally {
    loading.value = false;
  }
};

const sortedOptionList = computed(() => {
  return [...optionList.value].sort((a, b) => a.save_trm - b.save_trm);
});

const joinDenyText = (value) => {
  switch (value) {
    case 1:
      return "제한없음";
    case 2:
      return "서민전용";
    case 3:
      return "일부제한";
    default:
      return "정보없음";
  }
};

const goBack = () => {
  router.push("/saving");
};

onMounted(fetchSavingDetail);
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css");

:root {
  --primary-color: #5e72e4; /* 좀 더 부드러운 파란색 */
  --secondary-color: #f4f5f7; /* 밝은 회색 배경 */
  --text-color: #32325d; /* 어두운 텍스트 색상 */
  --text-light-color: #525f7f; /* 약간 밝은 텍스트 */
  --border-color: #e9ecef; /* 부드러운 경계선 */
  --card-bg: #ffffff;
  --highlight-color: #2dce89; /* 금리 강조색 */
  --error-color: #f5365c; /* 에러 색상 */
}

.saving-detail-container {
  max-width: 960px;
  margin: 30px auto;
  padding: 20px;
  background-color: var(--secondary-color);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  color: var(--text-color);
  border-radius: 16px;
}

.status-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 20px;
  text-align: center;
  border-radius: 12px;
  background-color: var(--card-bg);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.loading-indicator .spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 25px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-indicator p {
  font-size: 1.1rem;
  color: var(--text-light-color);
}

.error-indicator .error-icon {
  color: var(--error-color);
  margin-bottom: 20px;
}
.error-indicator h2 {
  font-size: 1.5rem;
  color: var(--error-color);
  margin-bottom: 10px;
}
.error-indicator p {
  font-size: 1rem;
  color: var(--text-light-color);
  margin-bottom: 25px;
  line-height: 1.6;
}

.content-wrapper {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.product-header {
  text-align: center;
  margin-bottom: 35px;
  padding: 30px 20px;
  background-color: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.bank-logo-wrapper {
  margin-bottom: 15px;
}
.bank-icon {
  color: var(--primary-color);
}

.product-name {
  font-size: 2.3rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 10px;
  line-height: 1.3;
}

.bank-name {
  font-size: 1.1rem;
  color: var(--text-light-color);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.bank-name i {
  color: var(--primary-color);
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr; /* 기본 1단 */
  gap: 25px;
}

/* 데스크탑에서는 2단으로 표시 */
@media (min-width: 768px) {
  .details-grid {
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  }
}

.detail-card {
  background-color: var(--card-bg);
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.detail-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-title i {
  font-size: 1.2rem;
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.info-list li {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px dashed var(--border-color);
  font-size: 0.95rem;
}
.info-list li:last-child {
  border-bottom: none;
}
.info-list strong {
  font-weight: 600;
  color: var(--text-color);
  margin-right: 10px;
}
.info-list span {
  color: var(--text-light-color);
  text-align: right;
}

.options-table-wrapper {
  overflow-x: auto;
}

.options-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.options-table th,
.options-table td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
  font-size: 0.9rem;
  color: var(--text-light-color);
}

.options-table th {
  background-color: #f8f9fe; /* 테이블 헤더 배경색 */
  font-weight: 600;
  color: var(--text-color);
  white-space: nowrap;
}

.options-table tbody tr:hover {
  background-color: #f0f3ff;
}

.options-table td:first-child,
.options-table th:first-child {
  text-align: center;
}
.options-table td:nth-child(3),
.options-table th:nth-child(3),
.options-table td:nth-child(4),
.options-table th:nth-child(4) {
  text-align: right;
}

.rate-highlight {
  font-weight: bold;
  color: var(--highlight-color);
}

.content-box {
  background-color: #fdfdfd;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--text-light-color);
}
.content-box p {
  margin: 0;
  white-space: pre-wrap;
}

.actions {
  margin-top: 35px;
  text-align: center;
}

.btn {
  padding: 12px 28px;
  border: none;
  border-radius: 30px; /* 좀 더 둥근 버튼 */
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 0 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}
.btn-primary:hover {
  background-color: #4357d0; /* 호버 시 약간 어둡게 */
  transform: translateY(-2px);
  box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
}

.btn-outline {
  background-color: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
}
.btn-outline:hover {
  background-color: var(--primary-color);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
}

.fas {
  margin-right: 8px;
}
</style>
