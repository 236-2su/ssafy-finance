<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
      <div class="container">
        <!-- 로고 -->
        <RouterLink class="navbar-brand d-flex align-items-center" to="/">
          <div class="logo-container me-2">
            <svg width="32" height="32" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="blueGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#00BFFF;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#0080FF;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="greenGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#7FFF00;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#32CD32;stop-opacity:1" />
                </linearGradient>
              </defs>
              <ellipse cx="35" cy="50" rx="25" ry="15" fill="none" stroke="url(#blueGradient)" stroke-width="8" transform="rotate(-45 35 50)"/>
              <ellipse cx="65" cy="50" rx="25" ry="15" fill="none" stroke="url(#greenGradient)" stroke-width="8" transform="rotate(45 65 50)"/>
            </svg>
          </div>
          <span class="fw-bold">MyFin</span>
        </RouterLink>

        <!-- 메뉴 (큰 화면 전용) -->
        <ul class="navbar-nav mx-auto d-none d-lg-flex">
          <li class="nav-item">
            <RouterLink class="nav-link fw-medium" to="/">Home</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link fw-medium" to="/news">News</RouterLink>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle fw-medium" href="#" id="servicesDropdown" role="button" data-bs-toggle="dropdown">
              Services
            </a>
            <ul class="dropdown-menu">
              <li><RouterLink class="dropdown-item" to="/saving">Deposit/Savings Rates</RouterLink></li>
              <li><RouterLink class="dropdown-item" to="/metal">Stock & Commodity Prices</RouterLink></li>
              <li><RouterLink class="dropdown-item" to="/youtube">Investment Videos</RouterLink></li>
              <li><RouterLink class="dropdown-item" to="/bank">Find Banks</RouterLink></li>
            </ul>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link fw-medium" to="/community">Community</RouterLink>
          </li>
        </ul>

        <!-- 로그인/로그아웃 (큰 화면 전용) -->
        <div class="d-none d-lg-flex align-items-center">
          <template v-if="userStore.isLogin">
            <RouterLink to="/profile" class="fw-bold text-dark me-3">{{
              userStore.username
            }}</RouterLink>
            <button class="btn btn-outline-danger btn-sm" @click="logout">
              Log Out
            </button>
          </template>
          <template v-else>
            <RouterLink class="btn btn-outline-primary btn-sm me-2" to="/login"
              >Log In</RouterLink
            >
            <RouterLink class="btn btn-primary btn-sm" to="/signup"
              >Sign Up</RouterLink
            >
          </template>
        </div>

        <!-- 햄버거 버튼 (작은 화면 전용) -->
        <button class="navbar-toggler d-lg-none" type="button" @click="toggleMenu">
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
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
              Log Out
            </button>
          </div>
        </template>
        <template v-else>
          <RouterLink class="btn btn-outline-primary mb-2" to="/login"
            >Log In</RouterLink
          >
          <RouterLink class="btn btn-primary mb-3" to="/signup"
            >Sign Up</RouterLink
          >
        </template>

        <!-- 메뉴 항목 -->
        <RouterLink class="menu-item" to="/">Home</RouterLink>
        <RouterLink class="menu-item" to="/news">News</RouterLink>
        <RouterLink class="menu-item" to="/saving">Deposit/Savings Rates</RouterLink>
        <RouterLink class="menu-item" to="/metal">Stock & Commodity Prices</RouterLink>
        <RouterLink class="menu-item" to="/youtube">Investment Videos</RouterLink>
        <RouterLink class="menu-item" to="/bank">Find Banks</RouterLink>
        <RouterLink class="menu-item" to="/community">Community</RouterLink>
      </div>
    </div>

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
.navbar {
  border-bottom: 1px solid #e9ecef;
}

.navbar-brand {
  font-size: 1.25rem;
}

.nav-link {
  color: #495057 !important;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #007bff !important;
}

.dropdown-menu {
  border: none;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.dropdown-item {
  padding: 0.5rem 1rem;
  transition: background-color 0.3s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  color: #007bff;
}

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
  transition: color 0.3s ease;
}

.menu-item:hover {
  color: #0d6efd;
}
</style>
