<template>
  <div class="survey-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="survey-card">
            <div class="survey-header">
              <h2 class="survey-title">투자 성향 설문조사</h2>
              <p class="survey-subtitle">
                맞춤형 투자 상품 추천을 위해 몇 가지 질문에 답해주세요.
              </p>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
              </div>
              <span class="progress-text">{{ currentStep }}/{{ totalSteps }}</span>
            </div>

            <form @submit.prevent="submitSurvey" class="survey-form">
              <!-- Step 1: 주식 투자 경험 -->
              <div v-if="currentStep === 1" class="survey-step">
                <h3 class="step-title">주식 투자 경험이 어느 정도인가요?</h3>
                <div class="options-grid">
                  <label v-for="option in stockExperienceOptions" :key="option.value" class="option-card">
                    <input 
                      type="radio" 
                      v-model="surveyData.stock_experience" 
                      :value="option.value"
                      class="option-input"
                    >
                    <div class="option-content">
                      <i :class="option.icon" class="option-icon"></i>
                      <h4>{{ option.label }}</h4>
                      <p>{{ option.description }}</p>
                    </div>
                  </label>
                </div>
              </div>

              <!-- Step 2: 투자 성향 -->
              <div v-if="currentStep === 2" class="survey-step">
                <h3 class="step-title">투자 성향은 어떻게 되시나요?</h3>
                <div class="options-grid">
                  <label v-for="option in investmentStyleOptions" :key="option.value" class="option-card">
                    <input 
                      type="radio" 
                      v-model="surveyData.investment_style" 
                      :value="option.value"
                      class="option-input"
                    >
                    <div class="option-content">
                      <i :class="option.icon" class="option-icon"></i>
                      <h4>{{ option.label }}</h4>
                      <p>{{ option.description }}</p>
                    </div>
                  </label>
                </div>
              </div>

              <!-- Step 3: 월 투자 금액 -->
              <div v-if="currentStep === 3" class="survey-step">
                <h3 class="step-title">월 투자 가능 금액은 얼마인가요?</h3>
                <div class="options-grid">
                  <label v-for="option in monthlyAmountOptions" :key="option.value" class="option-card">
                    <input 
                      type="radio" 
                      v-model="surveyData.monthly_investment_amount" 
                      :value="option.value"
                      class="option-input"
                    >
                    <div class="option-content">
                      <i :class="option.icon" class="option-icon"></i>
                      <h4>{{ option.label }}</h4>
                      <p>{{ option.description }}</p>
                    </div>
                  </label>
                </div>
              </div>

              <!-- Step 4: 투자 목적 -->
              <div v-if="currentStep === 4" class="survey-step">
                <h3 class="step-title">투자 목적은 무엇인가요?</h3>
                <div class="options-grid">
                  <label v-for="option in investmentGoalOptions" :key="option.value" class="option-card">
                    <input 
                      type="radio" 
                      v-model="surveyData.investment_goal" 
                      :value="option.value"
                      class="option-input"
                    >
                    <div class="option-content">
                      <i :class="option.icon" class="option-icon"></i>
                      <h4>{{ option.label }}</h4>
                      <p>{{ option.description }}</p>
                    </div>
                  </label>
                </div>
              </div>

              <!-- Step 5: 보유 주식 -->
              <div v-if="currentStep === 5" class="survey-step">
                <h3 class="step-title">현재 보유하고 있는 주식이 있나요?</h3>
                <div class="stock-input-section">
                  <div class="input-group mb-3">
                    <input 
                      type="text" 
                      v-model="newOwnedStock.code" 
                      placeholder="주식 코드 (예: 005930)"
                      class="form-control"
                    >
                    <input 
                      type="text" 
                      v-model="newOwnedStock.name" 
                      placeholder="주식명 (예: 삼성전자)"
                      class="form-control"
                    >
                    <button type="button" @click="addOwnedStock" class="btn btn-primary">추가</button>
                  </div>
                  <div class="stock-list">
                    <div v-for="(stock, index) in surveyData.owned_stocks" :key="index" class="stock-item">
                      <span>{{ stock.name }} ({{ stock.code }})</span>
                      <button type="button" @click="removeOwnedStock(index)" class="btn btn-sm btn-outline-danger">
                        <i class="fas fa-times"></i>
                      </button>
                    </div>
                  </div>
                  <p class="text-muted mt-2">보유 주식이 없다면 다음 단계로 넘어가세요.</p>
                </div>
              </div>

              <!-- Step 6: 관심 주식 -->
              <div v-if="currentStep === 6" class="survey-step">
                <h3 class="step-title">관심있는 주식이 있나요?</h3>
                <div class="stock-input-section">
                  <div class="input-group mb-3">
                    <input 
                      type="text" 
                      v-model="newInterestedStock.code" 
                      placeholder="주식 코드 (예: 035720)"
                      class="form-control"
                    >
                    <input 
                      type="text" 
                      v-model="newInterestedStock.name" 
                      placeholder="주식명 (예: 카카오)"
                      class="form-control"
                    >
                    <button type="button" @click="addInterestedStock" class="btn btn-primary">추가</button>
                  </div>
                  <div class="stock-list">
                    <div v-for="(stock, index) in surveyData.interested_stocks" :key="index" class="stock-item">
                      <span>{{ stock.name }} ({{ stock.code }})</span>
                      <button type="button" @click="removeInterestedStock(index)" class="btn btn-sm btn-outline-danger">
                        <i class="fas fa-times"></i>
                      </button>
                    </div>
                  </div>
                  <p class="text-muted mt-2">관심 주식이 없다면 다음 단계로 넘어가세요.</p>
                </div>
              </div>

              <!-- Navigation Buttons -->
              <div class="survey-navigation">
                <button 
                  type="button" 
                  @click="previousStep" 
                  v-if="currentStep > 1"
                  class="btn btn-outline-secondary"
                >
                  <i class="fas fa-arrow-left me-2"></i>이전
                </button>
                
                <button 
                  type="button" 
                  @click="nextStep" 
                  v-if="currentStep < totalSteps"
                  :disabled="!isCurrentStepValid"
                  class="btn btn-primary ms-auto"
                >
                  다음<i class="fas fa-arrow-right ms-2"></i>
                </button>
                
                <button 
                  type="submit" 
                  v-if="currentStep === totalSteps"
                  :disabled="loading || !isCurrentStepValid"
                  class="btn btn-success ms-auto"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  설문 완료
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="modal-overlay" @click="closeSuccessModal">
      <div class="success-modal" @click.stop>
        <div class="success-content">
          <i class="fas fa-check-circle success-icon"></i>
          <h3>설문조사 완료!</h3>
          <p>맞춤형 투자 상품 추천을 확인해보세요.</p>
          <div class="modal-buttons">
            <button @click="goToRecommendations" class="btn btn-primary">추천 보기</button>
            <button @click="goToProfile" class="btn btn-outline-secondary">프로필로 이동</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

const router = useRouter()
const userStore = useUserStore()

const currentStep = ref(1)
const totalSteps = 6
const loading = ref(false)
const showSuccessModal = ref(false)

const surveyData = ref({
  stock_experience: '',
  investment_style: '',
  monthly_investment_amount: '',
  investment_goal: '',
  owned_stocks: [],
  interested_stocks: []
})

const newOwnedStock = ref({ code: '', name: '' })
const newInterestedStock = ref({ code: '', name: '' })

const stockExperienceOptions = [
  {
    value: 'none',
    label: '투자 경험 없음',
    description: '주식 투자를 해본 적이 없습니다',
    icon: 'fas fa-seedling'
  },
  {
    value: 'beginner',
    label: '초보 (1년 미만)',
    description: '주식 투자를 시작한 지 1년이 안 되었습니다',
    icon: 'fas fa-leaf'
  },
  {
    value: 'intermediate',
    label: '중급 (1-3년)',
    description: '1년 이상 3년 미만의 투자 경험이 있습니다',
    icon: 'fas fa-chart-line'
  },
  {
    value: 'advanced',
    label: '고급 (3년 이상)',
    description: '3년 이상의 풍부한 투자 경험이 있습니다',
    icon: 'fas fa-trophy'
  }
]

const investmentStyleOptions = [
  {
    value: 'conservative',
    label: '안전형',
    description: '원금 보장을 중시하며 안정적인 수익을 추구합니다',
    icon: 'fas fa-shield-alt'
  },
  {
    value: 'moderate',
    label: '중립형',
    description: '적당한 위험을 감수하며 균형잡힌 투자를 선호합니다',
    icon: 'fas fa-balance-scale'
  },
  {
    value: 'aggressive',
    label: '공격형',
    description: '높은 수익을 위해 위험을 감수할 수 있습니다',
    icon: 'fas fa-rocket'
  }
]

const monthlyAmountOptions = [
  {
    value: 'under_50',
    label: '50만원 미만',
    description: '소액으로 투자를 시작하고 싶습니다',
    icon: 'fas fa-coins'
  },
  {
    value: '50_100',
    label: '50-100만원',
    description: '적당한 금액으로 꾸준히 투자하고 싶습니다',
    icon: 'fas fa-wallet'
  },
  {
    value: '100_300',
    label: '100-300만원',
    description: '여유 자금으로 본격적인 투자를 하고 싶습니다',
    icon: 'fas fa-money-bill-wave'
  },
  {
    value: 'over_300',
    label: '300만원 이상',
    description: '충분한 자금으로 다양한 투자를 하고 싶습니다',
    icon: 'fas fa-gem'
  }
]

const investmentGoalOptions = [
  {
    value: 'short_term',
    label: '단기 수익',
    description: '1년 이내 빠른 수익을 목표로 합니다',
    icon: 'fas fa-bolt'
  },
  {
    value: 'long_term',
    label: '장기 투자',
    description: '5년 이상 장기적인 자산 증식을 목표로 합니다',
    icon: 'fas fa-mountain'
  },
  {
    value: 'retirement',
    label: '은퇴 준비',
    description: '노후를 위한 안정적인 자산 형성이 목표입니다',
    icon: 'fas fa-umbrella'
  },
  {
    value: 'emergency_fund',
    label: '비상 자금',
    description: '예상치 못한 상황에 대비한 자금 마련이 목표입니다',
    icon: 'fas fa-first-aid'
  }
]

const progressPercentage = computed(() => {
  return (currentStep.value / totalSteps) * 100
})

const isCurrentStepValid = computed(() => {
  switch (currentStep.value) {
    case 1:
      return surveyData.value.stock_experience !== ''
    case 2:
      return surveyData.value.investment_style !== ''
    case 3:
      return surveyData.value.monthly_investment_amount !== ''
    case 4:
      return surveyData.value.investment_goal !== ''
    case 5:
    case 6:
      return true // 주식 정보는 선택사항
    default:
      return false
  }
})

const nextStep = () => {
  if (currentStep.value < totalSteps && isCurrentStepValid.value) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const addOwnedStock = () => {
  if (newOwnedStock.value.code && newOwnedStock.value.name) {
    surveyData.value.owned_stocks.push({
      code: newOwnedStock.value.code,
      name: newOwnedStock.value.name
    })
    newOwnedStock.value = { code: '', name: '' }
  }
}

const removeOwnedStock = (index) => {
  surveyData.value.owned_stocks.splice(index, 1)
}

const addInterestedStock = () => {
  if (newInterestedStock.value.code && newInterestedStock.value.name) {
    surveyData.value.interested_stocks.push({
      code: newInterestedStock.value.code,
      name: newInterestedStock.value.name
    })
    newInterestedStock.value = { code: '', name: '' }
  }
}

const removeInterestedStock = (index) => {
  surveyData.value.interested_stocks.splice(index, 1)
}

const submitSurvey = async () => {
  if (!isCurrentStepValid.value) return
  
  loading.value = true
  try {
    const response = await axios.post('/api/accounts/survey/', surveyData.value)
    console.log('Survey submitted:', response.data)
    showSuccessModal.value = true
  } catch (error) {
    console.error('Survey submission error:', error)
    alert('설문조사 제출 중 오류가 발생했습니다.')
  } finally {
    loading.value = false
  }
}

const closeSuccessModal = () => {
  showSuccessModal.value = false
}

const goToRecommendations = () => {
  showSuccessModal.value = false
  router.push('/recommendations')
}

const goToProfile = () => {
  showSuccessModal.value = false
  router.push('/profile')
}

onMounted(async () => {
  // 인증 체크
  const isAuthenticated = await userStore.checkAuthAndRedirect(router);
  if (!isAuthenticated) {
    return;
  }

  // 이미 설문조사를 완료한 사용자인지 확인
  if (userStore.user && userStore.user.survey_completed) {
    router.push('/profile')
  }
})
</script>

<style scoped>
.survey-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 0;
}

.survey-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.survey-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
}

.survey-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.survey-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1.5rem;
}

.progress-bar {
  background: rgba(255, 255, 255, 0.2);
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  background: white;
  height: 100%;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.9rem;
  opacity: 0.8;
}

.survey-form {
  padding: 2rem;
}

.survey-step {
  min-height: 400px;
}

.step-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.option-card {
  border: 2px solid #e9ecef;
  border-radius: 15px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.option-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.option-input {
  display: none;
}

.option-input:checked + .option-content {
  color: #667eea;
}

.option-input:checked + .option-content .option-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.option-card:has(.option-input:checked) {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

.option-content {
  text-align: center;
}

.option-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  background: #f8f9fa;
  color: #6c757d;
  font-size: 1.5rem;
  transition: all 0.3s ease;
}

.option-content h4 {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333;
}

.option-content p {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
  margin: 0;
}

.stock-input-section {
  max-width: 600px;
  margin: 0 auto;
}

.stock-list {
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.stock-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.survey-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
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

.success-modal {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  max-width: 400px;
  width: 90%;
  text-align: center;
}

.success-content {
  padding: 1rem;
}

.success-icon {
  font-size: 4rem;
  color: #28a745;
  margin-bottom: 1rem;
}

.success-content h3 {
  color: #333;
  margin-bottom: 1rem;
}

.success-content p {
  color: #666;
  margin-bottom: 2rem;
}

.modal-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.modal-buttons .btn {
  flex: 1;
}

@media (max-width: 768px) {
  .survey-page {
    padding: 1rem 0;
  }
  
  .survey-header {
    padding: 1.5rem;
  }
  
  .survey-title {
    font-size: 1.5rem;
  }
  
  .survey-form {
    padding: 1.5rem;
  }
  
  .options-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-buttons {
    flex-direction: column;
  }
}
</style>
