// src/stores/youtube.js
import { defineStore } from "pinia";
import { ref } from "vue";

// localStorage 키
const VIDEOS_KEY = "savedVideos";
const CHANNELS_KEY = "savedChannels";

export const useYouTubeStore = defineStore("youtube", () => {
  // 초기값은 localStorage 에서
  const savedVideos = ref(JSON.parse(localStorage.getItem(VIDEOS_KEY) || "[]"));
  const savedChannels = ref(
    JSON.parse(localStorage.getItem(CHANNELS_KEY) || "[]")
  );

  // 토글 액션
  function toggleVideo(id) {
    const i = savedVideos.value.indexOf(id);
    if (i > -1) savedVideos.value.splice(i, 1);
    else savedVideos.value.push(id);
    localStorage.setItem(VIDEOS_KEY, JSON.stringify(savedVideos.value));
  }
  function toggleChannel(id) {
    const i = savedChannels.value.indexOf(id);
    if (i > -1) savedChannels.value.splice(i, 1);
    else savedChannels.value.push(id);
    localStorage.setItem(CHANNELS_KEY, JSON.stringify(savedChannels.value));
  }

  // 상태 체크
  function isVideoSaved(id) {
    return savedVideos.value.includes(id);
  }
  function isChannelSaved(id) {
    return savedChannels.value.includes(id);
  }

  return {
    savedVideos,
    savedChannels,
    toggleVideo,
    toggleChannel,
    isVideoSaved,
    isChannelSaved,
  };
});
