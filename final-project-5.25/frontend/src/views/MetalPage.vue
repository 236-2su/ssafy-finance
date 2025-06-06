<template>
  <div class="metal-page">
    <div class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">귀금속 시세</h1>
          <p class="hero-subtitle">실시간 금·은 가격 변동을 확인하세요</p>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="content-wrapper">
        <!-- 현재 가격 카드 (기존과 동일) -->
        <div class="price-cards">
          <div class="price-card gold-card">
            <div class="price-header">
              <div class="metal-icon">
                <i class="fas fa-coins"></i>
              </div>
              <div class="metal-info">
                <h3 class="metal-name">금 (Gold)</h3>
                <p class="metal-unit">1온스당 (USD)</p>
              </div>
            </div>
            <div class="price-display">
              <div class="current-price">$2,048.50</div>
              <div class="price-change positive">
                <i class="fas fa-arrow-up"></i>
                +$12.30 (+0.6%)
              </div>
            </div>
            <div class="price-footer">
              <span class="last-update">최종 업데이트: 2시간 전</span>
            </div>
          </div>

          <div class="price-card silver-card">
            <div class="price-header">
              <div class="metal-icon">
                <i class="fas fa-medal"></i>
              </div>
              <div class="metal-info">
                <h3 class="metal-name">은 (Silver)</h3>
                <p class="metal-unit">1온스당 (USD)</p>
              </div>
            </div>
            <div class="price-display">
              <div class="current-price">$24.85</div>
              <div class="price-change negative">
                <i class="fas fa-arrow-down"></i>
                -$0.45 (-1.8%)
              </div>
            </div>
            <div class="price-footer">
              <span class="last-update">최종 업데이트: 2시간 전</span>
            </div>
          </div>
        </div>

        <!-- 차트 섹션 -->
        <div class="chart-section">
          <div class="chart-header">
            <h2 class="section-title">가격 변동 차트</h2>
            <div class="chart-controls">
              <div class="control-group">
                <label class="control-label">자산 선택</label>
                <select v-model="asset" class="control-select">
                  <option value="gold">금 (Gold)</option>
                  <option value="silver">은 (Silver)</option>
                </select>
              </div>
              <div class="control-group">
                <label class="control-label">시작일</label>
                <input type="date" v-model="startDate" class="control-input" />
              </div>
              <div class="control-group">
                <label class="control-label">종료일</label>
                <input type="date" v-model="endDate" class="control-input" />
              </div>
            </div>
          </div>

          <div class="chart-container">
            <div v-if="loading" class="loading-container">
              <div class="loading-spinner"></div>
              <p class="loading-text">차트 데이터를 불러오는 중...</p>
            </div>
            <div v-else-if="noData" class="no-data-container">
              <div class="no-data-icon">
                <i class="fas fa-chart-line fa-4x"></i>
              </div>
              <h3 class="no-data-title">데이터가 없습니다</h3>
              <p class="no-data-description">
                선택한 기간에 데이터가 없거나 날짜 형식이 올바르지 않습니다.<br />
                날짜를 확인하거나 다른 기간을 선택해주세요.
              </p>
              <button @click="useSampleData" class="sample-data-btn">
                샘플 차트 보기
              </button>
            </div>
            <div v-else class="chart-wrapper">
              <!-- vue-chartjs 컴포넌트 사용 -->
              <Line
                v-if="chartData.datasets && chartData.datasets.length > 0"
                :data="chartData"
                :options="chartOptions"
              />
            </div>
          </div>
        </div>

        <!-- 사이드바 (기존과 동일) -->
        <div class="sidebar">
          <div class="widget period-widget">
            <h4 class="widget-title">빠른 기간 선택</h4>
            <div class="period-buttons">
              <button @click="setQuickPeriod('1M')" class="period-btn">
                1개월
              </button>
              <button @click="setQuickPeriod('3M')" class="period-btn">
                3개월
              </button>
              <button @click="setQuickPeriod('6M')" class="period-btn">
                6개월
              </button>
              <button @click="setQuickPeriod('1Y')" class="period-btn">
                1년
              </button>
              <button @click="setQuickPeriod('YTD')" class="period-btn">
                연초대비
              </button>
            </div>
          </div>
          <div class="widget market-info-widget">
            <h4 class="widget-title">시장 정보</h4>
            <div class="market-stats">
              <div class="stat-item">
                <div class="stat-label">거래량</div>
                <div class="stat-value">1.2M oz</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">52주 최고</div>
                <div class="stat-value">$2,135.40</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">52주 최저</div>
                <div class="stat-value">$1,810.20</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">시가총액</div>
                <div class="stat-value">$12.8T</div>
              </div>
            </div>
          </div>
          <div class="widget tips-widget">
            <h4 class="widget-title">투자 팁</h4>
            <div class="tips-list">
              <div class="tip-item">
                <i class="fas fa-lightbulb"></i
                ><span>귀금속은 인플레이션 헤지 수단으로 활용됩니다</span>
              </div>
              <div class="tip-item">
                <i class="fas fa-lightbulb"></i
                ><span>달러 약세 시 금 가격이 상승하는 경향이 있습니다</span>
              </div>
              <div class="tip-item">
                <i class="fas fa-lightbulb"></i
                ><span
                  >지정학적 리스크 증가 시 안전자산 선호도가 높아집니다</span
                >
              </div>
              <div class="tip-item">
                <i class="fas fa-lightbulb"></i
                ><span>중앙은행의 금리 정책을 주의 깊게 관찰하세요</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from "vue";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler, // Filler 플러그인 추가 (영역 채우기용)
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler
);

export default {
  name: "MetalPage",
  components: {
    Line,
  },
  setup() {
    const asset = ref("gold");
    const startDate = ref("");
    const endDate = ref("");
    const noData = ref(false);
    const loading = ref(false);

    const chartLabels = ref([]);
    const chartPrices = ref([]);

    // vue-chartjs를 위한 chartData computed property
    const chartData = computed(() => ({
      labels: chartLabels.value,
      datasets: [
        {
          label: asset.value === "gold" ? "금 가격 (USD)" : "은 가격 (USD)",
          data: chartPrices.value,
          fill: true,
          backgroundColor:
            asset.value === "gold"
              ? "rgba(255, 193, 7, 0.1)"
              : "rgba(108, 117, 125, 0.1)",
          borderColor: asset.value === "gold" ? "#ffc107" : "#6c757d",
          borderWidth: 2, // 선 굵기 조정
          pointBackgroundColor: asset.value === "gold" ? "#ffc107" : "#6c757d",
          pointBorderColor: "#fff",
          pointBorderWidth: 1, // 포인트 테두리 굵기 조정
          pointRadius: 3, // 포인트 크기 조정
          pointHoverRadius: 5, // 호버 시 포인트 크기 조정
          tension: 0.1, // 곡선 부드러움 정도 (0.4는 너무 큼)
        },
      ],
    }));

    // vue-chartjs를 위한 chartOptions ref
    const chartOptions = ref({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          labels: {
            usePointStyle: true,
            padding: 20,
            font: { size: 14, weight: "bold" },
          },
        },
        title: {
          display: true,
          text: computed(() =>
            asset.value === "gold" ? "금 가격 추이" : "은 가격 추이"
          ), // computed로 동적 제목
          font: { size: 18, weight: "bold" },
          padding: { top: 10, bottom: 20 }, // 패딩 조정
        },
        filler: {
          // Filler 플러그인 옵션 (필요한 경우)
          propagate: false,
        },
        tooltip: {
          // 툴팁 설정 (필요한 경우)
          mode: "index",
          intersect: false,
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "날짜",
            font: { size: 14, weight: "bold" },
          },
          grid: { color: "rgba(0,0,0,0.05)" }, // 그리드 색상 연하게
        },
        y: {
          title: {
            display: true,
            text: "가격 (USD)",
            font: { size: 14, weight: "bold" },
          },
          grid: { color: "rgba(0,0,0,0.05)" }, // 그리드 색상 연하게
        },
      },
      interaction: {
        intersect: false,
        mode: "index",
      },
      elements: {
        point: {
          hoverBackgroundColor: "#fff",
          // hoverBorderWidth: 2 // 호버 시 포인트 테두리 (필요시)
        },
      },
    });

    const isValidDateString = (dateString) => {
      if (!dateString) return true;
      const regex = /^\d{4}-\d{2}-\d{2}$/;
      if (!regex.test(dateString)) return false;
      const date = new Date(dateString);
      const timestamp = date.getTime();
      if (typeof timestamp !== "number" || Number.isNaN(timestamp))
        return false;
      return date.toISOString().startsWith(dateString);
    };

    const fetchData = async () => {
      if (
        !isValidDateString(startDate.value) ||
        !isValidDateString(endDate.value)
      ) {
        console.warn(
          "날짜 형식이 올바르지 않습니다. (YYYY-MM-DD). API 호출을 중단합니다."
        );
        noData.value = true;
        loading.value = false;
        chartLabels.value = []; // 데이터 초기화
        chartPrices.value = []; // 데이터 초기화
        return;
      }
      if (
        startDate.value &&
        endDate.value &&
        new Date(startDate.value) > new Date(endDate.value)
      ) {
        console.warn("시작일이 종료일보다 늦습니다. API 호출을 중단합니다.");
        noData.value = true;
        loading.value = false;
        chartLabels.value = []; // 데이터 초기화
        chartPrices.value = []; // 데이터 초기화
        return;
      }

      loading.value = true;
      noData.value = false;

      try {
        let url = `/api/commodities/prices/?asset=${asset.value}`;
        if (startDate.value) url += `&start_date=${startDate.value}`;
        if (endDate.value) url += `&end_date=${endDate.value}`;

        const res = await fetch(url);
        const apiData = await res.json(); // .text() 대신 .json() 사용

        if (!res.ok) {
          console.error(
            "🚨 API 에러:",
            res.status,
            apiData.error || apiData.detail || "알 수 없는 에러"
          );
          noData.value = true;
          chartLabels.value = [];
          chartPrices.value = [];
          loading.value = false;
          return;
        }

        const data = apiData.data;
        if (!data || !data.length) {
          noData.value = true;
          chartLabels.value = [];
          chartPrices.value = [];
        } else {
          chartLabels.value = data.map((i) => i.date);
          chartPrices.value = data.map((i) => i.price);
          noData.value = false;
        }
      } catch (err) {
        console.error("🚨 네트워크 에러 또는 JSON 파싱 에러:", err);
        noData.value = true;
        chartLabels.value = [];
        chartPrices.value = [];
      } finally {
        loading.value = false;
      }
    };

    const useSampleData = () => {
      loading.value = true;
      noData.value = false;
      const today = new Date();
      const labels = [];
      const prices = [];
      for (let i = 29; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        labels.push(date.toISOString().split("T")[0]);
        const basePrice = asset.value === "gold" ? 2000 : 25;
        const variation = (Math.random() - 0.5) * (basePrice * 0.1);
        prices.push(parseFloat((basePrice + variation).toFixed(2)));
      }
      chartLabels.value = labels;
      chartPrices.value = prices;
      loading.value = false;
    };

    onMounted(() => {
      const today = new Date();
      endDate.value = today.toISOString().split("T")[0];
      const priorDate = new Date();
      priorDate.setMonth(priorDate.getMonth() - 1);
      startDate.value = priorDate.toISOString().split("T")[0];
      // fetchData는 watch에 의해 즉시 호출됨 (immediate: true)
    });

    watch([asset, startDate, endDate], fetchData, {
      immediate: true,
      deep: true,
    });

    const setQuickPeriod = (period) => {
      const today = new Date();
      endDate.value = today.toISOString().split("T")[0];
      let start;
      const baseDateForStart = new Date();
      switch (period) {
        case "1M":
          baseDateForStart.setMonth(baseDateForStart.getMonth() - 1);
          break;
        case "3M":
          baseDateForStart.setMonth(baseDateForStart.getMonth() - 3);
          break;
        case "6M":
          baseDateForStart.setMonth(baseDateForStart.getMonth() - 6);
          break;
        case "1Y":
          baseDateForStart.setFullYear(baseDateForStart.getFullYear() - 1);
          break;
        case "YTD":
          start = new Date(baseDateForStart.getFullYear(), 0, 1)
            .toISOString()
            .split("T")[0];
          break;
      }
      if (period !== "YTD") {
        start = baseDateForStart.toISOString().split("T")[0];
      }
      startDate.value = start;
    };

    return {
      asset,
      startDate,
      endDate,
      noData,
      loading,
      chartData,
      chartOptions,
      setQuickPeriod,
      useSampleData,
    };
  },
};
</script>

<style scoped>
/* 스타일은 기존과 동일하게 유지 */
.metal-page {
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

.price-cards {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.price-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.price-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.gold-card::before {
  background: linear-gradient(135deg, #ffc107 0%, #ff8f00 100%);
}

.silver-card::before {
  background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
}

.price-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
}

.price-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.metal-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.gold-card .metal-icon {
  background: linear-gradient(135deg, #ffc107 0%, #ff8f00 100%);
}

.silver-card .metal-icon {
  background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
}

.metal-name {
  font-size: 1.3rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.metal-unit {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.price-display {
  margin-bottom: 20px;
}

.current-price {
  font-size: 2.5rem;
  font-weight: 800;
  color: #333;
  margin-bottom: 10px;
}

.price-change {
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 600;
  font-size: 1.1rem;
}

.price-change.positive {
  color: #10b981;
}

.price-change.negative {
  color: #ef4444;
}

.price-footer {
  padding-top: 15px;
  border-top: 1px solid #f1f5f9;
}

.last-update {
  color: #888;
  font-size: 0.85rem;
}

.chart-section {
  grid-column: 1;
}

.chart-header {
  margin-bottom: 30px;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
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

.chart-controls {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.control-label {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.control-select,
.control-input {
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  background: white;
}

.control-select:focus,
.control-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.chart-container {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  min-height: 400px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(102, 126, 234, 0.3);
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-text {
  color: #666;
  font-size: 1.1rem;
}

.no-data-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  text-align: center;
}

.no-data-icon {
  color: #cbd5e1;
  margin-bottom: 20px;
}

.no-data-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #64748b;
  margin-bottom: 10px;
}

.no-data-description {
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 20px;
}

.sample-data-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sample-data-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.chart-wrapper {
  height: 400px;
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

.market-info-widget {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.market-info-widget .widget-title {
  color: white;
}

.market-stats {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

.stat-value {
  font-weight: 700;
  font-size: 1.1rem;
}

.tips-widget {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.tips-widget .widget-title {
  color: white;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.9rem;
  line-height: 1.5;
}

.tip-item i {
  color: #fbbf24;
  margin-top: 2px;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.news-item {
  padding-bottom: 15px;
  border-bottom: 1px solid #f1f5f9;
}

.news-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.news-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
  line-height: 1.4;
}

.news-time {
  color: #888;
  font-size: 0.8rem;
}

.period-widget {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.period-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.period-btn {
  background: rgba(255, 255, 255, 0.8);
  border: none;
  color: #8b4513;
  padding: 10px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.period-btn:hover {
  background: white;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .content-wrapper {
    grid-template-columns: 1fr;
    padding: 20px;
  }

  .price-cards {
    grid-template-columns: 1fr;
  }

  .chart-controls {
    flex-direction: column;
  }

  .chart-section {
    grid-column: 1;
  }

  .sidebar {
    grid-column: 1;
  }

  .period-buttons {
    grid-template-columns: 1fr;
  }
}
</style>
