<template>
  <div class="signup-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-6">
            <div class="signup-card">
              <div class="signup-header">
                <h2 class="signup-title">MyFin 회원가입</h2>
                <p class="signup-subtitle">계정을 만들어 시작하세요</p>
              </div>

              <form @submit.prevent="signup" class="signup-form">
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="username" class="form-label"
                        >사용자 이름 *</label
                      >
                      <input
                        id="username"
                        type="text"
                        v-model="username"
                        placeholder="사용자 이름을 입력하세요"
                        required
                        class="form-control"
                        @input="validateUsername"
                        @blur="validateUsername"
                      />
                      <div v-if="usernameError" class="form-error-message">
                        {{ usernameError }}
                      </div>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="email" class="form-label">이메일</label>
                      <input
                        id="email"
                        type="email"
                        v-model="email"
                        placeholder="이메일을 입력하세요"
                        class="form-control"
                        @input="validateEmail"
                        @blur="validateEmail"
                      />
                      <div v-if="emailError" class="form-error-message">
                        {{ emailError }}
                      </div>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="password" class="form-label"
                        >비밀번호 *</label
                      >
                      <input
                        id="password"
                        type="password"
                        v-model="password"
                        placeholder="비밀번호를 입력하세요"
                        required
                        class="form-control"
                        @input="validatePassword"
                        @blur="validatePassword"
                      />
                      <div v-if="passwordError" class="form-error-message">
                        {{ passwordError }}
                      </div>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="passwordConfirm" class="form-label"
                        >비밀번호 확인 *</label
                      >
                      <input
                        id="passwordConfirm"
                        type="password"
                        v-model="passwordConfirm"
                        placeholder="비밀번호를 다시 입력하세요"
                        required
                        class="form-control"
                        @input="validatePasswordConfirm"
                        @blur="validatePasswordConfirm"
                      />
                      <div
                        v-if="passwordConfirmError"
                        class="form-error-message"
                      >
                        {{ passwordConfirmError }}
                      </div>
                    </div>
                  </div>
                </div>

                <div class="form-group">
                  <label for="home_address" class="form-label">집 주소</label>
                  <div class="input-group">
                    <input
                      id="home_address"
                      type="text"
                      v-model="home_address"
                      placeholder="집 주소 검색 (선택 사항)"
                      class="form-control"
                      readonly
                      @click="openDaumPostcode('home')"
                    />
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="openDaumPostcode('home')"
                    >
                      검색
                    </button>
                  </div>
                </div>

                <div class="form-group">
                  <label for="company_address" class="form-label"
                    >회사 주소</label
                  >
                  <div class="input-group">
                    <input
                      id="company_address"
                      type="text"
                      v-model="company_address"
                      placeholder="회사 주소 검색 (선택 사항)"
                      class="form-control"
                      readonly
                      @click="openDaumPostcode('company')"
                    />
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="openDaumPostcode('company')"
                    >
                      검색
                    </button>
                  </div>
                </div>

                <button
                  type="submit"
                  class="btn btn-primary btn-signup"
                  :disabled="loading"
                >
                  <span
                    v-if="loading"
                    class="spinner-border spinner-border-sm me-2"
                  ></span>
                  {{ loading ? "계정 생성 중..." : "계정 만들기" }}
                </button>
              </form>

              <!-- Social Login Buttons -->
              <div class="social-login-divider my-4">
                <span class="divider-text">또는 소셜 계정으로 계속하기</span>
              </div>
              <div class="social-login-buttons">
                <a
                  href="http://localhost:8000/accounts/google/login/"
                  class="btn btn-social btn-google mb-2"
                >
                  <img
                    src="https://developers.google.com/identity/images/g-logo.png"
                    alt="Google logo"
                    class="social-icon"
                  />
                  Google 계정으로 로그인
                </a>
                <a
                  href="http://localhost:8000/accounts/kakao/login/"
                  class="btn btn-social btn-kakao"
                >
                  <img
                    src="https://developers.kakao.com/tool/resource/static/img/button/kakaotalksharing/kakaotalk_sharing_btn_medium.png"
                    alt="Kakao logo"
                    class="social-icon kakao-icon"
                  />
                  Kakao 계정으로 로그인
                </a>
              </div>
              <!-- End Social Login Buttons -->

              <div v-if="message" class="alert alert-danger mt-3">
                <i class="fas fa-exclamation-circle me-2"></i>
                {{ message }}
              </div>

              <div class="signup-footer">
                <p class="text-center">
                  이미 계정이 있으신가요?
                  <router-link to="/login" class="login-link"
                    >여기서 로그인하세요</router-link
                  >
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
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
const message = ref(""); // 전체 폼 관련 메시지 (예: 서버 응답 오류)
const loading = ref(false);

// 필드별 오류 메시지
const usernameError = ref("");
const emailError = ref("");
const passwordError = ref("");
const passwordConfirmError = ref("");

const openDaumPostcode = (type) => {
  new daum.Postcode({
    oncomplete: function (data) {
      let fullAddress = data.address;
      let extraAddress = "";

      if (data.addressType === "R") {
        if (data.bname !== "") {
          extraAddress += data.bname;
        }
        if (data.buildingName !== "") {
          extraAddress +=
            extraAddress !== "" ? `, ${data.buildingName}` : data.buildingName;
        }
        fullAddress += extraAddress !== "" ? ` (${extraAddress})` : "";
      }

      if (type === "home") {
        home_address.value = fullAddress;
      } else if (type === "company") {
        company_address.value = fullAddress;
      }
    },
  }).open();
};

// Individual field validation functions
const validateUsername = () => {
  usernameError.value = "";
  if (!username.value.trim()) {
    usernameError.value = "사용자 이름은 필수 항목입니다.";
    return false;
  }
  return true;
};

const validateEmail = () => {
  emailError.value = "";
  if (email.value && !/\S+@\S+\.\S+/.test(email.value)) {
    emailError.value =
      "유효한 이메일 주소를 입력해주세요 (예: user@example.com).";
    return false;
  }
  return true;
};

const validatePassword = () => {
  passwordError.value = "";
  if (!password.value) {
    passwordError.value = "비밀번호는 필수 항목입니다.";
    return false;
  } else if (password.value.length < 8) {
    passwordError.value = "비밀번호는 최소 8자 이상이어야 합니다.";
    return false;
  }
  return true;
};

const validatePasswordConfirm = () => {
  passwordConfirmError.value = "";
  if (!passwordConfirm.value) {
    passwordConfirmError.value = "비밀번호 확인은 필수 항목입니다.";
    return false;
  } else if (password.value !== passwordConfirm.value) {
    passwordConfirmError.value = "비밀번호가 일치하지 않습니다.";
    return false;
  }
  return true;
};

const validateForm = () => {
  // Run all individual validations
  const isUsernameValid = validateUsername();
  const isEmailValid = validateEmail();
  const isPasswordValid = validatePassword();
  const isPasswordConfirmValid = validatePasswordConfirm();

  message.value = ""; // Clear previous general messages
  return (
    isUsernameValid && isEmailValid && isPasswordValid && isPasswordConfirmValid
  );
};

const signup = async () => {
  if (!validateForm()) {
    // Ensure all fields are validated on submit attempt, even if not touched
    return;
  }

  loading.value = true;
  message.value = ""; // Clear previous general messages

  try {
    await axios.post("/api/accounts/signup/", {
      username: username.value,
      email: email.value || undefined, // Send undefined if empty
      password: password.value,
      home_address: home_address.value || undefined,
      company_address: company_address.value || undefined,
    });
    router.push("/login");
  } catch (err) {
    // 서버에서 오는 필드별 오류 처리 (선택적)
    if (err.response && err.response.data) {
      const errors = err.response.data;
      if (errors.username) usernameError.value = errors.username.join(" ");
      if (errors.email) emailError.value = errors.email.join(" ");
      if (errors.password) passwordError.value = errors.password.join(" ");
      // 기타 전역 오류 메시지
      if (errors.detail) message.value = errors.detail;
      else if (
        !usernameError.value &&
        !emailError.value &&
        !passwordError.value
      ) {
        message.value =
          "회원가입에 실패했습니다. 입력값을 확인하고 다시 시도해주세요.";
      }
    } else {
      message.value = "예상치 못한 오류가 발생했습니다. 다시 시도해주세요.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.signup-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  padding: 40px 0;
}

.hero-section {
  width: 100%;
  padding: 80px 0;
}

.signup-card {
  background: white;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.signup-header {
  text-align: center;
  margin-bottom: 2rem;
}

.signup-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.signup-subtitle {
  color: #666;
  font-size: 1rem;
  margin-bottom: 0;
}

.signup-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.form-control {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-control::placeholder {
  color: #adb5bd;
}

.btn-signup {
  width: 100%;
  padding: 0.875rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  transition: all 0.3s ease;
}

.btn-signup:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.btn-signup:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.alert {
  border-radius: 10px;
  border: none;
  padding: 1rem;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}

.signup-footer {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.login-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.form-error-message {
  color: #dc3545; /* Bootstrap's danger color */
  font-size: 0.875em;
  margin-top: 0.25rem;
}

.social-login-divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: #6c757d;
}

.social-login-divider::before,
.social-login-divider::after {
  content: "";
  flex: 1;
  border-bottom: 1px solid #dee2e6;
}

.social-login-divider:not(:empty)::before {
  margin-right: 0.5em;
}

.social-login-divider:not(:empty)::after {
  margin-left: 0.5em;
}

.divider-text {
  font-size: 0.9rem;
}

.social-login-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem; /* 버튼 사이 간격 */
  margin-bottom: 1.5rem; /* 아래쪽 여백 */
}

.btn-social {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 1px solid #dee2e6; /* 테두리 추가 */
}

.btn-social:hover {
  opacity: 0.9;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.social-icon {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}
.kakao-icon {
  width: 22px; /* 카카오 아이콘 크기 미세 조정 */
  height: 22px;
}

.btn-google {
  background-color: #ffffff;
  color: #495057; /* 구글 버튼 텍스트 색상 */
}

.btn-google:hover {
  background-color: #f8f9fa;
}

.btn-kakao {
  background-color: #fee500;
  color: #191919; /* 카카오 버튼 텍스트 색상 */
  border-color: #fee500;
}
.btn-kakao:hover {
  background-color: #fdd835;
}

/* Responsive Design */
@media (max-width: 768px) {
  .signup-card {
    margin: 1rem;
    padding: 2rem;
  }

  .signup-title {
    font-size: 1.5rem;
  }

  .hero-section {
    padding: 40px 0;
  }

  .row .col-md-6 {
    margin-bottom: 0;
  }
}
</style>
