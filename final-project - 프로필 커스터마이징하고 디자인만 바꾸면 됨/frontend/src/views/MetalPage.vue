<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">금·은 가격 변동 차트</h2>

    <div class="flex flex-wrap gap-4 mb-6">
      <!-- 자산 선택 -->
      <div>
        <label class="block font-semibold mb-1">자산 선택</label>
        <select v-model="asset" @change="fetchData" class="border p-2 rounded">
          <option value="gold">금 (Gold)</option>
          <option value="silver">은 (Silver)</option>
        </select>
      </div>
      <!-- 시작일 -->
      <div>
        <label class="block font-semibold mb-1">시작일</label>
        <input
          type="date"
          v-model="startDate"
          @change="fetchData"
          class="border p-2 rounded"
        />
      </div>
      <!-- 종료일 -->
      <div>
        <label class="block font-semibold mb-1">종료일</label>
        <input
          type="date"
          v-model="endDate"
          @change="fetchData"
          class="border p-2 rounded"
        />
      </div>
    </div>

    <div v-if="noData" class="text-red-500 font-semibold">
      선택한 기간에 데이터가 없습니다. (최대 2024년까지 제공)
    </div>

    <canvas v-else ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch, nextTick } from "vue";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  name: "MetalPage",
  setup() {
    const asset = ref("gold");
    const startDate = ref("");
    const endDate = ref("");
    const chart = ref(null);
    const chartCanvas = ref(null);
    const noData = ref(false);

    const fetchData = async () => {
      try {
        let url = `/api/commodities/prices/?asset=${asset.value}`;
        if (startDate.value) url += `&start_date=${startDate.value}`;
        if (endDate.value) url += `&end_date=${endDate.value}`;

        const res = await fetch(url);
        const text = await res.text();
        let json;
        try {
          json = JSON.parse(text);
        } catch {
          console.error("🚨 JSON 파싱 실패:", text);
          return;
        }
        if (!res.ok) {
          console.error("🚨 API 에러:", json.error);
          return;
        }

        const data = json.data;
        if (!data.length) {
          if (chart.value) {
            chart.value.destroy();
            chart.value = null;
          }
          noData.value = true;
          return;
        }
        noData.value = false;

        const labels = data.map((i) => i.date);
        const prices = data.map((i) => i.price);
        await nextTick();
        renderChart(labels, prices);
      } catch (err) {
        console.error("🚨 네트워크 에러:", err);
      }
    };

    const renderChart = (labels, dataPoints) => {
      // ▶️ 캔버스 요소 자체를 넘김
      const canvasEl = chartCanvas.value;
      if (chart.value) chart.value.destroy();
      chart.value = new Chart(canvasEl, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: asset.value === "gold" ? "Gold Price" : "Silver Price",
              data: dataPoints,
              fill: false,
              borderWidth: 2,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "top" },
            title: {
              display: true,
              text: asset.value === "gold" ? "금 가격 추이" : "은 가격 추이",
            },
          },
          scales: {
            x: { title: { display: true, text: "날짜" } },
            y: { title: { display: true, text: "가격 (USD)" } },
          },
        },
      });
    };

    onMounted(fetchData);
    watch([asset, startDate, endDate], fetchData);

    return { asset, startDate, endDate, chartCanvas, noData };
  },
};
</script>
