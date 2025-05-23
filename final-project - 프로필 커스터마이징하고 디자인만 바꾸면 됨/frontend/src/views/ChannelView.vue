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
          :src="channels[id]?.snippet.thumbnails.default.url"
          alt="썸네일"
          class="me-3 rounded-circle"
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

onMounted(loadChannels);
</script>
