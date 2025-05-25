<template>
  <div class="container mt-4" v-if="video">
    <h3>{{ video.snippet.title }}</h3>

    <!-- 저장/삭제 버튼 -->
    <div class="mb-3">
      <button
        class="btn"
        :class="
          youTube.isVideoSaved(video.id) ? 'btn-danger' : 'btn-outline-danger'
        "
        @click="youTube.toggleVideo(video.id)"
      >
        {{
          youTube.isVideoSaved(video.id) ? "나중에 보기 취소" : "나중에 보기"
        }}
      </button>

      <button
        class="btn ms-2"
        :class="
          youTube.isChannelSaved(video.snippet.channelId)
            ? 'btn-success'
            : 'btn-outline-success'
        "
        @click="youTube.toggleChannel(video.snippet.channelId)"
      >
        {{
          youTube.isChannelSaved(video.snippet.channelId)
            ? "채널 삭제"
            : "채널 저장"
        }}
      </button>
    </div>

    <!-- 영상 임베드 -->
    <div class="ratio ratio-16x9 mb-3">
      <iframe
        :src="`https://www.youtube-nocookie.com/embed/${video.id}`"
        allowfullscreen
      ></iframe>
    </div>

    <p>{{ video.snippet.description }}</p>
    <ul class="list-inline">
      <li class="list-inline-item">조회: {{ video.statistics.viewCount }}</li>
      <li class="list-inline-item">좋아요: {{ video.statistics.likeCount }}</li>
      <li class="list-inline-item">
        댓글: {{ video.statistics.commentCount }}
      </li>
    </ul>
  </div>
  <div v-else class="text-center my-5">로딩중...</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { useYouTubeStore } from "@/stores/youtube";

const route = useRoute();
const youTube = useYouTubeStore();
const videoId = route.params.id;
const video = ref(null);

async function fetchDetail() {
  const res = await axios.get("/api/youtube/videos/", {
    params: { id: videoId },
  });
  video.value = res.data.items?.[0] || null;
}

onMounted(fetchDetail);
</script>
