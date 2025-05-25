<template>
  <div class="container mt-4">
    <h2>좋아하는 채널</h2>
    <div v-if="yt.savedChannels.length">
      <div
        v-for="id in yt.savedChannels"
        :key="id"
        class="d-flex align-items-center mb-3"
      >
        <img
          :src="channels[id]?.snippet.thumbnails.default.url || getDefaultChannelImage()"
          :alt="channels[id]?.snippet.title || '채널 썸네일'"
          class="me-3 rounded-circle"
          @error="handleImageError"
        />
        <div class="flex-grow-1">
          <p class="mb-0">{{ channels[id]?.snippet.title }}</p>
        </div>
        <button
          class="btn btn-sm btn-outline-danger"
          @click="yt.toggleChannel(id)"
        >
          삭제
        </button>
      </div>
    </div>
    <p v-else>저장된 채널이 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useYouTubeStore } from "@/stores/youtube";

const yt = useYouTubeStore();
const channels = ref({});

async function loadChannels() {
  if (!yt.savedChannels.length) return;
  const res = await axios.get("/api/youtube/channels/", {
    params: { id: yt.savedChannels.join(",") },
  });
  res.data.items.forEach((item) => {
    channels.value[item.id] = item;
  });
}

function getDefaultChannelImage() {
  // 유튜브 기본 채널 이미지
  return 'https://yt3.ggpht.com/a/default-user=s88-c-k-c0x00ffffff-no-rj';
}

function handleImageError(event) {
  // 이미지 로드 실패 시 유튜브 기본 채널 이미지로 교체
  event.target.src = getDefaultChannelImage();
}

function getYoutubeChannelThumbnail(channelId) {
  // 유튜브 채널 ID로부터 썸네일 URL 생성 (실제로는 API에서 가져와야 함)
  if (!channelId) return getDefaultChannelImage();
  // 채널 썸네일은 API를 통해서만 정확히 가져올 수 있으므로 기본 이미지 사용
  return getDefaultChannelImage();
}

onMounted(loadChannels);
</script>
