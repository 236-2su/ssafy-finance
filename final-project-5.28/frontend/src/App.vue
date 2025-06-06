<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
      <div class="container">
        <!-- 로고 -->
        <RouterLink class="navbar-brand d-flex align-items-center" to="/">
          <div class="logo-container me-2">
            <svg
              width="32"
              height="32"
              viewBox="0 0 100 100"
              xmlns="http://www.w3.org/2000/svg"
            >
              <defs>
                <linearGradient
                  id="blueGradient"
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="100%"
                >
                  <stop
                    offset="0%"
                    style="stop-color: #00bfff; stop-opacity: 1"
                  />
                  <stop
                    offset="100%"
                    style="stop-color: #0080ff; stop-opacity: 1"
                  />
                </linearGradient>
                <linearGradient
                  id="greenGradient"
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="100%"
                >
                  <stop
                    offset="0%"
                    style="stop-color: #7fff00; stop-opacity: 1"
                  />
                  <stop
                    offset="100%"
                    style="stop-color: #32cd32; stop-opacity: 1"
                  />
                </linearGradient>
              </defs>
              <ellipse
                cx="35"
                cy="50"
                rx="25"
                ry="15"
                fill="none"
                stroke="url(#blueGradient)"
                stroke-width="8"
                transform="rotate(-45 35 50)"
              />
              <ellipse
                cx="65"
                cy="50"
                rx="25"
                ry="15"
                fill="none"
                stroke="url(#greenGradient)"
                stroke-width="8"
                transform="rotate(45 65 50)"
              />
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
            <a
              class="nav-link dropdown-toggle fw-medium"
              href="#"
              id="servicesDropdown"
              role="button"
              data-bs-toggle="dropdown"
            >
              Services
            </a>
            <ul class="dropdown-menu">
              <li>
                <RouterLink class="dropdown-item" to="/saving"
                  >Deposit/Savings Rates</RouterLink
                >
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/metal"
                  >Stock & Commodity Prices</RouterLink
                >
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/youtube"
                  >Investment Videos</RouterLink
                >
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/bank"
                  >Find Banks</RouterLink
                >
              </li>
              <li>
                <RouterLink class="dropdown-item" to="/recommendations"
                  >AI 금융 추천</RouterLink
                >
              </li>
            </ul>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link fw-medium" to="/community"
              >Community</RouterLink
            >
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
        <button
          class="navbar-toggler d-lg-none"
          type="button"
          @click="toggleMenu"
        >
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
            <RouterLink
              to="/profile"
              class="fw-bold text-dark me-2"
              @click="closeMenu"
            >
              {{ userStore.username }}
            </RouterLink>
            <button class="btn btn-outline-danger btn-sm" @click="logout">
              Log Out
            </button>
          </div>
        </template>
        <template v-else>
          <RouterLink
            class="btn btn-outline-primary mb-2"
            to="/login"
            @click="closeMenu"
            >Log In</RouterLink
          >
          <RouterLink
            class="btn btn-primary mb-3"
            to="/signup"
            @click="closeMenu"
            >Sign Up</RouterLink
          >
        </template>

        <!-- 메뉴 항목 -->
        <RouterLink class="menu-item" to="/" @click="closeMenu"
          >Home</RouterLink
        >
        <RouterLink class="menu-item" to="/news" @click="closeMenu"
          >News</RouterLink
        >
        <RouterLink class="menu-item" to="/saving" @click="closeMenu"
          >Deposit/Savings Rates</RouterLink
        >
        <RouterLink class="menu-item" to="/metal" @click="closeMenu"
          >Stock & Commodity Prices</RouterLink
        >
        <RouterLink class="menu-item" to="/youtube" @click="closeMenu"
          >Investment Videos</RouterLink
        >
        <RouterLink class="menu-item" to="/bank" @click="closeMenu"
          >Find Banks</RouterLink
        >
        <RouterLink class="menu-item" to="/recommendations" @click="closeMenu"
          >AI 금융 추천</RouterLink
        >
        <RouterLink class="menu-item" to="/community" @click="closeMenu"
          >Community</RouterLink
        >
      </div>
    </div>

    <RouterView />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"; // onMounted 추가
import { RouterLink, RouterView, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import axios from "axios";

const router = useRouter();
const userStore = useUserStore();
const showMenu = ref(false);

const toggleMenu = () => {
  showMenu.value = !showMenu.value;
};

const closeMenu = () => {
  showMenu.value = false;
};

const logout = async () => {
  try {
    await axios.post("/api/accounts/logout/");
    userStore.logout();
    router.push("/");
    showMenu.value = false; // 로그아웃 시 메뉴 닫기
  } catch (err) {
    console.error("로그아웃 실패:", err);
  }
};

// 앱 시작 시 사용자 세션 유효성 검사
onMounted(async () => {
  try {
    await userStore.validateSession();
  } catch (error) {
    // validateSession 내부에서 401/403 에러 시 logout 처리하므로,
    // 여기서는 추가적인 에러 핸들링이 필요 없을 수 있습니다.
    // 필요하다면, 사용자에게 알림을 표시하는 등의 처리를 할 수 있습니다.
    console.warn("Session validation failed on app mount:", error.message);
  }
});
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
  top: 60px; /* Adjust based on navbar height */
  right: 0;
  width: max-content; /* Adjust width as needed */
  /* max-width: 280px; */ /* Example max-width */
  padding: 1rem;
  background-color: #fff;
  border-left: 1px solid #ddd;
  box-shadow: -2px 0 6px rgba(0, 0, 0, 0.1);
  z-index: 1050; /* Ensure it's above other content */
  white-space: nowrap; /* Prevent text wrapping */
}

.menu-item {
  display: block;
  padding: 6px 0; /* Reduced padding */
  color: #212529;
  text-decoration: none;
  text-align: left; /* Ensure text is left-aligned */
  font-weight: 500;
  transition: color 0.3s ease;
}

.menu-item:hover {
  color: #0d6efd;
}
</style>
