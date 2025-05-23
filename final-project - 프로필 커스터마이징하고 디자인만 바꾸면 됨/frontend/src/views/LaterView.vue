<template>
  <div class="container mt-4">
    <h2>나중에 볼 동영상</h2>
    <div v-if="yt.savedVideos.length" class="row">
      <div v-for="id in yt.savedVideos" :key="id" class="col-md-4 mb-4">
        <div class="card h-100">
          <img
            :src="getThumb(id)"
            class="card-img-top"
            @click="goDetail(id)"
            style="cursor: pointer"
          />
          <div class="card-body d-flex flex-column">
            <h6 class="card-title">{{ getTitle(id) }}</h6>
            <button
              class="mt-auto btn btn-sm btn-outline-danger"
              @click="yt.toggleVideo(id)"
            >
              삭제
            </button>
          </div>
        </div>
      </div>
    </div>
    <p v-else class="text-center">저장된 동영상이 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useYouTubeStore } from "@/stores/youtube";

const router = useRouter();
const yt = useYouTubeStore();

// 상세 정보를 캐싱
const details = ref({});

async function loadDetails() {
  if (!yt.savedVideos.length) return;
  try {
    const res = await axios.get("/api/youtube/videos/", {
      params: { id: yt.savedVideos.join(",") },
    });
    res.data.items.forEach((item) => {
      details.value[item.id] = item;
    });
  } catch (err) {
    console.error("동영상 정보 로드 실패", err);
  }
}

function getThumb(id) {
  return details.value[id]?.snippet.thumbnails.medium.url || "";
}
function getTitle(id) {
  return details.value[id]?.snippet.title || "로딩 중...";
}

function goDetail(id) {
  router.push({ name: "VideoDetail", params: { id } });
}

onMounted(loadDetails);
</script>

<style scoped>
.container {
  max-width: 800px;
}
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.card {
  cursor: pointer;
  width: 100%;
}
</style>
