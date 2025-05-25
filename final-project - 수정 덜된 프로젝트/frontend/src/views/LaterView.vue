<template>
  <div class="later-view">
    <div class="header-section">
      <h2 class="page-title">
        <i class="fas fa-clock"></i>
        나중에 볼 동영상
      </h2>
      <p class="page-subtitle">저장한 동영상을 모아서 확인하세요</p>
    </div>

    <div v-if="yt.savedVideos.length" class="videos-section">
      <div class="videos-grid">
        <div 
          v-for="video in yt.savedVideos" 
          :key="video.video_id" 
          class="video-card"
        >
          <div class="video-thumbnail" @click="goDetail(video.video_id)">
            <img
              :src="video.thumbnail_url"
              :alt="video.title"
              class="thumbnail-img"
            />
            <div class="play-overlay">
              <i class="fas fa-play"></i>
            </div>
          </div>
          
          <div class="video-info">
            <h4 class="video-title" @click="goDetail(video.video_id)">
              {{ video.title }}
            </h4>
            <p class="video-channel">{{ video.channel_title }}</p>
            <div class="video-meta">
              <span class="added-date">
                <i class="fas fa-calendar-plus"></i>
                {{ formatDate(video.added_at) }}
              </span>
            </div>
          </div>

          <div class="video-actions">
            <button
              class="action-btn watch-btn"
              @click="goDetail(video.video_id)"
            >
              <i class="fas fa-play"></i>
              시청하기
            </button>
            <button
              class="action-btn remove-btn"
              @click="removeVideo(video.video_id)"
            >
              <i class="fas fa-trash"></i>
              삭제
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="empty-section">
      <div class="empty-icon">
        <i class="fas fa-clock fa-4x"></i>
      </div>
      <h3 class="empty-title">저장된 동영상이 없습니다</h3>
      <p class="empty-description">
        관심있는 동영상을 검색해서<br>
        나중에 볼 영상으로 저장해보세요
      </p>
      <button @click="goToSearch" class="search-btn">
        <i class="fas fa-search"></i>
        동영상 검색하기
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useYouTubeStore } from "@/stores/youtube";

const router = useRouter();
const yt = useYouTubeStore();

function goDetail(videoId) {
  router.push({ name: "VideoDetail", params: { id: videoId } });
}

function removeVideo(videoId) {
  yt.toggleVideo(videoId);
}

function goToSearch() {
  router.push({ name: "SearchView" });
}

function formatDate(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays === 1) {
    return "오늘";
  } else if (diffDays === 2) {
    return "어제";
  } else if (diffDays <= 7) {
    return `${diffDays - 1}일 전`;
  } else {
    return date.toLocaleDateString('ko-KR');
  }
}

onMounted(() => {
  yt.initialize();
});
</script>

<style scoped>
.later-view {
  padding: 0;
}

.header-section {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #333;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.page-title i {
  color: #667eea;
}

.page-subtitle {
  color: #64748b;
  font-size: 1.1rem;
  margin: 0;
}

.videos-section {
  margin-top: 40px;
}

.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.video-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.video-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}

.video-thumbnail {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  cursor: pointer;
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

.video-info {
  padding: 20px;
  flex: 1;
}

.video-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.4;
  cursor: pointer;
  transition: color 0.3s ease;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-title:hover {
  color: #667eea;
}

.video-channel {
  color: #667eea;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 12px;
}

.video-meta {
  display: flex;
  gap: 15px;
  font-size: 0.8rem;
  color: #94a3b8;
}

.added-date {
  display: flex;
  align-items: center;
  gap: 4px;
}

.video-actions {
  padding: 0 20px 20px;
  display: flex;
  gap: 10px;
}

.action-btn {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.watch-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.watch-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.remove-btn {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.remove-btn:hover {
  background: #ef4444;
  color: white;
  transform: translateY(-1px);
}

.empty-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.empty-icon {
  color: #cbd5e1;
  margin-bottom: 30px;
}

.empty-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #64748b;
  margin-bottom: 15px;
}

.empty-description {
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.search-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
    flex-direction: column;
    gap: 10px;
  }
  
  .videos-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .video-actions {
    flex-direction: column;
  }
}
</style>
