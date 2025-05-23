<template>
  <div class="container mt-4">
    <!-- 상단 탭 네비게이션 -->
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <RouterLink
          class="nav-link"
          :class="{ active: currentTab === 'search' }"
          to="/youtube"
        >
          검색
        </RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink
          class="nav-link"
          :class="{ active: currentTab === 'later' }"
          to="/youtube/later"
        >
          나중에 볼 영상
        </RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink
          class="nav-link"
          :class="{ active: currentTab === 'channel' }"
          to="/youtube/channel"
        >
          채널
        </RouterLink>
      </li>
    </ul>

    <!-- 탭 컨텐츠 영역 -->
    <div class="mt-3">
      <RouterView />
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
.container {
  max-width: 800px;
}
</style>
