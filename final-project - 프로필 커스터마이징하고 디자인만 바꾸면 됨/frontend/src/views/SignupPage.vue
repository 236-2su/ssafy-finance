<template>
  <div class="signup-container">
    <h2>회원가입</h2>
    <form @submit.prevent="signup">
      <input
        type="text"
        v-model="username"
        placeholder="아이디"
        required
        class="form-control mb-2"
      />
      <input
        type="email"
        v-model="email"
        placeholder="이메일"
        class="form-control mb-2"
      />
      <input
        type="password"
        v-model="password"
        placeholder="비밀번호"
        required
        class="form-control mb-2"
      />
      <input
        type="password"
        v-model="passwordConfirm"
        placeholder="비밀번호 확인"
        required
        class="form-control mb-2"
      />
      <!-- 선택 입력 -->
      <input
        type="text"
        v-model="home_address"
        placeholder="집 주소 (선택)"
        class="form-control mb-2"
      />
      <input
        type="text"
        v-model="company_address"
        placeholder="회사 주소 (선택)"
        class="form-control mb-2"
      />

      <button type="submit" class="btn btn-primary">가입하기</button>
    </form>
    <p v-if="message" class="mt-3 text-danger">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

const username = ref("");
const email = ref("");
const password = ref("");
const passwordConfirm = ref("");
const home_address = ref("");
const company_address = ref("");
const message = ref("");

const signup = async () => {
  if (password.value !== passwordConfirm.value) {
    message.value = "비밀번호가 일치하지 않습니다.";
    return;
  }

  try {
    await axios.post("/api/accounts/signup/", {
      username: username.value,
      email: email.value || undefined,
      password: password.value,
      home_address: home_address.value || undefined,
      company_address: company_address.value || undefined,
    });
    router.push("/login");
  } catch (err) {
    message.value = "회원가입 실패: " + JSON.stringify(err.response.data);
  }
};
</script>
