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
        @click="toggleVideoHandler"
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
        @click="toggleChannelHandler"
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

function toggleVideoHandler() {
  if (!video.value) return;
  const currentVideo = video.value;
  const videoData = {
    video_id: currentVideo.id,
    title: currentVideo.snippet.title,
    channel_title: currentVideo.snippet.channelTitle,
    thumbnail_url: currentVideo.snippet.thumbnails.medium.url, // 또는 high.url
    description: currentVideo.snippet.description,
    published_at: currentVideo.snippet.publishedAt,
    added_at: new Date().toISOString(),
  };
  youTube.toggleVideo(currentVideo.id, videoData);
}

function toggleChannelHandler() {
  if (!video.value) return;
  const currentVideoSnippet = video.value.snippet;
  const channelData = {
    channel_id: currentVideoSnippet.channelId,
    title: currentVideoSnippet.channelTitle,
    // 채널 썸네일은 이 API 응답에 없을 수 있으므로,
    // youtube.js 스토어에서 기본값을 사용하거나, ChannelView에서 나중에 로드합니다.
    // thumbnail_url: '기본값 또는 나중에 채워짐',
    added_at: new Date().toISOString(),
  };
  youTube.toggleChannel(currentVideoSnippet.channelId, channelData);
}
</script>
