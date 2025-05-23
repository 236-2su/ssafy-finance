<template>
  <div class="container mt-5" v-if="loaded">
    <h2 class="mb-4">{{ displayName }}님의 정보</h2>

    <div class="card p-4 shadow-sm">
      <!-- 기본 정보 -->
      <h5 class="mb-3">기본 정보</h5>
      <ul class="list-group list-group-flush mb-4">
        <li class="list-group-item">
          <strong>아이디:</strong>
          <!-- 프로필 페이지 내에서 클릭 가능한 링크 -->
          <RouterLink :to="`/profile/${username}`">{{ username }}</RouterLink>
        </li>
        <li class="list-group-item">
          <strong>이메일:</strong> {{ profile.email || "미입력" }}
        </li>
      </ul>

      <!-- 선택 정보 -->
      <h5 class="mb-3">추가 정보</h5>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">
          <strong>집 주소:</strong> {{ profile.home_address || "미입력" }}
        </li>
        <li class="list-group-item">
          <strong>회사 주소:</strong> {{ profile.company_address || "미입력" }}
        </li>
      </ul>

      <!-- 본인 프로필일 때만 수정 버튼 보이기 -->
      <div class="text-end mt-4" v-if="isOwnProfile">
        <button class="btn btn-outline-primary" @click="goEdit">
          정보 수정
        </button>
      </div>
    </div>
  </div>

  <div v-else class="text-center my-5">로딩 중…</div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter, useRoute, RouterLink } from "vue-router";
import { useUserStore } from "@/stores/user";
import axios from "axios";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

// 1) URL 파라미터로 넘어온 username (또는 undefined)
const username = route.params.username || userStore.username;

// 2) 프로필 정보를 담을 객체
const profile = ref({
  email: "",
  home_address: "",
  company_address: "",
});
const loaded = ref(false);

// 3) 로그인한 본인의 프로필인지 여부
const isOwnProfile = computed(
  () => userStore.isLogin && userStore.username === username
);

// 4) 제목에 쓸 displayName
const displayName = computed(() => (isOwnProfile.value ? "내" : `${username}`));

// 5) 데이터 로드
onMounted(async () => {
  // 비로그인 상태로 “내 프로필” 접근 시 로그인 페이지로
  if (!userStore.isLogin && !route.params.username) {
    router.push("/login");
    return;
  }

  try {
    const res = await axios.get(`/api/accounts/profile/${username}/`);
    profile.value = res.data;
  } catch (err) {
    console.error("프로필 조회 실패", err);
    alert("프로필을 불러올 수 없습니다.");
    router.push("/");
  } finally {
    loaded.value = true;
  }
});

// 6) 수정 페이지로 이동
const goEdit = () => {
  router.push({ path: `/profile/edit`, query: { username } });
};
</script>
