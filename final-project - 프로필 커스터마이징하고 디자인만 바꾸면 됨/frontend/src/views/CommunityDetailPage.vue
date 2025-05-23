<template>
  <div class="container mt-4" v-if="post">
    <!-- 뒤로 가기 -->
    <button class="btn btn-link mb-3" @click="router.back()">← 뒤로</button>

    <!-- 카드 -->
    <div class="card mb-4">
      <div class="card-body">
        <!-- 제목 -->
        <h2 class="card-title mb-2">{{ post.title }}</h2>

        <!-- 메타 정보 -->
        <div class="text-muted mb-3">
          <small class="me-2">#{{ post.id }}</small>
          <small class="me-2">
            작성자:
            <RouterLink
              :to="`/profile/${post.author}`"
              class="text-decoration-none text-muted"
            >
              {{ post.author }}
            </RouterLink>
          </small>
          <small>{{ formatDate(post.created_at) }}</small>
        </div>

        <!-- 본문 -->
        <div class="card-text mb-3" v-html="post.content"></div>

        <!-- 액션 버튼 -->
        <div class="mb-3 d-flex align-items-center">
          <!-- 좋아요 버튼 -->
          <button
            @click="toggleLike"
            class="btn"
            :class="liked ? 'btn-danger me-2' : 'btn-outline-danger me-2'"
          >
            <span v-if="liked">❤️</span>
            <span v-else>🤍</span>
            {{ likeCount }}
          </button>

          <!-- 스크랩 버튼 -->
          <button
            @click="toggleBookmark"
            class="btn"
            :class="
              bookmarked ? 'btn-primary me-2' : 'btn-outline-primary me-2'
            "
          >
            <span v-if="bookmarked">🔖</span>
            <span v-else>📑</span>
            {{ bookmarkCount }}
          </button>

          <!-- 수정/삭제 버튼: 작성자만 우측 정렬 -->
          <div v-if="isAuthor" class="ms-auto d-flex">
            <RouterLink
              :to="`/community/edit/${post.id}`"
              class="btn btn-warning me-2"
            >
              수정
            </RouterLink>
            <button @click="deletePost" class="btn btn-danger">삭제</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 댓글 섹션 -->
    <h3>댓글</h3>
    <div
      v-for="comment in post.comments"
      :key="comment.id"
      class="comment mb-2 d-flex justify-content-between align-items-start"
    >
      <div>
        <strong>{{ comment.author }}:</strong> {{ comment.content }}
      </div>
      <button
        v-if="userStore.isLogin && comment.author === userStore.username"
        @click="deleteComment(comment.id)"
        class="btn btn-sm btn-outline-danger"
      >
        삭제
      </button>
    </div>
    <textarea
      v-model="newComment"
      placeholder="댓글을 입력하세요"
      class="form-control mb-2"
    ></textarea>
    <button @click="submitComment" class="btn btn-primary">댓글 작성</button>
  </div>

  <div v-else class="text-center my-5">로딩중...</div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter, RouterLink } from "vue-router";
import { useUserStore } from "@/stores/user";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const postId = route.params.id;
const post = ref(null);
const newComment = ref("");
const liked = ref(false);
const likeCount = ref(0);
const bookmarked = ref(false);
const bookmarkCount = ref(0);

// 날짜 포맷 헬퍼
const formatDate = (iso) =>
  new Date(iso).toLocaleString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });

// 작성자인지 여부 계산
const isAuthor = computed(
  () => userStore.isLogin && post.value?.author === userStore.username
);

// 게시글 상세 조회
async function fetchPost() {
  try {
    const { data } = await axios.get(`/api/community/posts/${postId}/`);
    post.value = data;
    liked.value = data.liked;
    likeCount.value = data.like_count;
    bookmarked.value = data.bookmarked;
    bookmarkCount.value = data.bookmark_count;
  } catch (err) {
    console.error("상세 로드 실패", err);
    alert("게시글을 불러오는 데 실패했습니다.");
    router.back();
  }
}

// 좋아요 토글
async function toggleLike() {
  if (!userStore.isLogin) {
    alert("로그인 후 이용 가능합니다.");
    return;
  }
  try {
    const { data } = await axios.post(
      `/api/community/posts/${postId}/like/`,
      null,
      { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }
    );
    liked.value = data.liked;
    likeCount.value = data.count;
  } catch (err) {
    console.error("좋아요 처리 실패", err);
  }
}

// 스크랩 토글
async function toggleBookmark() {
  if (!userStore.isLogin) {
    alert("로그인 후 이용 가능합니다.");
    return;
  }
  try {
    const { data } = await axios.post(
      `/api/community/posts/${postId}/bookmark/`,
      null,
      { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }
    );
    bookmarked.value = data.bookmarked;
    bookmarkCount.value = data.count;
  } catch (err) {
    console.error("스크랩 처리 실패", err);
  }
}

// 댓글 작성
async function submitComment() {
  if (!newComment.value.trim()) return;
  try {
    await axios.post(
      `/api/community/posts/${postId}/comments/`,
      { content: newComment.value },
      { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }
    );
    newComment.value = "";
    fetchPost();
  } catch (err) {
    console.error("댓글 작성 실패", err);
  }
}

// 댓글 삭제
async function deleteComment(commentId) {
  if (!confirm("정말로 이 댓글을 삭제하시겠습니까?")) return;
  try {
    await axios.delete(
      `/api/community/posts/${postId}/comments/${commentId}/`,
      { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }
    );
    fetchPost();
  } catch (err) {
    console.error("댓글 삭제 실패", err);
    alert("댓글 삭제에 실패했습니다.");
  }
}

// 게시글 삭제
async function deletePost() {
  if (!confirm("정말로 게시글을 삭제하시겠습니까?")) return;
  try {
    await axios.delete(`/api/community/posts/${postId}/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    });
    alert("삭제되었습니다.");
    router.push({
      path: "/community",
      query: { category: post.value.category },
    });
  } catch (err) {
    console.error("삭제 실패", err);
    alert("삭제에 실패했습니다.");
  }
}

onMounted(fetchPost);
</script>

<style scoped>
.container {
  max-width: 700px;
}
.me-2 {
  margin-right: 0.5rem;
}
.comment {
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
}
</style>
