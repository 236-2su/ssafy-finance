import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    isLogin: localStorage.getItem("isLogin") === "true",
    username: localStorage.getItem("username") || "",
    email: localStorage.getItem("email") || "",
    user: null,
    isValidating: false,
  }),
  actions: {
    login(username, email = "") {
      this.isLogin = true;
      this.username = username;
      this.email = email;
      localStorage.setItem("isLogin", "true");
      localStorage.setItem("username", username);
      if (email) {
        localStorage.setItem("email", email);
      }
    },
    logout() {
      this.isLogin = false;
      this.username = "";
      this.email = "";
      localStorage.removeItem("isLogin");
      localStorage.removeItem("username");
      localStorage.removeItem("email");
    },
    async validateSession() {
      if (this.isValidating) return;
      
      this.isValidating = true;
      try {
        const response = await axios.get('/api/accounts/current-user/');
        // 세션이 유효하면 사용자 정보 업데이트
        if (response.data.is_authenticated) {
          this.login(response.data.username, response.data.email);
          return true;
        } else {
          this.logout();
          return false;
        }
      } catch (error) {
        // 세션이 무효하면 로그아웃 처리
        if (error.response?.status === 403 || error.response?.status === 401) {
          this.logout();
          return false;
        }
        throw error;
      } finally {
        this.isValidating = false;
      }
    },
    async checkAuthAndRedirect(router, redirectPath = '/login') {
      if (!this.isLogin) {
        router.push(redirectPath);
        return false;
      }
      
      try {
        const isValid = await this.validateSession();
        if (!isValid) {
          router.push(redirectPath);
          return false;
        }
        return true;
      } catch (error) {
        console.error('Authentication check failed:', error);
        router.push(redirectPath);
        return false;
      }
    },
    async fetchUserProfile() {
      try {
        const response = await axios.get('/api/accounts/profile/');
        this.user = response.data;
        return response.data;
      } catch (error) {
        console.error('Failed to fetch user profile:', error);
        throw error;
      }
    }
  },
});
