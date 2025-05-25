<template>
  <div class="container my-4">
    <h3 class="mb-4">{{ isEdit ? "글 수정" : "글쓰기" }}</h3>

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
      <button class="btn btn-primary" @click="submit">
        {{ isEdit ? "수정하기" : "등록" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";

const router = useRouter();
const route = useRoute();

// query.id 가 문자열로 넘어오니 숫자 변환, 없으면 null
const postId = route.query.id ? Number(route.query.id) : null;
const isEdit = computed(() => postId !== null);

// form 필드
const category = ref(route.query.category || "free");
const title = ref(route.query.title || "");
const content = ref(route.query.content || "");

// 수정 모드로 진입했다면, 백엔드에서 최신 데이터를 불러와 덮어씌우기
onMounted(async () => {
  if (!isEdit.value) return;

  try {
    const { data } = await axios.get(`/api/community/posts/${postId}/`);
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
    if (isEdit.value) {
      // 수정: PATCH 또는 PUT
      await axios.patch(`/api/community/posts/${postId}/`, {
        category: category.value,
        title: title.value,
        content: content.value,
      });
      alert("글이 수정되었습니다!");
    } else {
      // 생성
      await axios.post("/api/community/posts/", {
        category: category.value,
        title: title.value,
        content: content.value,
      });
      alert("글이 등록되었습니다!");
    }
    // 완료 후 해당 카테고리 목록으로 돌아가기
    router.push({ path: "/community", query: { category: category.value } });
  } catch (err) {
    console.error("저장 실패", err);
    alert("저장에 실패했습니다.");
  }
};
</script>
