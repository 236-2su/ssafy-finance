<template>
  <div class="container mt-4">
    <!-- ✅ Bootstrap Carousel (이미지는 나중에 삽입) -->
    <div id="carouselExample" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div class="carousel-item active">
          <div
            class="d-flex justify-content-center align-items-center bg-light"
            style="height: 300px"
          >
            <h3 class="text-secondary">Carousel 이미지 1</h3>
          </div>
        </div>
        <div class="carousel-item">
          <div
            class="d-flex justify-content-center align-items-center bg-light"
            style="height: 300px"
          >
            <h3 class="text-secondary">Carousel 이미지 2</h3>
          </div>
        </div>
        <div class="carousel-item">
          <div
            class="d-flex justify-content-center align-items-center bg-light"
            style="height: 300px"
          >
            <h3 class="text-secondary">Carousel 이미지 3</h3>
          </div>
        </div>
      </div>

      <!-- ✅ Carousel Controls -->
      <button
        class="carousel-control-prev"
        type="button"
        data-bs-target="#carouselExample"
        data-bs-slide="prev"
      >
        <span class="carousel-control-prev-icon"></span>
      </button>
      <button
        class="carousel-control-next"
        type="button"
        data-bs-target="#carouselExample"
        data-bs-slide="next"
      >
        <span class="carousel-control-next-icon"></span>
      </button>
    </div>
  </div>
</template>

<script setup>
// 특별한 JS 없음
</script>
