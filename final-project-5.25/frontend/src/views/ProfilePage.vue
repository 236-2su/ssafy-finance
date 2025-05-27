<template>
  <div class="profile-page">
    <div class="hero-section">
      <div class="container">
        <div class="hero-content">
          <div class="profile-avatar">
            <div class="avatar-circle">
              <i class="fas fa-user"></i>
            </div>
            <div class="avatar-status" v-if="isOwnProfile">
              <i class="fas fa-crown"></i>
            </div>
          </div>
          <h1 class="hero-title">{{ displayName }}님의 프로필</h1>
          <p class="hero-subtitle" v-if="isOwnProfile">
            개인정보를 관리하고 금융 활동을 확인하세요
          </p>
          <p class="hero-subtitle" v-else>
            {{ username }}님의 공개 프로필입니다
          </p>

          <!-- 설문조사 완료 상태 -->
          <div
            v-if="isOwnProfile && profile.survey_completed"
            class="survey-status completed"
          >
            <i class="fas fa-check-circle"></i>
            <span>투자 성향 설문조사 완료</span>
          </div>
          <div v-else-if="isOwnProfile" class="survey-status incomplete">
            <i class="fas fa-exclamation-circle"></i>
            <span>설문조사를 완료해주세요</span>
            <router-link to="/survey" class="survey-link"
              >설문조사 하기</router-link
            >
          </div>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="content-wrapper" v-if="loaded">
        <!-- 프로필 카드 -->
        <div class="profile-cards">
          <!-- 기본 정보 카드 -->
          <div class="info-card basic-info">
            <div class="card-header">
              <div class="card-icon">
                <i class="fas fa-id-card"></i>
              </div>
              <h3 class="card-title">기본 정보</h3>
            </div>
            <div class="card-content">
              <div class="info-item">
                <div class="info-label">
                  <i class="fas fa-user"></i>
                  아이디
                </div>
                <div class="info-value">
                  <RouterLink
                    :to="`/profile/${username}`"
                    class="username-link"
                  >
                    {{ username }}
                  </RouterLink>
                </div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <i class="fas fa-envelope"></i>
                  이메일
                </div>
                <div class="info-value">
                  {{ profile.email || "미입력" }}
                </div>
              </div>
              <div class="info-item" v-if="profile.phone">
                <div class="info-label">
                  <i class="fas fa-phone"></i>
                  전화번호
                </div>
                <div class="info-value">
                  {{ profile.phone }}
                </div>
              </div>
              <div class="info-item" v-if="profile.home_address">
                <div class="info-label" style="white-space: nowrap">
                  <i class="fas fa-home"></i>
                  집 주소
                </div>
                <div class="info-value">
                  {{ profile.home_address || "미입력" }}
                </div>
              </div>
              <div class="info-item" v-if="profile.company_address">
                <div class="info-label" style="white-space: nowrap">
                  <i class="fas fa-building"></i>
                  회사 주소
                </div>
                <div class="info-value">
                  {{ profile.company_address || "미입력" }}
                </div>
              </div>
            </div>
          </div>

          <!-- 투자 성향 카드 (설문조사 완료 시) -->
          <div
            class="info-card investment-info"
            v-if="isOwnProfile && profile.survey_completed"
          >
            <div class="card-header">
              <div class="card-icon">
                <i class="fas fa-chart-pie"></i>
              </div>
              <h3 class="card-title">투자 성향</h3>
            </div>
            <div class="card-content">
              <div class="info-item">
                <div class="info-label">
                  <i class="fas fa-graduation-cap"></i>
                  투자 경험
                </div>
                <div class="info-value">
                  {{ getInvestmentExperienceLabel(profile.stock_experience) }}
                </div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <i class="fas fa-balance-scale"></i>
                  투자 성향
                </div>
                <div class="info-value">
                  {{ getInvestmentStyleLabel(profile.investment_style) }}
                </div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <i class="fas fa-wallet"></i>
                  월 투자금액
                </div>
                <div class="info-value">
                  {{ getMonthlyAmountLabel(profile.monthly_investment_amount) }}
                </div>
              </div>
              <div class="info-item">
                <div class="info-label">
                  <i class="fas fa-bullseye"></i>
                  <!-- 투자 목적 아이콘 변경/추가 -->
                  투자 목적
                </div>
                <div class="info-value">
                  {{ getInvestmentGoalLabel(profile.investment_goal) }}
                </div>
              </div>
              <button
                @click="goToSurvey"
                class="btn btn-outline-primary mt-3 w-100"
              >
                <i class="fas fa-redo-alt me-2"></i>설문조사 다시하기
              </button>
            </div>
          </div>

          <!-- 빠른 액션 카드 (본인만 볼 수 있음) -->
          <div class="info-card quick-actions" v-if="isOwnProfile">
            <div class="card-header">
              <div class="card-icon">
                <i class="fas fa-bolt"></i>
              </div>
              <h3 class="card-title">빠른 액션</h3>
            </div>
            <div class="card-content">
              <div class="action-buttons">
                <button class="action-btn primary" @click="goEdit">
                  <i class="fas fa-edit"></i>
                  <span>정보 수정</span>
                </button>
                <router-link to="/recommendations" class="action-btn secondary">
                  <i class="fas fa-lightbulb"></i>
                  <span>투자 추천</span>
                </router-link>
                <button class="action-btn tertiary" @click="goToCommunity">
                  <i class="fas fa-users"></i>
                  <span>커뮤니티</span>
                </button>
                <button class="action-btn quaternary" @click="goToVideos">
                  <i class="fas fa-video"></i>
                  <span>저장한 영상</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 보유 주식 섹션 -->
        <div class="section" v-if="isOwnProfile">
          <h3 class="section-title">
            <i class="fas fa-chart-line"></i>
            보유 주식
            <button
              @click="toggleOwnedStockSearch"
              class="btn btn-sm btn-outline-primary ms-2"
            >
              <i
                :class="showOwnedStockSearch ? 'fas fa-times' : 'fas fa-plus'"
              ></i>
            </button>
          </h3>
          <div v-if="showOwnedStockSearch" class="stock-search-section mb-3">
            <input
              type="text"
              v-model="ownedStockSearchQuery"
              @input="debouncedSearchOwnedStocks"
              placeholder="주식명 또는 코드 검색"
              class="form-control mb-2"
            />
            <div
              v-if="ownedStockSearchResults.length > 0"
              class="search-results list-group"
            >
              <button
                type="button"
                class="list-group-item list-group-item-action"
                v-for="stock in ownedStockSearchResults"
                :key="stock.stock_code"
                @click="addStock('owned', stock)"
              >
                {{ stock.stock_name }} ({{ stock.stock_code }})
              </button>
            </div>
          </div>
          <div
            v-if="profile.owned_stocks && profile.owned_stocks.length > 0"
            class="stock-grid"
          >
            <div
              v-for="stock in profile.owned_stocks"
              :key="stock.code"
              class="stock-card"
            >
              <div class="stock-info">
                <div class="stock-name">{{ stock.name }}</div>
                <div class="stock-code">{{ stock.code }}</div>
              </div>
              <div class="stock-actions">
                <button
                  @click="removeStock('owned', stock.code)"
                  class="btn-remove"
                >
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
          </div>
          <p v-else-if="!showOwnedStockSearch" class="text-muted">
            보유 주식이 없습니다.
          </p>
        </div>

        <!-- 관심 주식 섹션 -->
        <div class="section" v-if="isOwnProfile">
          <h3 class="section-title">
            <i class="fas fa-heart"></i>
            관심 주식
            <button
              @click="toggleInterestedStockSearch"
              class="btn btn-sm btn-outline-primary ms-2"
            >
              <i
                :class="
                  showInterestedStockSearch ? 'fas fa-times' : 'fas fa-plus'
                "
              ></i>
            </button>
          </h3>
          <div
            v-if="showInterestedStockSearch"
            class="stock-search-section mb-3"
          >
            <input
              type="text"
              v-model="interestedStockSearchQuery"
              @input="debouncedSearchInterestedStocks"
              placeholder="주식명 또는 코드 검색"
              class="form-control mb-2"
            />
            <div
              v-if="interestedStockSearchResults.length > 0"
              class="search-results list-group"
            >
              <button
                type="button"
                class="list-group-item list-group-item-action"
                v-for="stock in interestedStockSearchResults"
                :key="stock.stock_code"
                @click="addStock('interested', stock)"
              >
                {{ stock.stock_name }} ({{ stock.stock_code }})
              </button>
            </div>
          </div>
          <div
            v-if="
              profile.interested_stocks && profile.interested_stocks.length > 0
            "
            class="stock-grid"
          >
            <div
              v-for="(stockName, index) in profile.interested_stocks"
              :key="`interested-${stockName}-${index}`"
              class="stock-card"
            >
              <div class="stock-info">
                <div class="stock-name">{{ stockName }}</div>
                <!-- <div class="stock-code">관심 주식은 이름만 표시</div> -->
              </div>
              <div class="stock-actions">
                <button
                  @click="removeStock('interested', stockName)"
                  class="btn-remove"
                >
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
          </div>
          <p v-else-if="!showInterestedStockSearch" class="text-muted">
            관심 주식이 없습니다.
          </p>
        </div>

        <!-- 스크랩한 글 섹션 -->
        <div class="section" v-if="isOwnProfile">
          <h3 class="section-title">
            <i class="fas fa-bookmark"></i>
            스크랩한 글
          </h3>
          <div v-if="scrappedPosts.length > 0" class="post-list">
            <div
              v-for="post in showAllScrapped
                ? scrappedPosts
                : scrappedPosts.slice(0, 5)"
              :key="post.id"
              class="post-item"
              @click="goToPostDetail(post.id)"
            >
              <div class="post-item-header">
                <span class="post-item-category"
                  >[{{ post.category_display }}]</span
                >
                <h4 class="post-item-title ms-2">{{ post.title }}</h4>
                <span class="post-item-author ms-auto"
                  >작성자: {{ post.author }}</span
                >
              </div>
            </div>
          </div>
          <button
            v-if="scrappedPosts.length > 5"
            @click="toggleShowAllScrapped"
            class="btn btn-outline-secondary mt-3"
          >
            {{ showAllScrapped ? "간략히 보기" : "더보기" }}
          </button>
          <p v-if="scrappedPosts.length === 0" class="text-muted">
            스크랩한 글이 없습니다.
          </p>
        </div>

        <!-- 추천 유튜브 영상 섹션 -->
        <div class="section" v-if="isOwnProfile && (recommendedVideosLoading || recommendedVideos.length > 0)">
          <h3 class="section-title">
            <i class="fas fa-video"></i>
            추천 영상
          </h3>
          <div v-if="recommendedVideosLoading" class="loading-section small-spinner">
            <div class="loading-spinner"></div>
            <p class="loading-text">추천 영상을 불러오는 중...</p>
          </div>
          <div v-else-if="recommendedVideos.length > 0" class="video-grid">
            <div
              v-for="video in recommendedVideos"
              :key="video.video_id"
              class="video-card"
              @click="openVideo(video)"
            >
              <div class="video-thumbnail">
                <img
                  :src="video.thumbnail_url || getYoutubeThumbnail(video.video_id)"
                  :alt="video.title"
                  @error="handleVideoImageError"
                />
                <!-- <div class="video-duration">{{ video.duration }}</div> -->
                <!-- 추천 영상에서는 duration, view_count 등 상세 정보가 없을 수 있음 -->
              </div>
              <div class="video-content">
                <h4 class="video-title">{{ video.title }}</h4>
                <p class="video-channel">{{ video.channel_title }}</p>
                <!-- <div class="video-meta">
                  <span class="video-views">조회수 {{ formatViews(video.view_count) }}</span>
                  <span class="video-date">{{ formatDate(video.published_at) }}</span>
                </div> -->
              </div>
              <!-- 추천 영상에는 별도 액션 버튼 (예: 나중에 보기 추가)이 필요하면 여기에 추가 -->
            </div>
          </div>
          <p v-else class="text-muted">
            추천할 영상이 없거나, 관심/보유 주식을 추가해주세요.
          </p>
        </div>

        <!-- 내가 작성한 글 섹션 -->
        <div class="section">
          <h3 class="section-title">
            <i class="fas fa-pen-alt"></i>
            {{ isOwnProfile ? "내가" : username + "님이" }} 작성한 글
          </h3>
          <div v-if="userPosts.length > 0" class="post-list">
            <div
              v-for="post in showAllUserPosts
                ? userPosts
                : userPosts.slice(0, 5)"
              :key="post.id"
              class="post-item"
              @click="goToPostDetail(post.id)"
            >
              <div class="post-item-header">
                <span class="post-item-category"
                  >[{{ post.category_display }}]</span
                >
                <h4 class="post-item-title ms-2">{{ post.title }}</h4>
              </div>
            </div>
          </div>
          <button
            v-if="userPosts.length > 5"
            @click="toggleShowAllUserPosts"
            class="btn btn-outline-secondary mt-3"
          >
            {{ showAllUserPosts ? "간략히 보기" : "더보기" }}
          </button>
          <p v-if="userPosts.length === 0" class="text-muted">
            작성한 글이 없습니다.
          </p>
        </div>

        <!-- 유튜브 나중에 볼 영상 섹션 -->
        <div
          class="section"
          v-if="
            isOwnProfile &&
            profile.watch_later_videos &&
            profile.watch_later_videos.length > 0
          "
        >
          <h3 class="section-title">
            <i class="fas fa-clock"></i>
            나중에 볼 영상
          </h3>
          <div class="video-grid">
            <div
              v-for="video in profile.watch_later_videos"
              :key="video.video_id"
              class="video-card"
              @click="openVideo(video)"
            >
              <div class="video-thumbnail">
                <img
                  :src="
                    video.thumbnail_url || getYoutubeThumbnail(video.video_id)
                  "
                  :alt="video.title"
                  @error="handleVideoImageError"
                />
                <div class="video-duration">{{ video.duration }}</div>
              </div>
              <div class="video-content">
                <h4 class="video-title">{{ video.title }}</h4>
                <p class="video-channel">{{ video.channel_title }}</p>
                <div class="video-meta">
                  <span class="video-views"
                    >조회수 {{ formatViews(video.view_count) }}</span
                  >
                  <span class="video-date">{{
                    formatDate(video.published_at)
                  }}</span>
                </div>
              </div>
              <div class="video-actions">
                <button
                  @click.stop="removeWatchLater(video.video_id)"
                  class="btn-remove"
                >
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 구독 채널 섹션 -->
        <div
          class="section"
          v-if="
            isOwnProfile &&
            profile.subscribed_channels &&
            profile.subscribed_channels.length > 0
          "
        >
          <h3 class="section-title">
            <i class="fas fa-heart"></i>
            구독 채널
          </h3>
          <div class="channel-grid">
            <div
              v-for="channel in profile.subscribed_channels"
              :key="channel.channel_id"
              class="channel-card"
              @click="openChannel(channel)"
            >
              <div class="channel-thumbnail">
                <img
                  :src="channel.thumbnail_url || getDefaultChannelImage()"
                  :alt="channel.title"
                  @error="handleChannelImageError"
                />
              </div>
              <div class="channel-content">
                <h4 class="channel-title">{{ channel.title }}</h4>
                <p class="channel-description">
                  {{ truncateText(channel.description, 80) }}
                </p>
                <div class="channel-meta">
                  <span class="channel-subscribers"
                    >구독자 {{ formatViews(channel.subscriber_count) }}</span
                  >
                </div>
              </div>
              <div class="channel-actions">
                <button
                  @click.stop="removeSubscription(channel.channel_id)"
                  class="btn-remove"
                >
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 관련 뉴스 섹션 -->
        <div class="section" v-if="isOwnProfile && relatedNews.length > 0">
          <h3 class="section-title">
            <i class="fas fa-newspaper"></i>
            관련 뉴스
          </h3>
          <div class="news-grid">
            <div
              v-for="news in relatedNews"
              :key="news.id"
              class="news-card"
              @click="openNews(news)"
            >
              <div class="news-image">
                <img
                  v-if="news.image_url"
                  :src="news.image_url"
                  :alt="news.title"
                />
                <div v-else class="news-placeholder">
                  <i class="fas fa-newspaper"></i>
                </div>
              </div>
              <div class="news-content">
                <h4 class="news-title">{{ news.title }}</h4>
                <p class="news-summary">
                  {{ truncateText(news.summary || news.content, 100) }}
                </p>
                <div class="news-meta">
                  <span class="news-date">{{
                    formatDate(news.published_date)
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 최근 활동 섹션 -->
        <div class="section" v-if="isOwnProfile">
          <h3 class="section-title">
            <i class="fas fa-clock"></i>
            최근 활동
          </h3>
          <div class="activity-list">
            <div v-if="activities.length > 0">
              <div
                v-for="activity in activities"
                :key="activity.id"
                class="activity-item"
              >
                <div class="activity-icon">
                  <i :class="getActivityIcon(activity.activity_type)"></i>
                </div>
                <div class="activity-content">
                  <div class="activity-title">
                    {{ getActivityTitle(activity.activity_type) }}
                  </div>
                  <div class="activity-description">
                    {{ activity.description }}
                  </div>
                  <div class="activity-time">
                    {{ formatDate(activity.created_at) }}
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="no-activity">
              <i class="fas fa-clock"></i>
              <p>아직 활동 내역이 없습니다.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 로딩 상태 -->
      <div v-else class="loading-section">
        <div class="loading-spinner"></div>
        <p class="loading-text">프로필을 불러오는 중...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRouter, useRoute, RouterLink } from "vue-router";
import { useUserStore } from "@/stores/user";
import axios from "axios";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const username = route.params.username || userStore.username;

const profile = ref({
  email: "",
  phone: "",
  home_address: "",
  company_address: "",
  stock_experience: "",
  investment_style: "",
  monthly_investment_amount: "",
  investment_goal: "",
  owned_stocks: [],
  interested_stocks: [],
  survey_completed: false,
});

// 주식 검색 관련
const showOwnedStockSearch = ref(false);
const ownedStockSearchQuery = ref("");
const ownedStockSearchResults = ref([]);
const showInterestedStockSearch = ref(false);
const interestedStockSearchQuery = ref("");
const interestedStockSearchResults = ref([]);

const activities = ref([]);
const relatedNews = ref([]);
const scrappedPosts = ref([]);
const userPosts = ref([]);
const showAllScrapped = ref(false);
const showAllUserPosts = ref(false);

const recommendedVideos = ref([]);
const recommendedVideosLoading = ref(false);

const loaded = ref(false);

const isOwnProfile = computed(
  () => userStore.isLogin && userStore.username === username
);

const displayName = computed(() => (isOwnProfile.value ? "내" : `${username}`));

onMounted(async () => {
  if (isOwnProfile.value) {
    const isAuthenticated = await userStore.checkAuthAndRedirect(router);
    if (!isAuthenticated) {
      return;
    }
  } else if (!route.params.username) {
    router.push("/login");
    return;
  }

  try {
    const res = await axios.get(`/api/accounts/profile/${username}/`);
    profile.value = res.data;

    if (isOwnProfile.value) {
      await Promise.all([
        loadActivities(),
        loadRelatedNews(),
        loadScrappedPosts(true),
        loadUserPosts(true),
        loadRecommendedVideos(), // 추천 영상 로드 추가
      ]);
    } else {
      await loadUserPosts(true);
      // 타인 프로필의 경우, 공개된 관심/보유 주식 기반 추천은 현재 User 모델에 공개 필드가 없으므로 생략
      // 만약 공개 주식 정보가 있다면 여기서 호출 가능
    }
  } catch (err) {
    console.error("프로필 조회 실패:", err);
    if (err.response?.status === 403 || err.response?.status === 401) {
      alert("로그인이 필요합니다.");
      router.push("/login");
    } else {
      alert("프로필을 불러올 수 없습니다.");
      router.push("/");
    }
  } finally {
    loaded.value = true;
  }
});

// profile.owned_stocks 또는 profile.interested_stocks가 변경될 때 추천 영상을 다시 로드
watch(
  () => [profile.value.owned_stocks, profile.value.interested_stocks],
  async (newStocks, oldStocks) => {
    // 초기 로드 시에는 onMounted에서 이미 호출되므로, 변경 시에만 호출
    if (loaded.value && isOwnProfile.value) {
      // 배열 내용 비교를 위해 JSON.stringify 사용 (더 정교한 비교가 필요할 수 있음)
      if (JSON.stringify(newStocks) !== JSON.stringify(oldStocks)) {
        await loadRecommendedVideos();
      }
    }
  },
  { deep: true }
);

const loadRecommendedVideos = async () => {
  if (!isOwnProfile.value) return;

  recommendedVideosLoading.value = true;
  recommendedVideos.value = [];
  const stockKeywords = new Set();

  (profile.value.owned_stocks || []).forEach(stock => {
    if (stock && stock.name) {
      stockKeywords.add(stock.name);
    }
  });
  (profile.value.interested_stocks || []).forEach(stockName => {
    if (stockName) {
      stockKeywords.add(stockName);
    }
  });

  if (stockKeywords.size === 0) {
    recommendedVideosLoading.value = false;
    return;
  }

  const videoResults = [];
  const videoIds = new Set(); // 중복 영상 제거용

  try {
    for (const keyword of stockKeywords) {
      // 각 키워드에 대해 유튜브 검색 (예: "삼성전자 주식")
      const searchQuery = `${keyword} 주식`; // 검색어 예시, 필요시 조정
      try {
        const response = await axios.get("/api/youtube/search/", {
          params: { q: searchQuery, maxResults: 3 }, // 주식당 3개 영상
        });
        if (response.data && response.data.items) {
          response.data.items.forEach(item => {
            if (item.id && item.id.videoId && !videoIds.has(item.id.videoId)) {
              videoIds.add(item.id.videoId);
              videoResults.push({
                video_id: item.id.videoId,
                title: item.snippet.title,
                channel_title: item.snippet.channelTitle,
                thumbnail_url: item.snippet.thumbnails.medium.url, // 또는 high
                // published_at: item.snippet.publishedAt, // 필요시 추가
                // duration, view_count 등은 상세 API 호출 필요 (여기서는 목록 API 결과만 사용)
              });
            }
          });
        }
      } catch (searchError) {
        console.error(`Error searching YouTube for ${keyword}:`, searchError);
        // 개별 검색 실패 시 계속 진행
      }
    }
    // 전체 영상 개수 제한 (예: 최대 10개)
    recommendedVideos.value = videoResults.slice(0, 10);
  } catch (error) {
    console.error("Error loading recommended videos:", error);
    recommendedVideos.value = [];
  } finally {
    recommendedVideosLoading.value = false;
  }
};

const loadActivities = async () => {
  try {
    const response = await axios.get("/api/accounts/activities/");
    activities.value = response.data.slice(0, 5);
  } catch (error) {
    console.error("활동 내역 로드 실패:", error);
  }
};

const goToPostDetail = (postId) => {
  router.push(`/community/post/${postId}`); // 경로 수정
};

const loadScrappedPosts = async (isInitial = false) => {
  if (!isOwnProfile.value) return;
  try {
    const limit = isInitial && !showAllScrapped.value ? 5 : null;
    const url = limit
      ? `/api/accounts/scrapped-posts/?limit=${limit}`
      : "/api/accounts/scrapped-posts/";
    const response = await axios.get(url);
    scrappedPosts.value = response.data;
  } catch (error) {
    console.error("스크랩한 글 로드 실패:", error);
    scrappedPosts.value = [];
  }
};

const loadUserPosts = async (isInitial = false) => {
  try {
    const limit = isInitial && !showAllUserPosts.value ? 5 : null;
    const url = limit
      ? `/api/community/posts/?author_username=${username}&limit=${limit}` // author -> author_username 변경
      : `/api/community/posts/?author_username=${username}`; // author -> author_username 변경
    const response = await axios.get(url);
    userPosts.value = response.data.results || response.data || [];
  } catch (error) {
    console.error("작성한 글 로드 실패:", error);
    userPosts.value = [];
  }
};

const toggleShowAllScrapped = () => {
  showAllScrapped.value = !showAllScrapped.value;
  loadScrappedPosts();
};

const toggleShowAllUserPosts = () => {
  showAllUserPosts.value = !showAllUserPosts.value;
  loadUserPosts();
};

const debounce = (func, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(null, args);
    }, delay);
  };
};

const searchStocksAPI = async (query, resultsRef) => {
  if (query.trim() === "") {
    resultsRef.value = [];
    return;
  }
  try {
    const response = await axios.get(`/api/main/stocks/search/?query=${query}`);
    resultsRef.value = response.data;
  } catch (error) {
    console.error("Error searching stocks:", error);
    resultsRef.value = [];
  }
};

const debouncedSearchOwnedStocks = debounce(
  () => searchStocksAPI(ownedStockSearchQuery.value, ownedStockSearchResults),
  300
);
const debouncedSearchInterestedStocks = debounce(
  () =>
    searchStocksAPI(
      interestedStockSearchQuery.value,
      interestedStockSearchResults
    ),
  300
);

const toggleOwnedStockSearch = () => {
  showOwnedStockSearch.value = !showOwnedStockSearch.value;
  if (!showOwnedStockSearch.value) {
    ownedStockSearchQuery.value = "";
    ownedStockSearchResults.value = [];
  }
};

const toggleInterestedStockSearch = () => {
  showInterestedStockSearch.value = !showInterestedStockSearch.value;
  if (!showInterestedStockSearch.value) {
    interestedStockSearchQuery.value = "";
    interestedStockSearchResults.value = [];
  }
};

const addStock = async (type, stockFromSearch) => {
  // stockFromSearch는 { stock_code: '...', stock_name: '...' } 형태
  try {
    if (type === "interested") {
      const stockName = stockFromSearch.stock_name;
      if (
        profile.value.interested_stocks &&
        profile.value.interested_stocks.includes(stockName)
      ) {
        alert("이미 관심 목록에 있는 주식입니다.");
        return;
      }
      // 백엔드 UserStocksView의 POST는 stock_name을 직접 받음
      await axios.post("/api/accounts/stocks/", { stock_name: stockName });
      // userStore를 통해 상태를 업데이트하거나, 프로필을 다시 fetch 할 수 있음
      // 여기서는 직접 profile.value.interested_stocks를 업데이트 (userStore 연동 시 변경 필요)
      if (!profile.value.interested_stocks) {
        profile.value.interested_stocks = [];
      }
      profile.value.interested_stocks.push(stockName);
      toggleInterestedStockSearch();
    } else if (type === "owned") {
      const stockData = {
        code: stockFromSearch.stock_code,
        name: stockFromSearch.stock_name,
      };
      if (
        profile.value.owned_stocks &&
        profile.value.owned_stocks.find((s) => s.code === stockData.code)
      ) {
        alert("이미 보유 목록에 있는 주식입니다.");
        return;
      }
      // 보유 주식 추가 API가 별도로 있다면 호출, 여기서는 UserStocksView가 type으로 구분한다고 가정
      // 하지만 UserStocksView는 현재 관심 주식만 처리하도록 변경했으므로, 보유 주식 로직은 분리 또는 수정 필요
      // 백엔드 UserStocksView의 POST는 type: "owned" 와 함께 stock_data 객체를 기대함
      await axios.post("/api/accounts/stocks/", {
        type: "owned",
        stock_data: stockData,
      });
      if (!profile.value.owned_stocks) {
        profile.value.owned_stocks = [];
      }
      profile.value.owned_stocks.push(stockData);
      toggleOwnedStockSearch();
    }
  } catch (error) {
    console.error("주식 추가 실패:", error);
    alert("주식 추가 중 오류가 발생했습니다.");
  }
};

const loadRelatedNews = async () => {
  try {
    const ownedStocksForNews = (profile.value.owned_stocks || []).filter(
      (stock) => stock && stock.name && typeof stock.name === "string"
    ); // Ensure stock.name is a non-null string

    const interestedStocksForNews = (profile.value.interested_stocks || [])
      .filter((stockName) => stockName && typeof stockName === "string") // Ensure stockName is a non-null string
      .map((stockName) => ({ name: stockName }));

    const allStockObjects = [...ownedStocksForNews, ...interestedStocksForNews];

    if (allStockObjects.length > 0) {
      const response = await axios.get("/api/news/");
      const allNews = response.data || [];

      relatedNews.value = allNews
        .filter((news) => {
          if (!news || typeof news.title !== "string") return false;
          return allStockObjects.some((stock) => {
            // stock.name is already validated to be a non-null string by prior filters/maps
            const stockName = stock.name; // stock is guaranteed to have a 'name' property here
            return (
              news.title.includes(stockName) ||
              (news.content &&
                typeof news.content === "string" &&
                news.content.includes(stockName))
            );
          });
        })
        .slice(0, 6);
    } else {
      relatedNews.value = []; // No stocks to relate news to, so clear related news
    }
  } catch (error) {
    console.error("관련 뉴스 로드 실패:", error);
    relatedNews.value = []; // Ensure relatedNews is cleared on error
  }
};

const removeStock = async (type, identifier) => {
  // identifier는 stockCode 또는 stockName
  try {
    if (type === "interested") {
      const stockName = identifier;
      // 백엔드 UserStocksView의 DELETE는 stock_name을 직접 받음
      await axios.delete("/api/accounts/stocks/", {
        data: { stock_name: stockName },
      });
      // userStore를 통해 상태를 업데이트하거나, 프로필을 다시 fetch 할 수 있음
      // 여기서는 직접 profile.value.interested_stocks를 업데이트
      if (profile.value.interested_stocks) {
        profile.value.interested_stocks =
          profile.value.interested_stocks.filter(
            (sName) => sName !== stockName
          );
      }
    } else if (type === "owned") {
      const stockCode = identifier;
      // 보유 주식 제거 API가 별도로 있다면 호출, 여기서는 UserStocksView가 type으로 구분한다고 가정
      // 하지만 UserStocksView는 현재 관심 주식만 처리하도록 변경했으므로, 보유 주식 로직은 분리 또는 수정 필요
      await axios.delete("/api/accounts/stocks/", {
        data: {
          type: "owned", // 이 부분은 백엔드 UserStocksView가 owned도 처리할 경우 유효
          stock_code: stockCode,
        },
      });
      if (profile.value.owned_stocks) {
        profile.value.owned_stocks = profile.value.owned_stocks.filter(
          (stock) => stock.code !== stockCode
        );
      }
    }
  } catch (error) {
    console.error("주식 제거 실패:", error);
    alert("주식 제거 중 오류가 발생했습니다.");
  }
};

const openNews = (news) => {
  router.push(`/news/${news.id}`);
};

const goEdit = () => {
  router.push({ path: `/profile/edit`, query: { username } });
};

const goToCommunity = () => {
  router.push("/community");
};

const goToSurvey = () => {
  router.push({ path: "/survey", query: { retake: "true" } });
};

const goToVideos = () => {
  router.push("/youtube/later");
};

const openVideo = (video) => {
  router.push(`/youtube/video/${video.video_id}`);
};

const openChannel = (channel) => {
  router.push(`/youtube/channel/${channel.channel_id}`);
};

const removeWatchLater = async (videoId) => {
  try {
    await axios.delete("/api/accounts/youtube/", {
      data: {
        type: "video",
        content_id: videoId,
      },
    });

    profile.value.watch_later_videos = profile.value.watch_later_videos.filter(
      (video) => video.video_id !== videoId
    );
  } catch (error) {
    console.error("나중에 볼 영상 제거 실패:", error);
    alert("영상 제거 중 오류가 발생했습니다.");
  }
};

const removeSubscription = async (channelId) => {
  try {
    await axios.delete("/api/accounts/youtube/", {
      data: {
        type: "channel",
        content_id: channelId,
      },
    });

    profile.value.subscribed_channels =
      profile.value.subscribed_channels.filter(
        (channel) => channel.channel_id !== channelId
      );
  } catch (error) {
    console.error("구독 채널 제거 실패:", error);
    alert("채널 제거 중 오류가 발생했습니다.");
  }
};

const formatViews = (count) => {
  if (!count) return "0";
  if (count >= 10000) {
    return Math.floor(count / 10000) + "만";
  } else if (count >= 1000) {
    return Math.floor(count / 1000) + "천";
  }
  return count.toString();
};

const formatDate = (dateString) => {
  if (!dateString) return "미입력";
  const date = new Date(dateString);
  return date.toLocaleDateString("ko-KR");
};

const truncateText = (text, maxLength) => {
  if (!text) return "";
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
};

const getInvestmentExperienceLabel = (value) => {
  const labels = {
    none: "투자 경험 없음",
    beginner: "초보 (1년 미만)",
    intermediate: "중급 (1-3년)",
    advanced: "고급 (3년 이상)",
  };
  return labels[value] || "미설정";
};

const getInvestmentStyleLabel = (value) => {
  const labels = {
    conservative: "안전형",
    moderate: "중립형",
    aggressive: "공격형",
  };
  return labels[value] || "미설정";
};

const getMonthlyAmountLabel = (value) => {
  const labels = {
    under_50: "50만원 미만",
    "50_100": "50-100만원",
    "100_300": "100-300만원",
    over_300: "300만원 이상",
  };
  return labels[value] || "미설정";
};

const getInvestmentGoalLabel = (value) => {
  const labels = {
    short_term: "단기 수익",
    long_term: "장기 투자",
    retirement: "은퇴 준비",
    emergency_fund: "비상 자금",
  };
  return labels[value] || "미설정";
};

const getActivityIcon = (activityType) => {
  const icons = {
    login: "fas fa-sign-in-alt",
    news_view: "fas fa-newspaper",
    video_watch: "fas fa-play",
    stock_search: "fas fa-chart-line",
    saving_search: "fas fa-piggy-bank",
    community_post: "fas fa-edit",
    community_comment: "fas fa-comment",
    survey_completed: "fas fa-check-circle",
  };
  return icons[activityType] || "fas fa-circle";
};

const getActivityTitle = (activityType) => {
  const titles = {
    login: "로그인",
    news_view: "뉴스 조회",
    video_watch: "영상 시청",
    stock_search: "주식 검색",
    saving_search: "예적금 검색",
    community_post: "커뮤니티 글 작성",
    community_comment: "댓글 작성",
    survey_completed: "설문조사 완료",
  };
  return titles[activityType] || "활동";
};

const getYoutubeThumbnail = (videoId) => {
  if (!videoId) return getDefaultVideoImage();
  return `https://i.ytimg.com/vi/${videoId}/mqdefault.jpg`;
};

const getDefaultVideoImage = () => {
  return "https://i.ytimg.com/vi/default.jpg";
};

const getDefaultChannelImage = () => {
  return "https://yt3.ggpht.com/a/default-user=s88-c-k-c0x00ffffff-no-rj";
};

const handleVideoImageError = (event) => {
  event.target.src = getDefaultVideoImage();
};

const handleChannelImageError = (event) => {
  event.target.src = getDefaultChannelImage();
};
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-section {
  padding: 80px 0 60px;
  text-align: center;
}

.hero-content {
  max-width: 600px;
  margin: 0 auto;
}

.profile-avatar {
  position: relative;
  display: inline-block;
  margin-bottom: 30px;
}

.avatar-circle {
  width: 120px;
  height: 120px;
  background: rgba(255, 255, 255, 0.2);
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: white;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.avatar-status {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 35px;
  height: 35px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  border: 3px solid white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.9rem;
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.4);
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  margin-bottom: 15px;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 20px;
  line-height: 1.6;
}

.survey-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 25px;
  font-weight: 600;
  margin-top: 10px;
}

.survey-status.completed {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
  border: 2px solid rgba(34, 197, 94, 0.3);
}

.survey-status.incomplete {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
  border: 2px solid rgba(251, 191, 36, 0.3);
}

.survey-link {
  color: white;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.2);
  padding: 5px 15px;
  border-radius: 15px;
  margin-left: 10px;
  transition: all 0.3s ease;
}

.survey-link:hover {
  background: rgba(255, 255, 255, 0.3);
  color: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.content-wrapper {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 30px 30px 0 0;
  padding: 40px;
  margin-top: -20px;
  backdrop-filter: blur(10px);
}

.profile-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.info-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.info-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.basic-info::before {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.investment-info::before {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.quick-actions::before {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f1f5f9;
}

.card-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  color: white;
}

.basic-info .card-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.investment-info .card-icon {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.quick-actions .card-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.card-content {
  flex: 1;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #f8fafc;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #64748b;
  font-size: 0.9rem;
}

.info-label i {
  width: 16px;
  color: #94a3b8;
}

.info-value {
  font-weight: 600;
  color: #333;
  text-align: right;
}

.username-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 700;
  transition: color 0.3s ease;
}

.username-link:hover {
  color: #5a67d8;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.secondary {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.action-btn.tertiary {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
  color: white;
}

.action-btn.quaternary {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.section {
  margin-bottom: 40px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f1f5f9;
}

.stock-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.stock-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.stock-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.stock-info {
  flex: 1;
}

.stock-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.stock-code {
  font-size: 0.8rem;
  color: #64748b;
}

.btn-remove {
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-remove:hover {
  background: #dc2626;
  transform: scale(1.1);
}

.post-list {
  display: grid;
  gap: 15px;
}

.post-item {
  background: white;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.post-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.post-link {
  text-decoration: none;
  color: inherit;
}

.post-item-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.post-item-category {
  font-size: 0.9rem; /* 크기 약간 키움 */
  color: #667eea;
  font-weight: 600;
  /* margin-bottom 제거 또는 조정 */
}

/* .post-item-content 와 .post-item-date 는 현재 템플릿에서 사용 안함 */
/* 필요시 주석 해제 또는 스타일 유지 */
/*
.post-item-content {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
  margin-bottom: 10px;
}

.post-item-date {
  font-size: 0.8rem;
  color: #94a3b8;
}
*/

.post-item-header {
  display: flex;
  align-items: center; /* 수직 중앙 정렬 */
  justify-content: space-between; /* 양쪽 끝으로 요소를 분산 */
  width: 100%;
}

.post-item-header .post-item-title {
  margin-bottom: 0; /* 제목 아래 여백 제거 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-grow: 1; /* 제목이 남은 공간을 차지하도록 */
  margin-right: 10px; /* 작성자와의 간격 */
}

.post-item-author {
  font-size: 0.85rem;
  color: #555;
  white-space: nowrap; /* 작성자 이름이 길어도 한 줄로 */
  flex-shrink: 0; /* 작성자 이름이 줄어들지 않도록 */
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.news-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
}

.news-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.news-image {
  height: 150px;
  overflow: hidden;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.news-placeholder {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
}

.news-content {
  padding: 20px;
}

.news-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.4;
}

.news-summary {
  color: #666;
  line-height: 1.5;
  margin-bottom: 15px;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.news-date {
  font-size: 0.8rem;
  color: #94a3b8;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}

.video-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.video-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.video-thumbnail {
  position: relative;
  height: 180px;
  overflow: hidden;
}

.video-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.video-content {
  padding: 15px;
}

.video-title {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-channel {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.video-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: #94a3b8;
}

.video-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.video-card:hover .video-actions {
  opacity: 1;
}

.channel-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.channel-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  display: flex;
  align-items: center;
  gap: 15px;
}

.channel-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.channel-thumbnail {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.channel-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.channel-content {
  flex: 1;
}

.channel-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.channel-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 8px;
}

.channel-meta {
  font-size: 0.8rem;
  color: #94a3b8;
}

.channel-actions {
  position: absolute;
  top: 15px;
  right: 15px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.channel-card:hover .channel-actions {
  opacity: 1;
}

.activity-list {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px 0;
  border-bottom: 1px solid #f1f5f9;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.activity-description {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 4px;
}

.activity-time {
  color: #94a3b8;
  font-size: 0.8rem;
}

.no-activity {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
}

.no-activity i {
  font-size: 3rem;
  margin-bottom: 15px;
}

.loading-section {
  text-align: center;
  padding: 80px 20px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

.loading-text {
  color: white;
  font-size: 1.1rem;
}

.loading-section.small-spinner .loading-spinner {
  width: 30px;
  height: 30px;
  border-width: 3px;
  margin-bottom: 10px;
}
.loading-section.small-spinner .loading-text {
  font-size: 0.9rem;
  color: #555; /* 흰색 배경이므로 어두운 색으로 변경 */
}


@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .profile-cards {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    grid-template-columns: 1fr;
  }

  .stock-grid {
    grid-template-columns: 1fr;
  }

  .news-grid {
    grid-template-columns: 1fr;
  }

  .content-wrapper {
    padding: 20px;
  }
}
</style>
