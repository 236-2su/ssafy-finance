<template>
  <div class="container mt-5">
    <h2 class="mb-4">프로필 정보 수정</h2>
    <form @submit.prevent="updateProfile" class="card p-4 shadow-sm">
      <div class="mb-3">
        <label class="form-label">이메일</label>
        <input type="email" v-model="email" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">집 주소</label>
        <div class="input-group">
          <input
            type="text"
            v-model="homeAddress"
            class="form-control"
            placeholder="주소 검색 버튼을 이용해주세요"
            readonly
          />
          <button
            type="button"
            @click="openDaumPostcode('home')"
            class="btn btn-outline-secondary"
          >
            주소 검색
          </button>
        </div>
      </div>
      <div class="mb-3">
        <label class="form-label">회사 주소</label>
        <div class="input-group">
          <input
            type="text"
            v-model="companyAddress"
            class="form-control"
            placeholder="주소 검색 버튼을 이용해주세요"
            readonly
          />
          <button
            type="button"
            @click="openDaumPostcode('company')"
            class="btn btn-outline-secondary"
          >
            주소 검색
          </button>
        </div>
      </div>

      <!-- 비밀번호 변경 (선택) -->
      <div class="mb-3">
        <label class="form-label">새 비밀번호</label>
        <input type="password" v-model="newPassword" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">비밀번호 확인</label>
        <input type="password" v-model="passwordConfirm" class="form-control" />
      </div>

      <button type="submit" class="btn btn-primary">저장</button>
    </form>
    <p v-if="message" class="mt-3 text-success">{{ message }}</p>
    <p v-if="error" class="mt-3 text-danger">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const email = ref("");
const homeAddress = ref("");
const companyAddress = ref("");
const newPassword = ref("");
const passwordConfirm = ref("");
const message = ref("");
const error = ref("");

onMounted(async () => {
  try {
    const res = await axios.get("/api/accounts/profile/");
    email.value = res.data.email;
    homeAddress.value = res.data.home_address;
    companyAddress.value = res.data.company_address;
  } catch (err) {
    error.value = "사용자 정보를 불러오지 못했습니다.";
  }
});

const openDaumPostcode = (type) => {
  new daum.Postcode({
    oncomplete: function (data) {
      let fullAddress = data.roadAddress; // 도로명 주소 변수
      let extraAddress = ""; // 참고항목 변수

      if (data.bname !== "" && /[동|로|가]$/g.test(data.bname)) {
        extraAddress += data.bname;
      }
      if (data.buildingName !== "" && data.apartment === "Y") {
        extraAddress +=
          extraAddress !== "" ? ", " + data.buildingName : data.buildingName;
      }
      if (extraAddress !== "") {
        extraAddress = " (" + extraAddress + ")";
      }
      fullAddress += extraAddress;

      if (type === "home") {
        homeAddress.value = fullAddress;
      } else if (type === "company") {
        companyAddress.value = fullAddress;
      }
    },
  }).open();
};

const updateProfile = async () => {
  try {
    const res = await axios.put("/api/accounts/profile/", {
      email: email.value,
      home_address: homeAddress.value,
      company_address: companyAddress.value,
      new_password: newPassword.value,
      password_confirm: passwordConfirm.value,
    });
    message.value = res.data.message;

    // ✅ 로그인 상태 유지, 1초 후 프로필 상세페이지로 이동
    setTimeout(() => {
      router.push("/profile");
    }, 1000);
  } catch (err) {
    error.value = err.response?.data?.message || "수정 실패";
  }
};
</script>
