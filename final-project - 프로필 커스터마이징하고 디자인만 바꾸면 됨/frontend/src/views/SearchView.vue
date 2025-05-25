<template>
  <div class="container mt-4">
    <!-- 검색 폼 (변경 없음) -->
    <div class="input-group mb-3">
      <input
        v-model="keyword"
        @keyup.enter="searchVideos"
        placeholder="검색어 입력"
        class="form-control"
      />
      <button class="btn btn-primary" @click="searchVideos">검색</button>
    </div>

    <!-- 결과 리스트 -->
    <div v-if="videos.length" class="row">
      <div
        v-for="video in videos"
        :key="video.id.videoId"
        class="col-md-4 mb-4"
      >
        <div class="card h-100">
          <img
            :src="video.snippet.thumbnails.medium.url"
            class="card-img-top"
            alt="thumbnail"
            @click="goDetail(video.id.videoId)"
            style="cursor: pointer"
          />
          <div class="card-body d-flex flex-column">
            <h6 class="card-title">{{ video.snippet.title }}</h6>
            <button
              class="mt-auto btn btn-sm"
              :class="
                youTube.isVideoSaved(video.id.videoId)
                  ? 'btn-outline-danger'
                  : 'btn-outline-success'
              "
              @click="youTube.toggleVideo(video.id.videoId)"
            >
              {{
                youTube.isVideoSaved(video.id.videoId) ? "삭제" : "나중에 보기"
              }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <p v-else class="text-center">검색 결과가 없습니다.</p>
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

async function searchVideos() {
  if (!keyword.value.trim()) return;
  const res = await axios.get("/api/youtube/search/", {
    params: { q: keyword.value, maxResults: 15 },
  });
  videos.value = res.data.items || [];
}

function goDetail(id) {
  router.push({ name: "VideoDetail", params: { id } });
}
</script>

<style scoped>
.card {
  cursor: default;
}
.card-body {
  display: flex;
  flex-direction: column;
}
</style>
