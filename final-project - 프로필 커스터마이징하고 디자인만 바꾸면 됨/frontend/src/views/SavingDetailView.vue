<template>
  <div class="container" v-if="productDetail && optionList.length">
    <h1>{{ productDetail.fin_prdt_nm }}</h1>
    <p>은행: {{ productDetail.kor_co_nm }}</p>
    <p>가입 방법: {{ productDetail.join_way }}</p>
    <p>가입 대상: {{ productDetail.join_member }}</p>

    <h2>금리 옵션</h2>
    <ul>
      <li v-for="opt in optionList" :key="opt.id">
        {{ opt.save_trm }}개월 - 기본 {{ opt.intr_rate ?? "N/A" }}%, 최고
        {{ opt.intr_rate2 ?? "N/A" }}%
      </li>
    </ul>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const fin_prdt_cd = route.params.fin_prdt_cd;
const productDetail = ref(null);
const optionList = ref([]);

const fetchSavingDetail = async () => {
  try {
    const res = await axios.get(
      `http://127.0.0.1:8000/saving/saving-products-options/${fin_prdt_cd}/`
    );
    optionList.value = res.data;

    const product_id = res.data[0]?.product;
    const productRes = await axios.get(
      `http://127.0.0.1:8000/saving/saving-products-detail/${fin_prdt_cd}/`
    );
    productDetail.value = productRes.data;
  } catch (err) {
    console.error("상세조회 실패", err);
  }
};

onMounted(fetchSavingDetail);
</script>

<style scoped>
.container {
  padding: 20px;
}
</style>
