<!-- BankPage.vue -->
<template>
  <!-- 네비바 높이(56px) 제외 전체 높이 설정 -->
  <div class="d-flex" style="height: calc(100vh - 56px)">
    <!-- 사이드바 -->
    <aside class="w-25 p-4 bg-light overflow-auto">
      <div class="mb-3">
        <label class="form-label">시/도</label>
        <select v-model="sido" @change="onSidoChange" class="form-select">
          <option value="">선택</option>
          <option v-for="r in mapInfo" :key="r.name" :value="r.name">
            {{ r.name }}
          </option>
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label">시/군/구</label>
        <select v-model="sigungu" class="form-select">
          <option value="">선택</option>
          <option v-for="g in guList" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label">은행명</label>
        <select v-model="bankName" class="form-select">
          <option value="">선택</option>
          <option v-for="b in bankInfo" :key="b" :value="b">{{ b }}</option>
        </select>
      </div>
      <button class="btn btn-primary w-100" @click="searchBanks">검색</button>
    </aside>

    <!-- 지도 영역 -->
    <div id="map" class="flex-grow-1"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import data from "@/data.json";

// 환경변수
const KAKAO_MAP_KEY = import.meta.env.VITE_KAKAO_MAP_KEY;

// 지역 & 은행 목록
const mapInfo = data.mapInfo;
const bankInfo = data.bankInfo;
const guList = ref([]);
const sido = ref("");
const sigungu = ref("");
const bankName = ref("");

// 지도 로딩 상태
const kakaoLoaded = ref(false);
let map;
const markers = [];

onMounted(() => {
  // Kakao Maps SDK 로드 (autoload=false 필수)
  const script = document.createElement("script");
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_MAP_KEY}&libraries=services&autoload=false`;
  script.onload = () => {
    // SDK 로드 후, 내부 모듈 로드
    kakao.maps.load(() => {
      map = new kakao.maps.Map(document.getElementById("map"), {
        center: new kakao.maps.LatLng(37.5665, 126.978),
        level: 4,
      });
      kakaoLoaded.value = true;
    });
  };
  document.head.appendChild(script);
});

// 시/도 변경 시
function onSidoChange() {
  const region = mapInfo.find((r) => r.name === sido.value);
  guList.value = region ? region.countries : [];
  sigungu.value = "";
}

// 은행 검색
function searchBanks() {
  if (!kakaoLoaded.value)
    return alert("지도 준비 중입니다. 잠시만 기다려주세요.");
  if (!sido.value || !sigungu.value || !bankName.value) {
    return alert("모든 항목을 선택해주세요.");
  }

  const ps = new kakao.maps.services.Places();
  // 기존 마커 제거
  markers.forEach((m) => m.setMap(null));
  markers.length = 0;

  const keyword = `${sido.value} ${sigungu.value} ${bankName.value}`;
  ps.keywordSearch(keyword, (places, status) => {
    if (status !== kakao.maps.services.Status.OK) {
      return alert("검색 결과가 없습니다.");
    }
    const bounds = new kakao.maps.LatLngBounds();
    places.forEach((place) => {
      const pos = new kakao.maps.LatLng(place.y, place.x);
      bounds.extend(pos);
      const marker = new kakao.maps.Marker({ map, position: pos });
      markers.push(marker);
      kakao.maps.event.addListener(marker, "click", () => {
        new kakao.maps.InfoWindow({
          content: `<div style="padding:5px;">${place.place_name}</div>`,
        }).open(map, marker);
      });
    });
    map.setBounds(bounds);
  });
}
</script>

<style scoped>
#map,
.flex-grow-1 {
  width: 100%;
  height: 100%;
}
.d-flex {
  box-sizing: border-box;
}
</style>
