<template>
  <div class="login-container">
    <h2>로그인</h2>
    <form @submit.prevent="login">
      <input
        type="text"
        v-model="username"
        placeholder="아이디"
        required
        class="form-control mb-2"
      />
      <input
        type="password"
        v-model="password"
        placeholder="비밀번호"
        required
        class="form-control mb-2"
      />
      <button type="submit" class="btn btn-primary">로그인</button>
    </form>
    <p v-if="error" class="mt-3 text-danger">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";

const router = useRouter();
const userStore = useUserStore();

const username = ref("");
const password = ref("");
const error = ref("");

const login = async () => {
  try {
    const res = await axios.post("/api/accounts/login/", {
      username: username.value,
      password: password.value,
    });
    userStore.login(res.data.username); // ✅ username 저장
    router.push("/");
  } catch (err) {
    error.value = "로그인 실패: 아이디 또는 비밀번호를 확인해주세요.";
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 4rem auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f8f9fa;
}
</style>
