<template>
  <div class="container">
    <div class="header">
      <h1>예금/적금 상품 목록</h1>
      <div class="filter-buttons">
        <button 
          :class="['filter-btn', { active: selectedFilter === 'all' }]"
          @click="setFilter('all')"
        >
          전체
        </button>
        <button 
          :class="['filter-btn', { active: selectedFilter === '예금' }]"
          @click="setFilter('예금')"
        >
          예금
        </button>
        <button 
          :class="['filter-btn', { active: selectedFilter === '적금' }]"
          @click="setFilter('적금')"
        >
          적금
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>상품 정보를 불러오는 중...</p>
    </div>

    <div v-else-if="filteredProducts.length" class="products-grid">
      <div
        class="product-card"
        v-for="product in filteredProducts"
        :key="product.fin_prdt_cd"
        @click="goDetail(product.fin_prdt_cd)"
      >
        <div class="product-header">
          <div class="product-type" :class="product.product_type">
            {{ product.product_type }}
          </div>
          <div class="bank-name">{{ product.kor_co_nm }}</div>
        </div>
        
        <h3 class="product-name">{{ product.fin_prdt_nm }}</h3>
        
        <div class="product-info">
          <div class="info-item" v-if="product.join_way">
            <span class="label">가입방법:</span>
            <span class="value">{{ product.join_way }}</span>
          </div>
          
          <div class="info-item" v-if="product.join_member">
            <span class="label">가입대상:</span>
            <span class="value">{{ product.join_member }}</span>
          </div>
          
          <div class="special-condition" v-if="product.spcl_cnd">
            <span class="label">우대조건:</span>
            <span class="value">{{ product.spcl_cnd }}</span>
          </div>
        </div>
        
        <div class="card-footer">
          <span class="view-detail">자세히 보기 →</span>
        </div>
      </div>
    </div>

    <div v-else class="no-products">
      <div class="no-products-icon">📊</div>
      <h3>표시할 상품이 없습니다</h3>
      <p>다른 필터를 선택해보세요.</p>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";

const productList = ref([]);
const loading = ref(true);
const selectedFilter = ref('all');
const router = useRouter();

const filteredProducts = computed(() => {
  if (selectedFilter.value === 'all') {
    return productList.value;
  }
  return productList.value.filter(product => product.product_type === selectedFilter.value);
});

const getProducts = async () => {
  try {
    loading.value = true;
    const res = await axios.get(
      "http://127.0.0.1:8000/saving/combined-products/"
    );
    productList.value = res.data.response.result.baseList;
  } catch (err) {
    console.error("상품 조회 실패", err);
  } finally {
    loading.value = false;
  }
};

const setFilter = (filter) => {
  selectedFilter.value = filter;
};

const goDetail = (fin_prdt_cd) => {
  router.push(`/saving/${fin_prdt_cd}`);
};

onMounted(getProducts);
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 30px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.filter-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 20px;
}

.filter-btn {
  padding: 12px 24px;
  border: 2px solid rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.1);
  color: white;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.filter-btn:hover {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
}

.filter-btn.active {
  background: rgba(255,255,255,0.9);
  color: #667eea;
  border-color: white;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: white;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255,255,255,0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
  padding: 20px 0;
}

.product-card {
  background: rgba(255,255,255,0.95);
  border-radius: 20px;
  padding: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(0,0,0,0.2);
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.product-type {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  color: white;
}

.product-type.예금 {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.product-type.적금 {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.bank-name {
  font-size: 0.9rem;
  color: #666;
  font-weight: 600;
}

.product-name {
  font-size: 1.3rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
  line-height: 1.4;
}

.product-info {
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.label {
  font-weight: 600;
  color: #555;
  min-width: 80px;
}

.value {
  color: #333;
  flex: 1;
}

.special-condition {
  margin-top: 12px;
  padding: 12px;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  border-radius: 10px;
  font-size: 0.85rem;
}

.special-condition .label {
  color: #8b4513;
  font-weight: 700;
}

.special-condition .value {
  color: #8b4513;
}

.card-footer {
  text-align: right;
  margin-top: 20px;
}

.view-detail {
  color: #667eea;
  font-weight: 600;
  font-size: 0.9rem;
}

.no-products {
  text-align: center;
  padding: 80px 20px;
  color: white;
}

.no-products-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.no-products h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.no-products p {
  opacity: 0.8;
}

@media (max-width: 768px) {
  .container {
    padding: 15px;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .filter-buttons {
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .filter-btn {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
  
  .products-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .product-card {
    padding: 20px;
  }
}
</style>
