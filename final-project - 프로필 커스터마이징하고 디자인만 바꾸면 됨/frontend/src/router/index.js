import { createRouter, createWebHistory } from "vue-router";

// 뷰 컴포넌트 import
import MainPage from "@/views/MainPage.vue";
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

const routes = [
  { path: "/", name: "Main", component: MainPage },
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
