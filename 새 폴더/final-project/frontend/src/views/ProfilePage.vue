<template>
  <div class="profile-page">
    <div class="hero-section">
      <div class="container">
        <div class="hero-content">
          <div class="profile-avatar">
            <div class="avatar-circle">
              <i class="fas fa-user"></i>
            </div>
            <div class="avatar-status" v-if="isOwnProfile">
              <i class="fas fa-crown"></i>
            </div>
          </div>
          <h1 class="hero-title">{{ displayName }}님의 프로필</h1>
          <p class="hero-subtitle" v-if="isOwnProfile">
            개인정보를 관리하고 금융 활동을 확인하세요
          </p>
          <p class="hero-subtitle" v-else>
            {{ username }}님의 공개 프로필입니다
          </p>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="content-wrapper" v-if="loaded">
        <!-- 프로필 카드 -->
        <div class="profile-cards">
          <!-- 기본 정보 카드 -->
          <div class="info-card basic-info">
            <div class="card-header">
              <div class="card-icon">
                <i class="fas fa-id-card"></i>
              </div>
              <h3 class="card-title">기본 정보</h3>
            </div>
            <div class="card-content">
              <div class="info-item">
                <div class="info-label">
                  <i class="fas fa-user"></i>
                  아이디
                </div>
                <div class="info-value">
                  <RouterLink :to="`/profile/${username}`" class="username-link">
                    {{ username }}
                  </RouterLink>
                </div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <i class="fas fa-envelope"></i>
                  이메일
                </div>
                <div class="info-value">
                  {{ profile.email || "미입력" }}
                </div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <i class="fas fa-calendar-alt"></i>
                  가입일
                </div>
                <div class="info-value">
                  {{ formatDate(profile.date_joined) }}
                </div>
              </div>
            </div>
          </div>

          <!-- 주소 정보 카드 -->
          <div class="info-card address-info">
            <div class="card-header">
              <div class="card-icon">
                <i class="fas fa-map-marker-alt"></i>
              </div>
              <h3 class="card-title">주소 정보</h3>
            </div>
            <div class="card-content">
              <div class="info-item">
                <div class="info-label">
                  <i class="fas fa-home"></i>
                  집 주소
                </div>
                <div class="info-value">
                  {{ profile.home_address || "미입력" }}
                </div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <i class="fas fa-building"></i>
                  회사 주소
                </div>
                <div class="info-value">
                  {{ profile.company_address || "미입력" }}
                </div>
              </div>
            </div>
          </div>

          <!-- 금융 정보 카드 (본인만 볼 수 있음) -->
          <div class="info-card financial-info" v-if="isOwnProfile">
            <div class="card-header">
              <div class="card-icon">
                <i class="fas fa-chart-line"></i>
              </div>
              <h3 class="card-title">금융 활동</h3>
            </div>
            <div class="card-content">
              <div class="financial-stats">
                <div class="stat-item">
                  <div class="stat-icon">
                    <i class="fas fa-bookmark"></i>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">12</div>
                    <div class="stat-label">저장한 영상</div>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon">
                    <i class="fas fa-comments"></i>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">8</div>
                    <div class="stat-label">작성한 글</div>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon">
                    <i class="fas fa-heart"></i>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">25</div>
                    <div class="stat-label">받은 좋아요</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 빠른 액션 카드 (본인만 볼 수 있음) -->
          <div class="info-card quick-actions" v-if="isOwnProfile">
            <div class="card-header">
              <div class="card-icon">
                <i class="fas fa-bolt"></i>
              </div>
              <h3 class="card-title">빠른 액션</h3>
            </div>
            <div class="card-content">
              <div class="action-buttons">
                <button class="action-btn primary" @click="goEdit">
                  <i class="fas fa-edit"></i>
                  <span>정보 수정</span>
                </button>
                <button class="action-btn secondary" @click="goToSavings">
                  <i class="fas fa-piggy-bank"></i>
                  <span>적금 상품</span>
                </button>
                <button class="action-btn tertiary" @click="goToCommunity">
                  <i class="fas fa-users"></i>
                  <span>커뮤니티</span>
                </button>
                <button class="action-btn quaternary" @click="goToVideos">
                  <i class="fas fa-video"></i>
                  <span>저장한 영상</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 최근 활동 (본인만 볼 수 있음) -->
        <div class="recent-activity" v-if="isOwnProfile">
          <h3 class="section-title">
            <i class="fas fa-clock"></i>
            최근 활동
          </h3>
          <div class="activity-list">
            <div class="activity-item">
              <div class="activity-icon">
                <i class="fas fa-comment"></i>
              </div>
              <div class="activity-content">
                <div class="activity-title">새로운 댓글을 작성했습니다</div>
                <div class="activity-description">"투자 전략에 대한 좋은 글이네요!"</div>
                <div class="activity-time">2시간 전</div>
              </div>
            </div>
            <div class="activity-item">
              <div class="activity-icon">
                <i class="fas fa-bookmark"></i>
              </div>
              <div class="activity-content">
                <div class="activity-title">영상을 저장했습니다</div>
                <div class="activity-description">"2024년 부동산 투자 전망"</div>
                <div class="activity-time">1일 전</div>
              </div>
            </div>
            <div class="activity-item">
              <div class="activity-icon">
                <i class="fas fa-heart"></i>
              </div>
              <div class="activity-content">
                <div class="activity-title">게시글에 좋아요를 받았습니다</div>
                <div class="activity-description">"초보자를 위한 주식 투자 가이드"</div>
                <div class="activity-time">3일 전</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 로딩 상태 -->
      <div v-else class="loading-section">
        <div class="loading-spinner"></div>
        <p class="loading-text">프로필을 불러오는 중...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter, useRoute, RouterLink } from "vue-router";
import { useUserStore } from "@/stores/user";
import axios from "axios";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

// 1) URL 파라미터로 넘어온 username (또는 undefined)
const username = route.params.username || userStore.username;

// 2) 프로필 정보를 담을 객체
const profile = ref({
  email: "",
  home_address: "",
  company_address: "",
  date_joined: "",
});
const loaded = ref(false);

// 3) 로그인한 본인의 프로필인지 여부
const isOwnProfile = computed(
  () => userStore.isLogin && userStore.username === username
);

// 4) 제목에 쓸 displayName
const displayName = computed(() => (isOwnProfile.value ? "내" : `${username}`));

// 5) 데이터 로드
onMounted(async () => {
  // 비로그인 상태로 "내 프로필" 접근 시 로그인 페이지로
  if (!userStore.isLogin && !route.params.username) {
    router.push("/login");
    return;
  }

  try {
    const res = await axios.get(`/api/accounts/profile/${username}/`);
    profile.value = res.data;
  } catch (err) {
    console.error("프로필 조회 실패", err);
    alert("프로필을 불러올 수 없습니다.");
    router.push("/");
  } finally {
    loaded.value = true;
  }
});

// 6) 수정 페이지로 이동
const goEdit = () => {
  router.push({ path: `/profile/edit`, query: { username } });
};

// 7) 빠른 액션 함수들
const goToSavings = () => {
  router.push("/saving");
};

const goToCommunity = () => {
  router.push("/community");
};

const goToVideos = () => {
  router.push("/youtube/later");
};

// 8) 날짜 포맷팅
const formatDate = (dateString) => {
  if (!dateString) return "미입력";
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR');
};
</script>

<style scoped>
.profile-page {
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

.profile-avatar {
  position: relative;
  display: inline-block;
  margin-bottom: 30px;
}

.avatar-circle {
  width: 120px;
  height: 120px;
  background: rgba(255,255,255,0.2);
  border: 4px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: white;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.avatar-status {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 35px;
  height: 35px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  border: 3px solid white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.9rem;
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.4);
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  margin-bottom: 15px;
  text-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.hero-subtitle {
  font-size: 1.1rem;
  color: rgba(255,255,255,0.9);
  margin-bottom: 40px;
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.content-wrapper {
  background: rgba(255,255,255,0.95);
  border-radius: 30px 30px 0 0;
  padding: 40px;
  margin-top: -20px;
  backdrop-filter: blur(10px);
}

.profile-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.info-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.info-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.basic-info::before {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.address-info::before {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.financial-info::before {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.quick-actions::before {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0,0,0,0.12);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f1f5f9;
}

.card-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  color: white;
}

.basic-info .card-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.address-info .card-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.financial-info .card-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.quick-actions .card-icon {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.card-content {
  flex: 1;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #f8fafc;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #64748b;
  font-size: 0.9rem;
}

.info-label i {
  width: 16px;
  color: #94a3b8;
}

.info-value {
  font-weight: 600;
  color: #333;
  text-align: right;
}

.username-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 700;
  transition: color 0.3s ease;
}

.username-link:hover {
  color: #5a67d8;
}

.financial-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: #f8fafc;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: #f1f5f9;
  transform: translateY(-2px);
}

.stat-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 800;
  color: #333;
  line-height: 1;
}

.stat-label {
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 2px;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px 15px;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.secondary {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.action-btn.tertiary {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.action-btn.quaternary {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.action-btn i {
  font-size: 1.2rem;
}

.action-btn span {
  font-size: 0.85rem;
}

.recent-activity {
  margin-top: 40px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title i {
  color: #667eea;
}

.activity-list {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 20px 0;
  border-bottom: 1px solid #f1f5f9;
}

.activity-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.activity-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.activity-description {
  color: #64748b;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.activity-time {
  color: #94a3b8;
  font-size: 0.8rem;
}

.loading-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: #64748b;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.2rem;
  }
  
  .avatar-circle {
    width: 100px;
    height: 100px;
    font-size: 2.5rem;
  }
  
  .content-wrapper {
    padding: 20px;
  }
  
  .profile-cards {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .financial-stats {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .activity-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .activity-icon {
    align-self: flex-start;
  }
}
</style>
