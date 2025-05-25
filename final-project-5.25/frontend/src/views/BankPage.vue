<template>
  <div class="bank-page">
    <div class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">은행 찾기</h1>
          <p class="hero-subtitle">가까운 은행과 ATM을 쉽고 빠르게 찾아보세요</p>
        </div>
      </div>
    </div>

    <div class="bank-finder-container">
      <!-- 검색 사이드바 -->
      <aside class="search-sidebar">
        <div class="search-header">
          <h3 class="search-title">
            <i class="fas fa-map-marker-alt"></i>
            위치 및 은행 선택
          </h3>
        </div>

        <div class="search-form">
          <div class="form-group">
            <label class="form-label">
              <i class="fas fa-map"></i>
              시/도
            </label>
            <div class="select-wrapper">
              <select v-model="sido" @change="onSidoChange" class="form-select">
                <option value="">시/도를 선택하세요</option>
                <option v-for="r in mapInfo" :key="r.name" :value="r.name">
                  {{ r.name }}
                </option>
              </select>
              <i class="fas fa-chevron-down select-arrow"></i>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">
              <i class="fas fa-building"></i>
              시/군/구
            </label>
            <div class="select-wrapper">
              <select v-model="sigungu" class="form-select" :disabled="!sido">
                <option value="">시/군/구를 선택하세요</option>
                <option v-for="g in guList" :key="g" :value="g">{{ g }}</option>
              </select>
              <i class="fas fa-chevron-down select-arrow"></i>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">
              <i class="fas fa-university"></i>
              은행명
            </label>
            <div class="select-wrapper">
              <select v-model="bankName" class="form-select">
                <option value="">은행을 선택하세요</option>
                <option v-for="b in bankInfo" :key="b" :value="b">{{ b }}</option>
              </select>
              <i class="fas fa-chevron-down select-arrow"></i>
            </div>
          </div>

          <button 
            class="search-btn" 
            @click="searchBanks"
            :disabled="!sido || !sigungu || !bankName"
          >
            <i class="fas fa-search"></i>
            은행 검색
          </button>
        </div>

        <!-- 검색 결과 정보 -->
        <div v-if="searchResults.length > 0" class="search-results-info">
          <div class="results-header">
            <h4 class="results-title">
              <i class="fas fa-list"></i>
              검색 결과 ({{ searchResults.length }}개)
            </h4>
          </div>
          <div class="results-list">
            <div 
              v-for="(result, index) in searchResults" 
              :key="index"
              class="result-item"
              @click="focusOnMarker(index)"
            >
              <div class="result-icon">
                <i class="fas fa-map-pin"></i>
              </div>
              <div class="result-info">
                <h5 class="result-name">{{ result.place_name }}</h5>
                <p class="result-address">{{ result.address_name }}</p>
                <p class="result-phone" v-if="result.phone">
                  <i class="fas fa-phone"></i>
                  {{ result.phone }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- 인기 은행 -->
        <div class="popular-banks">
          <h4 class="popular-title">
            <i class="fas fa-star"></i>
            인기 은행
          </h4>
          <div class="bank-tags">
            <button 
              v-for="bank in popularBanks" 
              :key="bank"
              @click="selectBank(bank)"
              class="bank-tag"
            >
              {{ bank }}
            </button>
          </div>
        </div>
      </aside>

      <!-- 지도 영역 -->
      <div class="map-container">
        <div v-if="!kakaoLoaded" class="map-loading">
          <div class="loading-spinner"></div>
          <p class="loading-text">지도를 불러오는 중...</p>
        </div>
        <div id="map" class="map-view"></div>
        
        <!-- 지도 컨트롤 -->
        <div class="map-controls">
          <button @click="resetMapView" class="control-btn" title="지도 초기화">
            <i class="fas fa-home"></i>
          </button>
          <button @click="getCurrentLocation" class="control-btn" title="현재 위치">
            <i class="fas fa-crosshairs"></i>
          </button>
        </div>
      </div>
    </div>
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
const searchResults = ref([]);

// 인기 은행 목록
const popularBanks = ["국민은행", "신한은행", "우리은행", "하나은행", "농협은행", "기업은행"];

// 지도 로딩 상태
const kakaoLoaded = ref(false);
let map;
const markers = [];
const infoWindows = [];

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

// 인기 은행 선택
function selectBank(bank) {
  bankName.value = bank;
}

// 은행 검색
function searchBanks() {
  if (!kakaoLoaded.value) {
    alert("지도 준비 중입니다. 잠시만 기다려주세요.");
    return;
  }
  if (!sido.value || !sigungu.value || !bankName.value) {
    alert("모든 항목을 선택해주세요.");
    return;
  }

  const ps = new kakao.maps.services.Places();
  
  // 기존 마커와 정보창 제거
  clearMarkers();
  searchResults.value = [];

  const keyword = `${sido.value} ${sigungu.value} ${bankName.value}`;
  
  ps.keywordSearch(keyword, (places, status) => {
    if (status !== kakao.maps.services.Status.OK) {
      alert("검색 결과가 없습니다.");
      return;
    }
    
    searchResults.value = places;
    const bounds = new kakao.maps.LatLngBounds();
    
    places.forEach((place, index) => {
      const pos = new kakao.maps.LatLng(place.y, place.x);
      bounds.extend(pos);
      
      // 마커 생성
      const marker = new kakao.maps.Marker({ 
        map, 
        position: pos,
        title: place.place_name
      });
      
      // 정보창 생성
      const infoWindow = new kakao.maps.InfoWindow({
        content: createInfoWindowContent(place),
        removable: true
      });
      
      markers.push(marker);
      infoWindows.push(infoWindow);
      
      // 마커 클릭 이벤트
      kakao.maps.event.addListener(marker, "click", () => {
        // 다른 정보창 닫기
        infoWindows.forEach(iw => iw.close());
        infoWindow.open(map, marker);
      });
    });
    
    map.setBounds(bounds);
  });
}

// 정보창 내용 생성
function createInfoWindowContent(place) {
  return `
    <div style="padding: 15px; min-width: 200px; font-family: 'Pretendard', sans-serif;">
      <h5 style="margin: 0 0 8px 0; color: #333; font-weight: 600;">${place.place_name}</h5>
      <p style="margin: 0 0 5px 0; color: #666; font-size: 0.9rem;">${place.address_name}</p>
      ${place.phone ? `<p style="margin: 0; color: #667eea; font-size: 0.85rem;"><i class="fas fa-phone"></i> ${place.phone}</p>` : ''}
    </div>
  `;
}

// 마커에 포커스
function focusOnMarker(index) {
  if (markers[index]) {
    const marker = markers[index];
    const position = marker.getPosition();
    
    map.setCenter(position);
    map.setLevel(3);
    
    // 정보창 열기
    infoWindows.forEach(iw => iw.close());
    infoWindows[index].open(map, marker);
  }
}

// 마커 및 정보창 제거
function clearMarkers() {
  markers.forEach(marker => marker.setMap(null));
  infoWindows.forEach(infoWindow => infoWindow.close());
  markers.length = 0;
  infoWindows.length = 0;
}

// 지도 초기화
function resetMapView() {
  if (map) {
    map.setCenter(new kakao.maps.LatLng(37.5665, 126.978));
    map.setLevel(4);
    clearMarkers();
    searchResults.value = [];
  }
}

// 현재 위치 가져오기
function getCurrentLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        const currentPos = new kakao.maps.LatLng(lat, lng);
        
        map.setCenter(currentPos);
        map.setLevel(3);
        
        // 현재 위치 마커 추가
        const currentMarker = new kakao.maps.Marker({
          position: currentPos,
          map: map
        });
        
        const infoWindow = new kakao.maps.InfoWindow({
          content: '<div style="padding:10px; font-weight:600; color:#667eea;">현재 위치</div>'
        });
        
        infoWindow.open(map, currentMarker);
      },
      (error) => {
        alert("현재 위치를 가져올 수 없습니다.");
      }
    );
  } else {
    alert("이 브라우저에서는 위치 서비스를 지원하지 않습니다.");
  }
}
</script>

<style scoped>
.bank-page {
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
  text-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.hero-subtitle {
  font-size: 1.2rem;
  color: rgba(255,255,255,0.9);
  margin-bottom: 40px;
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.bank-finder-container {
  display: flex;
  height: calc(100vh - 200px);
  background: rgba(255,255,255,0.95);
  border-radius: 30px 30px 0 0;
  margin-top: -20px;
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.search-sidebar {
  width: 400px;
  background: white;
  padding: 30px;
  overflow-y: auto;
  border-right: 1px solid #e2e8f0;
  box-shadow: 2px 0 10px rgba(0,0,0,0.05);
}

.search-header {
  margin-bottom: 30px;
}

.search-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #333;
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-title i {
  color: #667eea;
}

.search-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.form-label i {
  color: #667eea;
  width: 16px;
}

.select-wrapper {
  position: relative;
}

.form-select {
  width: 100%;
  padding: 12px 40px 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.9rem;
  background: white;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
  appearance: none;
}

.form-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-select:disabled {
  background: #f8fafc;
  color: #94a3b8;
  cursor: not-allowed;
}

.select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  pointer-events: none;
  font-size: 0.8rem;
}

.search-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 15px 20px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.search-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.search-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.search-results-info {
  margin-bottom: 30px;
  border-top: 1px solid #e2e8f0;
  padding-top: 20px;
}

.results-header {
  margin-bottom: 15px;
}

.results-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.results-title i {
  color: #10b981;
}

.results-list {
  max-height: 300px;
  overflow-y: auto;
}

.result-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.result-item:hover {
  background: rgba(102, 126, 234, 0.05);
  border-color: rgba(102, 126, 234, 0.2);
}

.result-icon {
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  flex-shrink: 0;
}

.result-info {
  flex: 1;
}

.result-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.result-address {
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 4px;
}

.result-phone {
  font-size: 0.8rem;
  color: #667eea;
  display: flex;
  align-items: center;
  gap: 4px;
}

.popular-banks {
  border-top: 1px solid #e2e8f0;
  padding-top: 20px;
}

.popular-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.popular-title i {
  color: #fbbf24;
}

.bank-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.bank-tag {
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  color: #667eea;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.bank-tag:hover {
  background: #667eea;
  color: white;
  transform: translateY(-1px);
}

.map-container {
  flex: 1;
  position: relative;
  background: #f8fafc;
}

.map-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: white;
  z-index: 10;
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: #64748b;
  font-size: 1.1rem;
}

.map-view {
  width: 100%;
  height: 100%;
}

.map-controls {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 5;
}

.control-btn {
  width: 40px;
  height: 40px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  color: #64748b;
}

.control-btn:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .bank-finder-container {
    flex-direction: column;
    height: auto;
    min-height: calc(100vh - 200px);
  }
  
  .search-sidebar {
    width: 100%;
    max-height: 400px;
  }
  
  .map-container {
    height: 400px;
  }
  
  .map-controls {
    top: 10px;
    right: 10px;
  }
  
  .control-btn {
    width: 35px;
    height: 35px;
  }
}
</style>
