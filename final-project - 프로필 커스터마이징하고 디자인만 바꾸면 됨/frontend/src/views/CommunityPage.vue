<template>
  <div class="container mt-4">
    <h2>커뮤니티 게시판</h2>

    <!-- 카테고리 탭 (생략) -->
    <ul class="nav nav-pills mb-3">
      <li class="nav-item" v-for="(label, cat) in categories" :key="cat">
        <button
          class="nav-link"
          :class="{ active: category === cat }"
          @click="category = cat"
        >
          {{ label }}
        </button>
      </li>
    </ul>

    <!-- 글 목록: 카드 -->
    <div v-if="posts.length">
      <RouterLink
        v-for="post in posts"
        :key="post.id"
        :to="`/community/post/${post.id}`"
        class="card mb-3 text-decoration-none text-dark list-card"
      >
        <div class="card-body">
          <!-- ① ID 와 작성자 -->
          <div class="d-flex justify-content-between align-items-center mb-1">
            <small class="text-muted">#{{ post.id }}</small>
            <small class="text-muted">
              <RouterLink
                :to="`/profile/${post.author}`"
                class="text-decoration-none text-muted"
                @click.stop
              >
                {{ post.author }}
              </RouterLink>
            </small>
          </div>

          <!-- ② 제목 -->
          <h5 class="card-title mb-1">{{ post.title }}</h5>

          <!-- ③ 작성일 -->
          <small class="text-muted">{{ formatDate(post.created_at) }}</small>
        </div>
      </RouterLink>
    </div>
    <p v-else class="text-center">등록된 글이 없습니다.</p>

    <!-- 글쓰기 버튼 -->
    <RouterLink to="/community/write" class="write-btn btn btn-primary">
      ✏️ 글쓰기
    </RouterLink>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const category = ref(route.query.category || "free");
const posts = ref([]);

const categories = {
  free: "자유게시판",
  invest: "투자 이야기",
  bank: "은행/기관 정보",
  qna: "Q&A",
};

// 날짜 포맷
const formatDate = (iso) =>
  new Date(iso).toLocaleString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });

// API 호출
const fetchPosts = async () => {
  try {
    const res = await axios.get("/api/community/posts/", {
      params: { category: category.value },
    });
    posts.value = res.data;
  } catch (err) {
    console.error("게시글 로드 실패", err);
  }
};

const deletePost = async (postId) => {
  try {
    await axios.delete(`/api/community/posts/${postId}/`);
    fetchPosts(); // 게시글 목록 갱신
  } catch (err) {
    console.error("게시글 삭제 실패", err);
  }
};

onMounted(fetchPosts);
watch(category, () => {
  fetchPosts();
  window.history.replaceState(
    null,
    "",
    `/community?category=${category.value}`
  );
});
</script>
