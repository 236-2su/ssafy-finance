<template>
  <div class="recommendation-page-container py-5">
    <div class="text-center mb-5">
      <h1 class="fw-bold">맞춤형 투자 추천</h1>
      <p class="lead text-muted">
        설문조사 결과를 바탕으로 추천된 투자 상품입니다.
      </p>
    </div>

    <p
      v-if="userStore.isLogin && !surveyCompleted"
      class="alert alert-warning text-center"
    >
      정확한 추천을 위해 먼저
      <RouterLink to="/survey" class="text-primary fw-bold"
        >투자 성향 설문조사</RouterLink
      >를 완료해주세요.
    </p>

    <div class="text-center mb-5" v-if="userStore.isLogin && surveyCompleted">
      <button
        class="btn btn-lg btn-primary px-5"
        @click="getRecommendations"
        :disabled="isLoading"
      >
        <span
          v-if="isLoading"
          class="spinner-border spinner-border-sm me-2"
          role="status"
          aria-hidden="true"
        ></span>
        {{ isLoading ? "추천받는 중..." : "내 추천 다시 받기" }}
      </button>
    </div>

    <div v-if="error" class="alert alert-danger mt-4" role="alert">
      {{ error }}
    </div>

    <div
      v-if="
        !isLoading &&
        !error &&
        (recommendedDeposits.length ||
          recommendedSavings.length ||
          aiStockRecommendation)
      "
    >
      <!-- 추천 주식 섹션 -->
      <section class="mb-5" v-if="aiStockRecommendation">
        <div class="d-flex align-items-center mb-3">
          <i class="bi bi-graph-up-arrow fs-2 me-2"></i>
          <h2 class="mb-0 fw-semibold">추천 주식</h2>
        </div>
        <p class="text-muted ms-1">투자 성향에 맞는 주식을 추천해드립니다.</p>

        <div class="row" v-if="parsedStockRecommendations.length">
          <div
            v-for="(stock, index) in parsedStockRecommendations"
            :key="`stock-${index}`"
            class="col-md-4 mb-4"
          >
            <div class="card recommendation-card stock-card h-100 shadow-sm">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title fw-bold">{{ stock.name }}</h5>
                <p class="card-text stock-description mb-4">
                  {{ stock.reason }}
                </p>
                <div class="mt-auto text-end">
                  <button
                    :class="[
                      'btn',
                      'btn-sm',
                      'w-100',
                      isStockInterested(stock.name)
                        ? 'btn-danger'
                        : 'btn-primary',
                    ]"
                    @click="handleAddInterestStock(stock)"
                  >
                    <i
                      :class="[
                        'bi',
                        isStockInterested(stock.name)
                          ? 'bi-heart-fill'
                          : 'bi-heart',
                        'me-1',
                      ]"
                    ></i>
                    {{
                      isStockInterested(stock.name)
                        ? "관심 주식 제거"
                        : "관심 주식 추가"
                    }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 추천 예적금 섹션 -->
      <section
        class="mb-5"
        v-if="recommendedDeposits.length || recommendedSavings.length"
      >
        <div class="d-flex align-items-center mb-3">
          <i class="bi bi-piggy-bank fs-2 me-2"></i>
          <h2 class="mb-0 fw-semibold">추천 예적금</h2>
        </div>
        <p class="text-muted ms-1">
          안전하고 수익성 높은 예적금 상품을 추천해드립니다.
        </p>
        <div class="row">
          <!-- 예금 상품 -->
          <div
            v-for="product in recommendedDeposits"
            :key="`dep-${product.id}`"
            class="col-md-6 mb-4"
          >
            <div
              class="card recommendation-card deposit-card h-100 shadow-sm"
              @click="handleProductDetail(product, 'deposit')"
              style="cursor: pointer"
            >
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <h5 class="card-title fw-bold">
                      {{ product.fin_prdt_nm }}
                    </h5>
                    <h6 class="card-subtitle mb-2 text-muted">
                      {{ product.kor_co_nm }}
                    </h6>
                  </div>
                  <span
                    class="badge bg-success-light text-success-dark rounded-pill px-3 py-2"
                    >{{ product.intr_rate2 }}%</span
                  >
                </div>
                <p class="card-text mt-3 product-description">
                  기본 {{ product.intr_rate }}% ({{
                    product.intr_rate_type_nm
                  }})<br />
                  <small>가입 기간: {{ product.save_trm }}개월</small>
                </p>
                <div class="mt-auto pt-3 text-end">
                  <!-- 상세 정보 버튼 제거 -->
                  <button
                    class="btn btn-primary btn-sm"
                    @click.stop="handleFindBranch(product)"
                  >
                    <i class="bi bi-geo-alt me-1"></i> 지점 찾기
                  </button>
                </div>
              </div>
            </div>
          </div>
          <!-- 적금 상품 -->
          <div
            v-for="product in recommendedSavings"
            :key="`sav-${product.id}`"
            class="col-md-6 mb-4"
          >
            <div
              class="card recommendation-card saving-card h-100 shadow-sm"
              @click="handleProductDetail(product, 'saving')"
              style="cursor: pointer"
            >
              <div class="card-body d-flex flex-column">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <h5 class="card-title fw-bold">
                      {{ product.fin_prdt_nm }}
                    </h5>
                    <h6 class="card-subtitle mb-2 text-muted">
                      {{ product.kor_co_nm }}
                    </h6>
                  </div>
                  <span
                    class="badge bg-success-light text-success-dark rounded-pill px-3 py-2"
                    >{{ product.intr_rate2 }}%</span
                  >
                </div>
                <p class="card-text mt-3 product-description">
                  기본 {{ product.intr_rate }}% ({{
                    product.intr_rate_type_nm
                  }})<br />
                  <small
                    >가입 기간: {{ product.save_trm }}개월,
                    {{ product.rsrv_type_nm }}</small
                  >
                </p>
                <div class="mt-auto pt-3 text-end">
                  <!-- 상세 정보 버튼 제거 -->
                  <button
                    class="btn btn-primary btn-sm"
                    @click.stop="handleFindBranch(product)"
                  >
                    <i class="bi bi-geo-alt me-1"></i> 지점 찾기
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
    <div
      v-else-if="
        !isLoading &&
        !error &&
        initialLoadDone &&
        !(
          recommendedDeposits.length ||
          recommendedSavings.length ||
          aiStockRecommendation
        )
      "
      class="alert alert-info text-center"
    >
      추천드릴 상품이 없거나, 추천을 받기 위한 조건이 충족되지 않았습니다.
      <br />
      <RouterLink to="/survey" class="text-primary fw-bold"
        >투자 성향 설문조사</RouterLink
      >를 다시 진행해보세요.
    </div>

    <!-- 하단 버튼 -->
    <div class="mt-5 pt-4 border-top text-center">
      <div class="row">
        <div class="col-md-6 mb-3 mb-md-0">
          <button
            class="btn btn-outline-secondary w-100 py-3"
            @click="redoSurvey"
          >
            <i class="bi bi-arrow-clockwise me-2"></i> 설문조사 다시하기
          </button>
        </div>
        <div class="col-md-6">
          <button class="btn btn-primary w-100 py-3" @click="goToProfile">
            <i class="bi bi-person-fill me-2"></i> 프로필로 이동
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"; // computed 추가
import axios from "axios";
import { useUserStore } from "@/stores/user";
import { useRouter, RouterLink } from "vue-router"; // RouterLink import

const userStore = useUserStore();
const router = useRouter();

const recommendedDeposits = ref([]);
const recommendedSavings = ref([]);
const aiStockRecommendation = ref(null); // 예: "안정적인 성장주 위주 포트폴리오: 삼성전자(50%), SK하이닉스(30%), 현대차(20%)"
const isLoading = ref(false);
const error = ref(null);
const surveyCompleted = ref(false);
const initialLoadDone = ref(false);

const API_URL = "/api/ai-recommendations/recommend/";
const interestedStockNames = ref([]); // 관심 주식 이름 목록 (로컬 상태)

// AI 주식 추천 문자열을 파싱하여 객체 배열로 변환하는 computed 속성
const parsedStockRecommendations = computed(() => {
  if (!aiStockRecommendation.value) {
    return [];
  }
  try {
    // AI가 반환하는 형식: "종목명: [이름]\n추천 이유: [설명]\n\n종목명: [이름]\n추천 이유: [설명]..."
    const recommendations = aiStockRecommendation.value.trim().split("\n\n");
    return recommendations
      .map((rec) => {
        const lines = rec.split("\n");
        const nameLine = lines.find((line) => line.startsWith("종목명:"));
        const reasonLine = lines.find((line) => line.startsWith("추천 이유:"));

        const name = nameLine
          ? nameLine.replace("종목명:", "").trim()
          : "정보 없음";
        const reason = reasonLine
          ? reasonLine.replace("추천 이유:", "").trim()
          : "정보 없음";

        return { name, reason };
      })
      .filter((stock) => stock.name !== "정보 없음"); // 유효한 데이터만 필터링
  } catch (error) {
    console.error("Error parsing stock recommendations:", error);
    return [
      {
        name: "추천 파싱 오류",
        reason: "추천 내용을 올바르게 분석하지 못했습니다.",
      },
    ];
  }
});

onMounted(async () => {
  if (userStore.isLogin) {
    try {
      // fetchUserProfile을 호출하면 스토어의 user 상태가 업데이트됨 (interested_stocks 포함)
      await userStore.fetchUserProfile();
      surveyCompleted.value = userStore.user?.survey_completed || false;

      // 스토어의 사용자 정보에서 관심 주식 목록을 가져와 로컬 상태에 반영
      if (userStore.user && Array.isArray(userStore.user.interested_stocks)) {
        interestedStockNames.value = [...userStore.user.interested_stocks];
      } else {
        interestedStockNames.value = [];
        // console.log("onMounted: userStore.user.interested_stocks를 찾을 수 없거나 배열이 아님.");
      }

      if (surveyCompleted.value) {
        getRecommendations();
      }
    } catch (err) {
      console.error("초기 데이터 로드 실패:", err);
      surveyCompleted.value = false;
    }
  } else {
    surveyCompleted.value = false;
  }
});

const getRecommendations = async () => {
  if (!userStore.isLogin) {
    error.value = "추천을 받으려면 로그인이 필요합니다.";
    return;
  }
  if (!surveyCompleted.value) {
    error.value = "AI 추천을 받으려면 먼저 투자 성향 설문조사를 완료해주세요.";
    return;
  }

  isLoading.value = true;
  error.value = null;
  initialLoadDone.value = true; // 추천 시도 플래그

  try {
    const response = await axios.post(
      API_URL,
      {},
      {
        headers: { Authorization: `Token ${userStore.token}` }, // 인증 토큰 추가
      }
    );
    recommendedDeposits.value = response.data.deposit_products || [];
    recommendedSavings.value = response.data.saving_products || [];
    aiStockRecommendation.value =
      response.data.stock_recommendations_ai || null;

    if (
      !recommendedDeposits.value.length &&
      !recommendedSavings.value.length &&
      !aiStockRecommendation.value
    ) {
      // 데이터는 성공적으로 받았으나 추천 내용이 없는 경우
      // error.value = "현재 조건에 맞는 추천 상품이 없습니다."; // 이 메시지는 상단 v-else-if에서 처리
    }
  } catch (err) {
    console.error("AI 추천 요청 실패:", err);
    if (err.response) {
      if (err.response.status === 401) {
        error.value = "로그인이 필요합니다. 로그인 후 다시 시도해주세요.";
      } else if (err.response.data && err.response.data.error) {
        error.value = `추천 오류: ${err.response.data.error}`;
      } else {
        error.value =
          "추천을 받아오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.";
      }
    } else {
      error.value = "네트워크 오류 또는 서버에 연결할 수 없습니다.";
    }
  } finally {
    isLoading.value = false;
  }
};

// 버튼 핸들러

// 주식이 관심 목록에 있는지 확인하는 함수
const isStockInterested = (stockName) => {
  return interestedStockNames.value.includes(stockName);
};

const handleAddInterestStock = async (stock) => {
  // async 추가
  const stockName = stock.name;
  if (!userStore.isLogin) {
    alert("로그인이 필요합니다.");
    router.push("/login");
    return;
  }

  try {
    if (isStockInterested(stockName)) {
      await userStore.removeStockFromWatchlist(stockName); // userStore 액션 호출
      // 스토어 상태 변경을 로컬 상태에 반영 (선택적, 스토어가 단일 진실 공급원이라면)
      // 또는 fetchUserProfile을 다시 호출하여 최신 상태를 가져올 수도 있음
      const index = interestedStockNames.value.indexOf(stockName);
      if (index > -1) interestedStockNames.value.splice(index, 1);
      console.log(`관심 주식 제거 완료: ${stockName}`);
    } else {
      await userStore.addStockToWatchlist(stockName); // userStore 액션 호출
      // 스토어 상태 변경을 로컬 상태에 반영
      if (!interestedStockNames.value.includes(stockName)) {
        interestedStockNames.value.push(stockName);
      }
      console.log(`관심 주식 추가 완료: ${stockName}`);
    }
    // userStore의 user.interested_stocks가 변경되었으므로, interestedStockNames를 다시 동기화 할 수 있음
    // if (userStore.user && Array.isArray(userStore.user.interested_stocks)) {
    //   interestedStockNames.value = [...userStore.user.interested_stocks];
    // }
  } catch (error) {
    console.error("관심 주식 처리 중 오류:", error);
    alert("관심 주식 처리 중 오류가 발생했습니다. 로그인 상태를 확인해주세요.");
  }
};

const handleProductDetail = (product, type) => {
  console.log(`${type} 상품 상세 정보:`, product);
  if (!product || !product.fin_prdt_cd) {
    console.error("상품 정보 또는 fin_prdt_cd가 없습니다.", product);
    alert("상품 정보를 불러올 수 없습니다.");
    return;
  }
  router.push({
    name: "SavingDetailView",
    params: { fin_prdt_cd: product.fin_prdt_cd },
  });
};

const handleFindBranch = (product) => {
  console.log("지점 찾기:", product.kor_co_nm);
  // 은행명 기반 지도 검색 페이지로 이동 또는 카카오맵 API 연동
  const searchQuery = `${product.kor_co_nm} 지점`;
  window.open(`https://map.kakao.com/link/search/${searchQuery}`, "_blank");
};

// handleFindBranch 함수 중복 제거됨

const redoSurvey = () => {
  router.push("/survey");
};

const goToProfile = () => {
  router.push("/profile");
};

// 페이지 첫 로드 시 또는 로그인 상태 변경 시 추천 자동 호출
// onMounted에서 surveyCompleted.value === true 일 때 getRecommendations() 호출하도록 수정됨.
</script>

<style scoped>
.recommendation-page-container {
  max-width: 1000px; /* 기존 900px에서 약간 넓힘 */
  margin: 0 auto;
  font-family: "Pretendard", sans-serif; /* 폰트 적용 (필요시 전역 설정) */
}

.fw-bold {
  font-weight: 700 !important;
}
.fw-semibold {
  font-weight: 600 !important;
}

.recommendation-card {
  border: none; /* 테두리 제거 */
  border-radius: 15px; /* 둥근 모서리 */
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.recommendation-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
}

/* 주식 카드 스타일 */
.stock-card {
  background: linear-gradient(
    135deg,
    #6f42c1,
    #4d2c91
  ); /* 보라색 계열 그라데이션 */
  color: white;
}
.stock-card .card-title {
  color: #f8f9fa; /* 밝은 제목 색상 */
}
.stock-card .stock-description {
  font-size: 0.95rem;
  color: #e9ecef; /* 밝은 설명 색상 */
  line-height: 1.6;
  max-height: 100px; /* 여러 줄일 경우 제한 */
  overflow-y: auto; /* 내용 많을 시 스크롤 */
}
.stock-card .btn-outline-primary {
  border-color: rgba(255, 255, 255, 0.8);
  color: rgba(255, 255, 255, 0.9);
}
.stock-card .btn-outline-primary:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}
.stock-card .btn-primary {
  background-color: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 255, 255, 0.9);
  color: #6f42c1;
}
.stock-card .btn-primary:hover {
  background-color: white;
  color: #6f42c1;
}

/* 예적금 카드 스타일 */
.deposit-card,
.saving-card {
  background-color: #f0fff0; /* 연한 녹색 배경 */
  /* background: linear-gradient(135deg, #28a745, #1e7e34); */ /* 녹색 계열 그라데이션 */
  /* color: white; */
}

.deposit-card .card-title,
.saving-card .card-title {
  color: #198754; /* 진한 녹색 제목 */
}
.deposit-card .card-subtitle,
.saving-card .card-subtitle {
  color: #555;
}

.product-description {
  font-size: 0.9rem;
  color: #333;
  line-height: 1.5;
}

.badge.bg-success-light {
  background-color: #d1e7dd !important; /* 부트스트랩 success-subtle 유사 */
}
.text-success-dark {
  color: #0a3622 !important; /* 부트스트랩 success-emphasis 유사 */
}

.btn-outline-primary {
  border-color: #0d6efd;
  color: #0d6efd;
}
.btn-outline-primary:hover {
  background-color: #0d6efd;
  color: white;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}
.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

.btn-outline-secondary {
  border-color: #6c757d;
  color: #6c757d;
}
.btn-outline-secondary:hover {
  background-color: #6c757d;
  color: white;
}

/* 아이콘 스타일 (Bootstrap Icons 사용 가정) */
.bi {
  vertical-align: -0.125em; /* 아이콘 정렬 */
}

/* 로딩 스피너 정렬 */
.spinner-border-sm {
  vertical-align: -0.125em;
}

/* 알림 메시지 스타일 */
.alert {
  border-radius: 8px;
}

/* 카드 내 버튼 정렬 */
.card-body .mt-auto {
  margin-top: auto !important;
}

/* 반응형 폰트 크기 (선택 사항) */
@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }
  h2 {
    font-size: 1.5rem;
  }
  .btn-lg {
    font-size: 1rem;
    padding: 0.5rem 1rem;
  }
  .recommendation-card .card-title {
    font-size: 1.1rem;
  }
}

pre {
  /* 기존 pre 스타일 유지 또는 수정 */
  white-space: pre-wrap;
  word-wrap: break-word;
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  color: #212529;
}
</style>
