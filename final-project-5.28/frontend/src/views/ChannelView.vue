<template>
  <div class="container mt-4">
    <h2>좋아하는 채널</h2>
    <div v-if="yt.savedChannels && yt.savedChannels.length">
      <div
        v-for="channelObj in yt.savedChannels"
        :key="channelObj.channel_id || channelObj"
        class="d-flex align-items-center mb-3"
      >
        <img
          :src="getChannelThumbnail(channelObj.channel_id || channelObj)"
          :alt="
            getChannelTitle(channelObj.channel_id || channelObj) ||
            '채널 썸네일'
          "
          class="me-3 rounded-circle"
          style="width: 50px; height: 50px; object-fit: cover"
          @error="handleImageError"
        />
        <div class="flex-grow-1">
          <p class="mb-0">
            {{ getChannelTitle(channelObj.channel_id || channelObj) }}
          </p>
        </div>
        <button
          class="btn btn-sm btn-outline-danger"
          @click="removeChannel(channelObj.channel_id || channelObj)"
        >
          삭제
        </button>
      </div>
    </div>
    <p v-else>저장된 채널이 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import axios from "axios";
import { useYouTubeStore } from "@/stores/youtube.js"; // .js 확장자 추가

const yt = useYouTubeStore();
const channelsDetails = ref({}); // 채널 ID를 키로, 채널 상세 정보를 값으로 저장

async function fetchChannelsDetails() {
  if (!yt.savedChannels || !yt.savedChannels.length) {
    channelsDetails.value = {};
    return;
  }

  const channelIdsToFetch = yt.savedChannels
    .map((channel) => channel.channel_id || channel) // 객체면 channel_id, 문자열이면 그대로 사용
    .filter((id) => id && !channelsDetails.value[id]); // 유효하고 아직 상세 정보가 없는 ID만

  if (!channelIdsToFetch.length) return;

  try {
    const response = await axios.get("/api/youtube/channels/", {
      params: { id: channelIdsToFetch.join(",") },
    });
    if (response.data && response.data.items) {
      response.data.items.forEach((item) => {
        channelsDetails.value[item.id] = item.snippet;
      });
    }
  } catch (error) {
    console.error("채널 상세 정보 로드 실패:", error);
  }
}

function getChannelThumbnail(channelId) {
  const details = channelsDetails.value[channelId];
  return details?.thumbnails?.default?.url || getDefaultChannelImage();
}

function getChannelTitle(channelId) {
  const details = channelsDetails.value[channelId];
  return details?.title || "채널 정보를 불러오는 중...";
}

function getDefaultChannelImage() {
  return "https://yt3.ggpht.com/a/default-user=s88-c-k-c0x00ffffff-no-rj";
}

function handleImageError(event) {
  event.target.src = getDefaultChannelImage();
}

async function removeChannel(channelId) {
  await yt.toggleChannel(channelId);
  // 삭제 후 channelsDetails에서 해당 채널 정보 제거 (선택적)
  // delete channelsDetails.value[channelId];
  // yt.savedChannels가 변경되면 watch가 감지하여 fetchChannelsDetails를 다시 호출하므로
  // 명시적으로 여기서 호출할 필요는 없을 수 있으나, 즉각적인 UI 반영을 위해 호출 가능
  // await fetchChannelsDetails(); // 필요에 따라 주석 해제
}

watch(
  () => yt.savedChannels,
  async (newSavedChannels, oldSavedChannels) => {
    // savedChannels 배열 자체가 변경되었거나, 내부 요소가 변경된 경우 모두 감지
    await fetchChannelsDetails();
  },
  { deep: true, immediate: true } // deep: true로 내부 객체 변경 감지, immediate: true로 초기 로드 시 실행
);

onMounted(async () => {
  // Pinia store의 초기화가 완료된 후 채널 정보를 가져오도록 보장
  if (yt.savedChannels.length > 0) {
    await fetchChannelsDetails();
  }
});
</script>
