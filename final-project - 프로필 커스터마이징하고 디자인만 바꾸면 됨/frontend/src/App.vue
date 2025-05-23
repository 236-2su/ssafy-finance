<template>
  <div>
    <nav class="navbar navbar-light bg-light px-4 justify-content-between">
      <!-- 로고 -->
      <RouterLink class="navbar-brand d-flex align-items-center" to="/">
        <img src="@/assets/logo.svg" alt="Logo" width="40" height="40" />
        <span class="ms-2">금융비교앱</span>
      </RouterLink>

      <!-- 메뉴 (큰 화면 전용) -->
      <ul class="nav d-none d-lg-flex align-items-center">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/saving"
            >예금/적금 금리비교</RouterLink
          >
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/metal"
            >현물 상품 가격확인</RouterLink
          >
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/youtube"
            >관심 종목 영상 검색</RouterLink
          >
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/bank">근처 은행 검색</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/community">커뮤니티</RouterLink>
        </li>
      </ul>

      <!-- 로그인/로그아웃 (큰 화면 전용) -->
      <div class="d-none d-lg-flex align-items-center">
        <template v-if="userStore.isLogin">
          <RouterLink to="/profile" class="fw-bold text-dark me-3">{{
            userStore.username
          }}</RouterLink>
          <button class="btn btn-outline-danger btn-sm" @click="logout">
            로그아웃
          </button>
        </template>
        <template v-else>
          <RouterLink class="btn btn-outline-primary btn-sm me-2" to="/login"
            >로그인</RouterLink
          >
          <RouterLink class="btn btn-primary btn-sm" to="/signup"
            >회원가입</RouterLink
          >
        </template>
      </div>

      <!-- 햄버거 버튼 (작은 화면 전용) -->
      <button class="btn btn-outline-dark d-lg-none" @click="toggleMenu">
        ☰
      </button>
    </nav>

    <!-- 모바일 전용 드롭다운 메뉴 -->
    <div class="offcanvas-menu d-lg-none" v-if="showMenu">
      <div class="d-flex flex-column align-items-start">
        <template v-if="userStore.isLogin">
          <div
            class="d-flex align-items-center justify-content-between w-100 mb-3"
          >
            <RouterLink to="/profile" class="fw-bold text-dark me-2">
              {{ userStore.username }}
            </RouterLink>
            <button class="btn btn-outline-danger btn-sm" @click="logout">
              로그아웃
            </button>
          </div>
        </template>
        <template v-else>
          <RouterLink class="btn btn-outline-primary mb-2" to="/login"
            >로그인</RouterLink
          >
          <RouterLink class="btn btn-primary mb-3" to="/signup"
            >회원가입</RouterLink
          >
        </template>

        <!-- 메뉴 항목 -->
        <RouterLink class="menu-item" to="/saving"
          >예금/적금 금리비교</RouterLink
        >
        <RouterLink class="menu-item" to="/metal"
          >현물 상품 가격확인</RouterLink
        >
        <RouterLink class="menu-item" to="/youtube"
          >관심 종목 영상 검색</RouterLink
        >
        <RouterLink class="menu-item" to="/bank">근처 은행 검색</RouterLink>
        <RouterLink class="menu-item" to="/community">커뮤니티</RouterLink>
      </div>
    </div>

    <div style="height: 4px; background-color: #28a745"></div>
    <RouterView />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink, RouterView, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import axios from "axios";

const router = useRouter();
const userStore = useUserStore();
const showMenu = ref(false);

const toggleMenu = () => {
  showMenu.value = !showMenu.value;
};

const logout = async () => {
  try {
    await axios.post("/api/accounts/logout/");
    userStore.logout();
    router.push("/");
    showMenu.value = false;
  } catch (err) {
    console.error("로그아웃 실패:", err);
  }
};
</script>

<style scoped>
.offcanvas-menu {
  position: fixed;
  top: 60px;
  right: 0;
  width: max-content;
  padding: 1rem;
  background-color: #fff;
  border-left: 1px solid #ddd;
  box-shadow: -2px 0 6px rgba(0, 0, 0, 0.1);
  z-index: 1050;
  white-space: nowrap;
}
.menu-item {
  display: block;
  padding: 6px 0;
  color: #212529;
  text-decoration: none;
  text-align: left;
  font-weight: 500;
}
.menu-item:hover {
  color: #0d6efd;
}
</style>
