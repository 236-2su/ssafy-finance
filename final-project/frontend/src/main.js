import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";
import axios from "axios";

// ✅ Bootstrap JS (Vite 방식)
import "bootstrap/dist/js/bootstrap.bundle.min.js";

// ✅ Bootstrap CSS (선택적으로 여기서 불러올 수도 있음)
// import 'bootstrap/dist/css/bootstrap.min.css'

const app = createApp(App);
app.use(router);
app.use(createPinia());
app.mount("#app");
// CSRF 토큰 설정
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_API_URL;
