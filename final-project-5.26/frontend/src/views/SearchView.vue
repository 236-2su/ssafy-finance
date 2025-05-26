<template>
  <div class="search-view">
    <!-- 검색 섹션 -->
    <div class="search-section">
      <div class="search-container">
        <div class="search-input-wrapper">
          <div class="search-icon">
            <i class="fas fa-search"></i>
          </div>
          <input
            v-model="keyword"
            @keyup.enter="searchVideos"
            placeholder="투자, 주식, 부동산 등 관심 주제를 검색해보세요"
            class="search-input"
          />
          <button class="search-btn" @click="searchVideos">
            <i class="fas fa-arrow-right"></i>
          </button>
        </div>
      </div>
      
      <!-- 인기 검색어 -->
      <div class="popular-keywords">
        <span class="popular-label">인기 검색어:</span>
        <div class="keyword-tags">
          <button 
            v-for="tag in popularKeywords" 
            :key="tag"
            @click="searchWithKeyword(tag)"
            class="keyword-tag"
          >
            {{ tag }}
          </button>
        </div>
      </div>
    </div>

    <!-- 검색 결과 -->
    <div v-if="loading" class="loading-section">
      <div class="loading-spinner"></div>
      <p class="loading-text">동영상을 검색하는 중...</p>
    </div>

    <div v-else-if="videos.length" class="results-section">
      <div class="results-header">
        <h3 class="results-title">
          <i class="fas fa-play-circle"></i>
          검색 결과 ({{ videos.length }}개)
        </h3>
        <div class="view-toggle">
          <button 
            @click="viewMode = 'grid'" 
            :class="{ active: viewMode === 'grid' }"
            class="view-btn"
          >
            <i class="fas fa-th"></i>
          </button>
          <button 
            @click="viewMode = 'list'" 
            :class="{ active: viewMode === 'list' }"
            class="view-btn"
          >
            <i class="fas fa-list"></i>
          </button>
        </div>
      </div>

      <div class="videos-container" :class="viewMode">
        <div
          v-for="video in videos"
          :key="video.id.videoId"
          class="video-card"
          @click="goDetail(video.id.videoId)"
        >
          <div class="video-thumbnail">
            <img
              :src="video.snippet.thumbnails.medium.url"
              :alt="video.snippet.title"
              class="thumbnail-img"
            />
            <div class="play-overlay">
              <i class="fas fa-play"></i>
            </div>
            <div class="video-duration">
              {{ formatDuration(video.contentDetails?.duration) }}
            </div>
          </div>
          
          <div class="video-info">
            <h4 class="video-title">{{ video.snippet.title }}</h4>
            <p class="video-channel">{{ video.snippet.channelTitle }}</p>
            <p class="video-description">{{ truncateText(video.snippet.description, 100) }}</p>
            <div class="video-meta">
              <span class="video-date">
                <i class="fas fa-calendar"></i>
                {{ formatDate(video.snippet.publishedAt) }}
              </span>
              <span class="video-views" v-if="video.statistics?.viewCount">
                <i class="fas fa-eye"></i>
                {{ formatViews(video.statistics.viewCount) }}
              </span>
            </div>
          </div>

          <div class="video-actions">
            <button
              class="action-btn save-btn"
              :class="{ saved: youTube.isVideoSaved(video.id.videoId) }"
              @click.stop="saveVideo(video)"
            >
              <i :class="youTube.isVideoSaved(video.id.videoId) ? 'fas fa-bookmark' : 'far fa-bookmark'"></i>
              {{ youTube.isVideoSaved(video.id.videoId) ? "저장됨" : "나중에 보기" }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="searched" class="empty-section">
      <div class="empty-icon">
        <i class="fas fa-search fa-4x"></i>
      </div>
      <h3 class="empty-title">검색 결과가 없습니다</h3>
      <p class="empty-description">
        다른 키워드로 검색해보시거나<br>
        인기 검색어를 이용해보세요
      </p>
      <button @click="clearSearch" class="clear-btn">
        새로 검색하기
      </button>
    </div>

    <div v-else class="welcome-section">
      <div class="welcome-content">
        <div class="welcome-icon">
          <i class="fas fa-video fa-4x"></i>
        </div>
        <h3 class="welcome-title">투자 동영상 검색</h3>
        <p class="welcome-description">
          전문가들의 투자 인사이트와 시장 분석을<br>
          동영상으로 만나보세요
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useYouTubeStore } from "@/stores/youtube";

const router = useRouter();
const youTube = useYouTubeStore();
const keyword = ref("");
const videos = ref([]);
const loading = ref(false);
const searched = ref(false);
const viewMode = ref('grid');

const popularKeywords = [
  "주식 투자", "부동산", "코인", "경제 전망", "금리", "인플레이션", "ETF", "배당주"
];

async function searchVideos() {
  if (!keyword.value.trim()) return;
  
  loading.value = true;
  searched.value = true;
  
  try {
    const res = await axios.get("/api/youtube/search/", {
      params: { q: keyword.value, maxResults: 15 },
    });
    videos.value = res.data.items || [];
  } catch (error) {
    console.error("검색 오류:", error);
    videos.value = [];
  } finally {
    loading.value = false;
  }
}

function searchWithKeyword(tag) {
  keyword.value = tag;
  searchVideos();
}

function goDetail(id) {
  router.push({ name: "VideoDetail", params: { id } });
}

function clearSearch() {
  keyword.value = "";
  videos.value = [];
  searched.value = false;
}

function truncateText(text, maxLength) {
  if (!text) return "";
  return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR');
}

function formatViews(viewCount) {
  const count = parseInt(viewCount);
  if (count >= 1000000) {
    return Math.floor(count / 1000000) + "M";
  } else if (count >= 1000) {
    return Math.floor(count / 1000) + "K";
  }
  return count.toString();
}

function formatDuration(duration) {
  if (!duration) return "";
  // ISO 8601 duration format parsing would go here
  return ""; // Simplified for now
}

function saveVideo(video) {
  const videoData = {
    video_id: video.id.videoId,
    title: video.snippet.title,
    channel_title: video.snippet.channelTitle,
    thumbnail_url: video.snippet.thumbnails.medium.url,
    description: video.snippet.description,
    published_at: video.snippet.publishedAt,
    added_at: new Date().toISOString()
  };
  
  youTube.toggleVideo(video.id.videoId, videoData);
}
</script>

<style scoped>
.search-view {
  padding: 0;
}

.search-section {
  margin-bottom: 40px;
}

.search-container {
  margin-bottom: 20px;
}

.search-input-wrapper {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
  background: white;
  border-radius: 50px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.search-input-wrapper:focus-within {
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
  transform: translateY(-2px);
}

.search-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 1.1rem;
  z-index: 2;
}

.search-input {
  width: 100%;
  padding: 18px 70px 18px 55px;
  border: none;
  outline: none;
  font-size: 1rem;
  background: transparent;
  color: #333;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-btn:hover {
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.popular-keywords {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
}

.popular-label {
  color: #64748b;
  font-weight: 600;
  font-size: 0.9rem;
}

.keyword-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.keyword-tag {
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  color: #667eea;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.keyword-tag:hover {
  background: #667eea;
  color: white;
  transform: translateY(-1px);
}

.loading-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: #64748b;
  font-size: 1.1rem;
}

.results-section {
  margin-top: 40px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f1f5f9;
}

.results-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  display: flex;
  align-items: center;
  gap: 10px;
}

.results-title i {
  color: #667eea;
}

.view-toggle {
  display: flex;
  gap: 4px;
  background: #f8fafc;
  padding: 4px;
  border-radius: 10px;
}

.view-btn {
  background: transparent;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn.active {
  background: white;
  color: #667eea;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.videos-container.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.videos-container.list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.video-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.videos-container.grid .video-card {
  display: flex;
  flex-direction: column;
}

.videos-container.list .video-card {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}

.video-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}

.video-thumbnail {
  position: relative;
  overflow: hidden;
}

.videos-container.grid .video-thumbnail {
  width: 100%;
  height: 200px;
}

.videos-container.list .video-thumbnail {
  width: 200px;
  height: 120px;
  flex-shrink: 0;
}

.thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.video-card:hover .thumbnail-img {
  transform: scale(1.05);
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0,0,0,0.7);
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.video-card:hover .play-overlay {
  opacity: 1;
}

.video-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0,0,0,0.8);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.video-info {
  padding: 20px;
  flex: 1;
}

.videos-container.list .video-info {
  padding: 15px 20px;
}

.video-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-channel {
  color: #667eea;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.video-description {
  color: #64748b;
  font-size: 0.85rem;
  line-height: 1.5;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.videos-container.list .video-description {
  -webkit-line-clamp: 3;
}

.video-meta {
  display: flex;
  gap: 15px;
  font-size: 0.8rem;
  color: #94a3b8;
}

.video-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.video-actions {
  padding: 0 20px 20px;
}

.videos-container.list .video-actions {
  padding: 15px 20px;
  align-self: flex-start;
}

.action-btn {
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  color: #667eea;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.action-btn:hover {
  background: #667eea;
  color: white;
  transform: translateY(-1px);
}

.action-btn.saved {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

.empty-section,
.welcome-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.empty-icon,
.welcome-icon {
  color: #cbd5e1;
  margin-bottom: 30px;
}

.empty-title,
.welcome-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #64748b;
  margin-bottom: 15px;
}

.empty-description,
.welcome-description {
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.clear-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

@media (max-width: 768px) {
  .search-input-wrapper {
    margin: 0 20px;
  }
  
  .popular-keywords {
    flex-direction: column;
    gap: 10px;
  }
  
  .results-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .videos-container.grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .videos-container.list .video-card {
    flex-direction: column;
  }
  
  .videos-container.list .video-thumbnail {
    width: 100%;
    height: 200px;
  }
}
</style>
