import { createRouter, createWebHistory } from "vue-router";

// 뷰 컴포넌트 import
import MainPage from "@/views/MainPage.vue";
import NewsPage from "@/views/NewsPage.vue";
import CommunityDetailPage from "@/views/CommunityDetailPage.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import CommunityEditPage from "@/views/CommunityEditPage.vue";
import YoutubePage from "@/views/YoutubePage.vue";
import SearchView from "@/views/SearchView.vue";
import LaterView from "@/views/LaterView.vue";
import ChannelView from "@/views/ChannelView.vue";
import VideoDetailView from "@/views/VideoDetailView.vue";
import SavingListView from "@/views/SavingListView.vue";
import SavingDetailView from "@/views/SavingDetailView.vue";
import SurveyPage from "@/views/SurveyPage.vue";
// import RecommendationPage from "@/views/RecommendationPage.vue"; // 기존 RecommendationPage는 더 이상 사용하지 않음
import AiRecommendationPage from "@/views/AiRecommendationPage.vue"; // 새로운 AI 추천 페이지만 사용

const routes = [
  { path: "/", name: "Main", component: MainPage },
  {
    path: "/news",
    name: "News",
    component: NewsPage,
  },
  {
    path: "/news/:id",
    name: "NewsDetail",
    component: () => import("@/views/NewsDetailPage.vue"),
    props: true,
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/LoginPage.vue"),
  },
  {
    path: "/signup",
    name: "Signup",
    component: () => import("@/views/SignupPage.vue"),
  },
  {
    path: "/saving",
    name: "SavingListView",
    component: SavingListView,
  },
  {
    path: "/saving/:fin_prdt_cd",
    name: "SavingDetailView",
    component: SavingDetailView,
  },
  {
    path: "/metal",
    name: "Metal",
    component: () => import("@/views/MetalPage.vue"),
  },
  {
    path: "/youtube",
    component: YoutubePage,
    children: [
      { path: "", name: "Search", component: SearchView },
      { path: "later", name: "Later", component: LaterView },
      { path: "channel", name: "Channel", component: ChannelView },
      {
        path: "video/:id",
        name: "VideoDetail",
        component: VideoDetailView,
        props: true,
      },
    ],
  },
  {
    path: "/bank",
    name: "Bank",
    component: () => import("@/views/BankPage.vue"),
  },
  {
    path: "/survey",
    name: "Survey",
    component: SurveyPage,
  },
  {
    path: "/recommendations", // 기존 경로 유지
    name: "Recommendations", // 기존 이름 유지 또는 "AiRecommendation"으로 변경 가능
    component: AiRecommendationPage, // 새로운 AI 추천 페이지 컴포넌트로 변경
  },
  // { // /ai-recommendation 경로는 삭제
  //   path: "/ai-recommendation",
  //   name: "AiRecommendation",
  //   component: AiRecommendationPage,
  // },

  // 커뮤니티
  {
    path: "/community",
    name: "Community",
    component: () => import("@/views/CommunityPage.vue"),
  },
  {
    path: "/community/write",
    name: "CommunityWrite",
    component: () => import("@/views/CommunityWritePage.vue"),
  },
  {
    path: "/community/post/:id",
    name: "CommunityDetail",
    component: CommunityDetailPage,
  },
  {
    path: "/community/edit/:id",
    name: "CommunityEdit",
    component: CommunityEditPage,
    props: true, // id를 props로 전달
  },

  // 프로필 수정은 동적 프로필보다 위에 둡니다!
  {
    path: "/profile/edit",
    name: "ProfileEdit",
    component: () => import("@/views/ProfileEditPage.vue"),
  },

  // 프로필 조회 (username 옵셔널)
  {
    path: "/profile/:username?",
    name: "UserProfile",
    component: ProfilePage,
    props: (route) => ({ username: route.params.username || null }),
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
