<template>
  <div class="container my-4">
    <h3 class="mb-4">글 수정</h3>

    <!-- 카테고리 선택 -->
    <div class="d-flex gap-3 mb-3">
      <select v-model="category" class="form-select w-auto">
        <option value="free">자유게시판</option>
        <option value="invest">투자 이야기</option>
        <option value="bank">은행/기관 정보</option>
        <option value="qna">Q&A</option>
      </select>
    </div>

    <!-- 제목 -->
    <input
      v-model="title"
      type="text"
      class="form-control mb-3"
      placeholder="제목을 입력해 주세요."
    />

    <!-- 안내문 -->
    <div class="alert alert-light small mb-3" role="alert">
      &lt;안내사항&gt;<br />
      - 규정을 준수해 주세요.<br />
      - 광고성, 중복 게시물 금지 등.
    </div>

    <!-- 본문 -->
    <textarea
      v-model="content"
      class="form-control mb-4"
      rows="10"
      placeholder="내용을 입력하세요."
    ></textarea>

    <!-- 제출 버튼 -->
    <div class="text-end">
      <button class="btn btn-secondary me-2" @click="router.back()">
        취소
      </button>
      <button class="btn btn-primary" @click="submit">
        수정하기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useUserStore } from "@/stores/user";
import axios from "axios";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const postId = route.params.id;

// form 필드
const category = ref("free");
const title = ref("");
const content = ref("");

// 기존 게시글 데이터 불러오기
onMounted(async () => {
  // 인증 체크
  const isAuthenticated = await userStore.checkAuthAndRedirect(router);
  if (!isAuthenticated) {
    return;
  }

  try {
    const { data } = await axios.get(`/api/community/posts/${postId}/`);
    
    // 작성자 확인
    if (data.author !== userStore.username) {
      alert("수정 권한이 없습니다.");
      router.back();
      return;
    }
    
    category.value = data.category;
    title.value = data.title;
    content.value = data.content;
  } catch (err) {
    console.error("글 불러오기 실패", err);
    alert("게시글을 불러오는 데 실패했습니다.");
    router.back();
  }
});

// submit 핸들러
const submit = async () => {
  if (!title.value.trim()) {
    alert("제목을 입력해 주세요.");
    return;
  }
  if (!content.value.trim()) {
    alert("내용을 입력해 주세요.");
    return;
  }

  try {
    await axios.patch(`/api/community/posts/${postId}/`, {
      category: category.value,
      title: title.value,
      content: content.value,
    });
    alert("글이 수정되었습니다!");
    // 수정 완료 후 상세 페이지로 이동
    router.push({ name: 'CommunityDetail', params: { id: postId } });
  } catch (err) {
    console.error("수정 실패", err);
    alert("수정에 실패했습니다.");
  }
};
</script>
