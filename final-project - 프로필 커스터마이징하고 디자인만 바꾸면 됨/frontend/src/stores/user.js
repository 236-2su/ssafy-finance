import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    isLogin: localStorage.getItem("isLogin") === "true",
    username: localStorage.getItem("username") || "",
  }),
  actions: {
    login(username) {
      this.isLogin = true;
      this.username = username;
      localStorage.setItem("isLogin", "true");
      localStorage.setItem("username", username);
    },
    logout() {
      this.isLogin = false;
      this.username = "";
      localStorage.removeItem("isLogin");
      localStorage.removeItem("username");
    },
  },
});
