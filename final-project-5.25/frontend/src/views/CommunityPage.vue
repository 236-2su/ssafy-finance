<template>
  <div class="community-page">
    <div class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">커뮤니티</h1>
          <p class="hero-subtitle">금융 정보를 공유하고 소통하는 공간</p>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="content-wrapper">
        <!-- 카테고리 탭 -->
        <div class="category-section">
          <h2 class="section-title">게시판 카테고리</h2>
          <div class="category-tabs">
            <button
              v-for="(label, cat) in categories"
              :key="cat"
              class="category-tab"
              :class="{ active: category === cat }"
              @click="category = cat"
            >
              <i :class="getCategoryIcon(cat)"></i>
              <span>{{ label }}</span>
            </button>
          </div>
        </div>

        <!-- 통계 정보 -->
        <div class="stats-section">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-comments"></i>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ posts.length }}</div>
              <div class="stat-label">게시글</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-users"></i>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ getUniqueAuthors() }}</div>
              <div class="stat-label">활성 사용자</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-fire"></i>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ getTodayPosts() }}</div>
              <div class="stat-label">오늘 게시글</div>
            </div>
          </div>
        </div>

        <!-- 글 목록 -->
        <div class="posts-section">
          <div class="section-header">
            <h2 class="section-title">{{ categories[category] }}</h2>
            <RouterLink to="/community/write" class="write-btn">
              <i class="fas fa-pen"></i>
              글쓰기
            </RouterLink>
          </div>

          <div v-if="posts.length" class="posts-grid">
            <RouterLink
              v-for="post in posts"
              :key="post.id"
              :to="`/community/post/${post.id}`"
              class="post-card"
            >
              <div class="post-header">
                <div class="post-meta">
                  <span class="post-id">#{{ post.id }}</span>
                  <span class="post-category">{{
                    categories[post.category] || "기타"
                  }}</span>
                </div>
                <div class="post-author">
                  <RouterLink
                    :to="`/profile/${post.author}`"
                    class="author-link"
                    @click.stop
                  >
                    <div class="author-avatar">
                      {{
                        getAuthorInitial(post.author_nickname || post.author)
                      }}
                    </div>
                    <span class="author-name">{{
                      post.author_nickname || post.author
                    }}</span>
                  </RouterLink>
                </div>
              </div>

              <div class="post-content">
                <h3 class="post-title">{{ post.title }}</h3>
                <p class="post-preview" v-if="post.content">
                  {{ getPostPreview(post.content) }}
                </p>
              </div>

              <div class="post-footer">
                <div class="post-stats">
                  <span class="stat-item">
                    <i class="fas fa-eye"></i>
                    {{ post.views || 0 }}
                    <!-- API 응답에 'views' 필드가 없으므로 항상 0으로 표시될 것입니다. -->
                  </span>
                  <span class="stat-item">
                    <i class="fas fa-heart"></i>
                    {{ post.like_count || 0 }}
                    <!-- API 응답 필드명 'like_count' 사용 -->
                  </span>
                  <span class="stat-item">
                    <i class="fas fa-comment"></i>
                    {{ post.comments ? post.comments.length : 0 }}
                    <!-- API 응답의 'comments' 배열 길이 사용 -->
                  </span>
                </div>
                <div class="post-date">
                  <i class="fas fa-clock"></i>
                  {{ formatDate(post.created_at) }}
                </div>
              </div>
            </RouterLink>
          </div>

          <div v-else class="empty-state">
            <div class="empty-icon">
              <i class="fas fa-comments fa-4x"></i>
            </div>
            <h3 class="empty-title">아직 게시글이 없습니다</h3>
            <p class="empty-description">첫 번째 게시글을 작성해보세요!</p>
            <RouterLink to="/community/write" class="empty-action-btn">
              <i class="fas fa-pen"></i>
              첫 글 작성하기
            </RouterLink>
          </div>
        </div>

        <!-- 인기 게시글 사이드바 -->
        <div class="sidebar">
          <div class="widget">
            <h4 class="widget-title">인기 게시글</h4>
            <div class="popular-posts">
              <RouterLink
                v-for="(post, index) in popularPosts.slice(0, 5)"
                :key="post.id"
                :to="`/community/post/${post.id}`"
                class="popular-post"
              >
                <div class="popular-rank">{{ index + 1 }}</div>
                <div class="popular-content">
                  <h5 class="popular-title">{{ post.title }}</h5>
                  <div class="popular-meta">
                    <span class="popular-author">{{
                      post.author_nickname || post.author
                    }}</span>
                    <span class="popular-views">
                      <i class="fas fa-heart"></i>
                      {{ post.likes_display_count }}
                    </span>
                  </div>
                </div>
              </RouterLink>
              <div v-if="!popularPosts.length" class="empty-popular-posts">
                <p>인기 게시글이 없습니다.</p>
              </div>
            </div>
          </div>

          <div class="widget">
            <h4 class="widget-title">커뮤니티 규칙</h4>
            <div class="community-rules">
              <div class="rule-item">
                <i class="fas fa-check-circle"></i>
                <span>서로 존중하며 예의를 지켜주세요</span>
              </div>
              <div class="rule-item">
                <i class="fas fa-check-circle"></i>
                <span>정확한 정보를 공유해주세요</span>
              </div>
              <div class="rule-item">
                <i class="fas fa-check-circle"></i>
                <span>스팸이나 광고는 금지됩니다</span>
              </div>
              <div class="rule-item">
                <i class="fas fa-check-circle"></i>
                <span>건전한 토론 문화를 만들어가요</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
// onUnmounted는 visibilitychange 리스너 제거용이었으므로, 해당 리스너가 없어지면 onUnmounted도 필요 없음.
// onActivated 훅은 keep-alive 설정이 어려워 사용하지 않기로 함.
const category = ref(route.query.category || "free");
const posts = ref([]);
const popularPosts = ref([]);

const categories = {
  free: "자유게시판",
  invest: "투자 이야기",
  bank: "은행/기관 정보",
  qna: "Q&A",
};

// 카테고리 아이콘 매핑
const getCategoryIcon = (cat) => {
  const icons = {
    free: "fas fa-comments",
    invest: "fas fa-chart-line",
    bank: "fas fa-university",
    qna: "fas fa-question-circle",
  };
  return icons[cat] || "fas fa-comments";
};

// 작성자 이니셜 생성
const getAuthorInitial = (author) => {
  if (typeof author === "string" || author instanceof String) {
    return author ? author.charAt(0).toUpperCase() : "?";
  }
  // In case author is an object or not a string as expected
  return "?";
};

// 게시글 미리보기 생성
const getPostPreview = (content) => {
  if (!content) return "";
  return content.length > 100 ? content.substring(0, 100) + "..." : content;
};

// 고유 작성자 수 계산
const getUniqueAuthors = () => {
  const authors = new Set(
    posts.value.map((post) => post.author_nickname || post.author)
  );
  return authors.size;
};

// 오늘 작성된 게시글 수 계산
const getTodayPosts = () => {
  const today = new Date().toDateString();
  return posts.value.filter((post) => {
    const postDate = new Date(post.created_at).toDateString();
    return postDate === today;
  }).length;
};

// 날짜 포맷
const formatDate = (iso) => {
  const date = new Date(iso);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

  if (diffHours < 1) {
    return "방금 전";
  } else if (diffHours < 24) {
    return `${diffHours}시간 전`;
  } else if (diffDays < 7) {
    return `${diffDays}일 전`;
  } else {
    return date.toLocaleDateString("ko-KR");
  }
};

// API 호출
const fetchPosts = async () => {
  console.log(`Fetching posts for category: ${category.value}`); // 카테고리 확인 로그
  try {
    const res = await axios.get("/api/community/posts/", {
      params: { category: category.value },
    });
    console.log("Fetched posts data:", JSON.parse(JSON.stringify(res.data))); // 응답 데이터 로그 (깊은 복사로 프록시 객체 회피)
    posts.value = res.data;
  } catch (err) {
    console.error("게시글 로드 실패", err);
    posts.value = []; // 오류 발생 시 빈 배열로 초기화
  }
};

const fetchPopularPosts = async () => {
  console.log("Fetching popular posts");
  try {
    const res = await axios.get("/api/community/posts/", {
      params: { sort: "popular" },
    });
    // API 응답에서 'like_count' 필드를 사용 (num_likes, likes 등은 현재 API 응답에 없음)
    popularPosts.value = res.data.map((post) => ({
      ...post,
      likes_display_count: post.like_count || 0,
    }));
  } catch (err) {
    console.error("인기 게시글 로드 실패", err);
    popularPosts.value = []; // 오류 발생 시 빈 배열로 초기화
  }
};

onMounted(() => {
  // 초기 데이터 로드
  fetchPosts();
  fetchPopularPosts();
});

// CommunityPage로 다시 탐색될 때 (예: 상세 페이지에서 뒤로 가기) 데이터를 새로고침합니다.
// 라우터 설정에서 이 컴포넌트에 해당하는 라우트의 name이 'CommunityPage'라고 가정합니다.
// 이 watch는 컴포넌트가 이미 마운트된 상태에서 라우트가 변경되어 다시 이 페이지로 돌아올 때를 위함입니다.
watch(
  () => route.name,
  (newName, oldName) => {
    console.log(`Route name changed - Old: ${oldName}, New: ${newName}`); // 라우트 변경 로그
    // CommunityPage로 돌아왔을 때 (newName이 'CommunityPage'이고, oldName이 있었던 경우)
    // 또는 CommunityPage 내에서 다른 경로에서 CommunityPage로 이동한 경우 (예: 다른 탭에서 이 페이지로 직접 링크)
    // onMounted는 초기 마운트에만 실행되므로, 페이지 재방문 시 데이터 갱신을 위해 필요합니다.
    // 라우터에 정의된 이름은 'Community' 입니다.
    if (
      newName === "Community" && // 'CommunityPage'에서 'Community'로 수정
      oldName !== undefined &&
      oldName !== null
    ) {
      // oldName이 null이나 undefined가 아닌 경우에만 (즉, 실제 이전 라우트가 있었던 경우)
      console.log(
        `Community page re-entered or specifically navigated to (Old: ${oldName}, New: ${newName}). Fetching data.`
      );
      fetchPosts();
      fetchPopularPosts();
    } else if (
      newName === "Community" && // 'CommunityPage'에서 'Community'로 수정
      (oldName === undefined || oldName === null)
    ) {
      // 이 경우는 거의 onMounted와 동일한 시점이거나, 직접 URL로 CommunityPage에 접근한 경우일 수 있음.
      // onMounted에서 이미 호출하므로, 중복 호출을 피하거나 로직을 통합해야 할 수 있음.
      // 현재는 onMounted에서 처리하므로 이 블록은 사실상 불필요하거나, 특정 엣지 케이스용.
      console.log(
        `CommunityPage initial navigation or direct access (oldName: ${oldName}). Data likely fetched by onMounted.`
      );
    }
  },
  { immediate: false } // 초기 마운트 시에는 onMounted에서 호출하므로 false
);

watch(category, () => {
  // 이 watch는 category ref가 변경될 때만 실행됩니다.
  console.log(`Category changed to: ${category.value}. Fetching posts.`);
  fetchPosts();
  // 카테고리 변경 시 URL 업데이트 (선택적: 브라우저 히스토리 스택 관리)
  // router.push({ query: { category: category.value } }) // 이렇게 하면 히스토리에 남음
  // 현재 방식은 히스토리에 남기지 않고 URL만 변경
  window.history.replaceState(
    null,
    "",
    `/community?category=${category.value}`
  );
});

// 라우트 변경 감지 (CommunityPage로 돌아왔을 때)
// CommunityDetailPage 등에서 CommunityPage로 돌아올 때,
// onMounted가 다시 실행되지 않는 경우를 대비 (예: keep-alive 미사용 및 브라우저 캐시)
// watch(() => route.fullPath, (newPath, oldPath) => {
//   // Community 페이지로 돌아왔는지, 또는 Community 페이지 내에서 이동했는지 등을 판단하여
//   // fetchPosts() 및 fetchPopularPosts() 호출 여부 결정
//   // 예: if (newPath.startsWith('/community') && !oldPath.startsWith('/community/post')) { ... }
//   // 이 방식은 복잡해질 수 있으므로 visibilitychange를 우선 사용
// }, { immediate: false }); // immediate: true로 하면 초기 로드 시에도 실행됨
</script>

<style scoped>
.community-page {
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

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: white;
  margin-bottom: 20px;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 40px;
  line-height: 1.6;
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
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 40px;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 30px;
  position: relative;
  padding-bottom: 10px;
}

.section-title::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

.category-section {
  grid-column: 1 / -1;
  margin-bottom: 30px;
}

.category-tabs {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.category-tab {
  background: white;
  border: 2px solid #e2e8f0;
  color: #64748b;
  padding: 12px 24px;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.category-tab:hover {
  border-color: #667eea;
  color: #667eea;
  transform: translateY(-2px);
}

.category-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.stats-section {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: 800;
  color: #333;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

.posts-section {
  grid-column: 1;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.write-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 24px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.write-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
  color: white;
}

.posts-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.post-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
  border-color: #667eea;
  color: inherit;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.post-meta {
  display: flex;
  gap: 10px;
  align-items: center;
}

.post-id {
  background: #f1f5f9;
  color: #64748b;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.post-category {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.post-author {
  display: flex;
  align-items: center;
}

.author-link {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #666;
  transition: all 0.3s ease;
}

.author-link:hover {
  color: #667eea;
}

.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
}

.author-name {
  font-weight: 500;
  font-size: 0.9rem;
}

.post-content {
  margin-bottom: 20px;
}

.post-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.4;
}

.post-preview {
  color: #666;
  line-height: 1.6;
  font-size: 0.95rem;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #f1f5f9;
}

.post-stats {
  display: flex;
  gap: 15px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #888;
  font-size: 0.85rem;
}

.post-date {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #888;
  font-size: 0.85rem;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  color: #cbd5e1;
  margin-bottom: 20px;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #64748b;
  margin-bottom: 10px;
}

.empty-description {
  color: #94a3b8;
  margin-bottom: 30px;
}

.empty-action-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 30px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.empty-action-btn:hover {
  transform: translateY(-2px);
  color: white;
}

.sidebar {
  grid-column: 2;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.widget {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.widget-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
}

.popular-posts {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.popular-post {
  display: flex;
  gap: 15px;
  align-items: flex-start;
  text-decoration: none; /* Add this to remove underline from RouterLink */
  color: inherit; /* Add this to inherit text color */
}

.popular-post:hover .popular-title {
  color: #667eea; /* Optional: Add hover effect for title */
}

.popular-rank {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
  flex-shrink: 0;
}

.popular-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
  line-height: 1.3;
  transition: color 0.3s ease; /* Optional: Smooth transition for hover effect */
}

.popular-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: #888;
}

.popular-views {
  display: flex;
  align-items: center;
  gap: 3px;
}

.empty-popular-posts p {
  color: #666;
  text-align: center;
  font-style: italic;
}

.community-rules {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rule-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  color: #666;
}

.rule-item i {
  color: #10b981;
}

.trending-widget {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.trending-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: rgba(255, 255, 255, 0.8);
  color: #8b4513;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .content-wrapper {
    grid-template-columns: 1fr;
    padding: 20px;
  }

  .category-tabs {
    justify-content: center;
  }

  .stats-section {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    gap: 20px;
    align-items: stretch;
  }

  .posts-section {
    grid-column: 1;
  }

  .sidebar {
    grid-column: 1;
  }
}
</style>
