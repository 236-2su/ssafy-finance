<template>
  <div class="container">
    <h1>적금 상품 목록</h1>
    <div v-if="savingList.length">
      <div
        class="product-card"
        v-for="product in savingList"
        :key="product.fin_prdt_cd"
        @click="goDetail(product.fin_prdt_cd)"
      >
        <h3>{{ product.fin_prdt_nm }}</h3>
        <p>은행명: {{ product.kor_co_nm }}</p>
      </div>
    </div>
    <div v-else>로딩 중...</div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const savingList = ref([]);
const router = useRouter();

const getSavings = async () => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:8000/saving/saving-products/"
    );
    savingList.value = res.data.response.result.baseList;
  } catch (err) {
    console.error("조회 실패", err);
  }
};

const goDetail = (fin_prdt_cd) => {
  router.push(`/saving/${fin_prdt_cd}`);
};

onMounted(getSavings);
</script>

<style scoped>
.container {
  padding: 20px;
}
.product-card {
  border: 1px solid #ccc;
  margin-bottom: 12px;
  padding: 10px;
  cursor: pointer;
  border-radius: 8px;
  transition: 0.3s;
}
.product-card:hover {
  background-color: #f2f2f2;
}
</style>
