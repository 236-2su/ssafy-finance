import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";
import axios from "axios";

// ✅ Bootstrap JS (Vite 방식)
import "bootstrap/dist/js/bootstrap.bundle.min.js";

// ✅ Bootstrap CSS (선택적으로 여기서 불러올 수도 있음)
// import 'bootstrap/dist/css/bootstrap.min.css'

// CSRF 토큰 설정
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_API_URL;

// CSRF 토큰을 자동으로 가져오는 인터셉터 설정
let csrfToken = null;
let isGettingToken = false;

const getCsrfToken = async () => {
  if (isGettingToken) return csrfToken;
  
  isGettingToken = true;
  try {
    const response = await axios.get('/api/accounts/csrf-token/');
    csrfToken = response.data.csrfToken;
    return csrfToken;
  } catch (error) {
    console.error('CSRF 토큰 가져오기 실패:', error);
    return null;
  } finally {
    isGettingToken = false;
  }
};

axios.interceptors.request.use(async (config) => {
  // CSRF 토큰 요청 자체는 인터셉터를 건너뛰기
  if (config.url?.includes('/csrf-token/')) {
    return config;
  }
  
  // POST, PUT, PATCH, DELETE 요청에만 CSRF 토큰 추가
  if (['post', 'put', 'patch', 'delete'].includes(config.method?.toLowerCase())) {
    // 항상 최신 CSRF 토큰 가져오기
    const token = await getCsrfToken();
    if (token) {
      config.headers['X-CSRFToken'] = token;
    }
  }
  
  return config;
}, (error) => {
  return Promise.reject(error);
});

// 403 에러 시 CSRF 토큰 재설정 및 인증 에러 처리
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 403) {
      // CSRF 토큰 관련 에러인지 확인
      if (error.response?.data?.detail?.includes('CSRF')) {
        // CSRF 토큰 재설정
        csrfToken = null;
        if (!isGettingToken) {
          isGettingToken = true;
          try {
            const response = await axios.get('/api/accounts/csrf-token/');
            csrfToken = response.data.csrfToken;
            // 원래 요청 재시도
            error.config.headers['X-CSRFToken'] = csrfToken;
            return axios.request(error.config);
          } catch (csrfError) {
            console.error('CSRF 토큰 재설정 실패:', csrfError);
          } finally {
            isGettingToken = false;
          }
        }
      } else if (error.response?.data?.detail?.includes('Authentication credentials were not provided')) {
        // 인증 에러 - 사용자를 로그인 페이지로 리다이렉트
        console.warn('Authentication failed - redirecting to login');
        // 현재 페이지가 로그인 페이지가 아닌 경우에만 리다이렉트
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

const app = createApp(App);
app.use(router);
app.use(createPinia());
app.mount("#app");
