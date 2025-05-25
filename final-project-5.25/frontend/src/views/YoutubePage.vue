<template>
  <div class="youtube-page">
    <div class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">투자 동영상</h1>
          <p class="hero-subtitle">금융 전문가들의 투자 인사이트를 영상으로 만나보세요</p>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="content-wrapper">
        <!-- 탭 네비게이션 -->
        <div class="tab-navigation">
          <RouterLink
            class="tab-link"
            :class="{ active: currentTab === 'search' }"
            to="/youtube"
          >
            <div class="tab-icon">
              <i class="fas fa-search"></i>
            </div>
            <span class="tab-text">검색</span>
          </RouterLink>
          <RouterLink
            class="tab-link"
            :class="{ active: currentTab === 'later' }"
            to="/youtube/later"
          >
            <div class="tab-icon">
              <i class="fas fa-clock"></i>
            </div>
            <span class="tab-text">나중에 볼 영상</span>
          </RouterLink>
          <RouterLink
            class="tab-link"
            :class="{ active: currentTab === 'channel' }"
            to="/youtube/channel"
          >
            <div class="tab-icon">
              <i class="fas fa-tv"></i>
            </div>
            <span class="tab-text">채널</span>
          </RouterLink>
        </div>

        <!-- 탭 컨텐츠 영역 -->
        <div class="tab-content">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute, RouterLink, RouterView } from "vue-router";

const route = useRoute();
// 현재 탭을 경로로부터 계산
const currentTab = computed(() => {
  if (route.path.startsWith("/youtube/later")) return "later";
  if (route.path.startsWith("/youtube/channel")) return "channel";
  return "search";
});
</script>

<style scoped>
.youtube-page {
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
  text-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.hero-subtitle {
  font-size: 1.2rem;
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
  min-height: 600px;
}

.tab-navigation {
  display: flex;
  gap: 8px;
  margin-bottom: 40px;
  background: rgba(102, 126, 234, 0.1);
  padding: 8px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.tab-link {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px 24px;
  border-radius: 16px;
  text-decoration: none;
  color: #64748b;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.tab-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 16px;
}

.tab-link:hover::before {
  opacity: 0.1;
}

.tab-link.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
  transform: translateY(-2px);
}

.tab-link.active::before {
  opacity: 0;
}

.tab-icon {
  font-size: 1.2rem;
  position: relative;
  z-index: 1;
}

.tab-text {
  font-size: 1rem;
  position: relative;
  z-index: 1;
}

.tab-content {
  position: relative;
  z-index: 1;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .content-wrapper {
    padding: 20px;
  }
  
  .tab-navigation {
    flex-direction: column;
    gap: 4px;
  }
  
  .tab-link {
    justify-content: flex-start;
    padding: 12px 20px;
  }
  
  .tab-text {
    font-size: 0.9rem;
  }
}
</style>
