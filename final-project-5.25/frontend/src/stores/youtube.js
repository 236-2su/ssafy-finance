// src/stores/youtube.js
import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { useUserStore } from "./user";

export const useYouTubeStore = defineStore("youtube", () => {
  const savedVideos = ref([]);
  const savedChannels = ref([]);
  const userStore = useUserStore();

  // 백엔드에서 사용자의 저장된 영상/채널 불러오기
  async function loadUserData() {
    if (!userStore.isLogin) return;
    
    try {
      const response = await axios.get("/api/accounts/profile/");
      if (response.data.watch_later_videos) {
        savedVideos.value = response.data.watch_later_videos;
      }
      if (response.data.subscribed_channels) {
        savedChannels.value = response.data.subscribed_channels;
      }
    } catch (error) {
      console.error("사용자 데이터 로드 실패:", error);
      // 로그인하지 않은 경우 localStorage에서 불러오기
      loadFromLocalStorage();
    }
  }

  // localStorage에서 불러오기 (비로그인 사용자용)
  function loadFromLocalStorage() {
    const videos = localStorage.getItem("savedVideos");
    const channels = localStorage.getItem("savedChannels");
    
    if (videos) {
      savedVideos.value = JSON.parse(videos);
    }
    if (channels) {
      savedChannels.value = JSON.parse(channels);
    }
  }

  // 영상 토글
  async function toggleVideo(videoId, videoData = null) {
    const isCurrentlySaved = isVideoSaved(videoId);
    
    if (userStore.isLogin) {
      try {
        if (isCurrentlySaved) {
          // 제거
          await axios.delete("/api/accounts/youtube/", {
            data: {
              type: "video",
              content_id: videoId
            }
          });
          savedVideos.value = savedVideos.value.filter(video => 
            video.video_id !== videoId
          );
        } else {
          // 추가
          const contentData = videoData || {
            video_id: videoId,
            title: "Unknown Video",
            channel_title: "Unknown Channel",
            thumbnail_url: "",
            added_at: new Date().toISOString()
          };
          
          await axios.post("/api/accounts/youtube/", {
            type: "video",
            content_data: contentData
          });
          savedVideos.value.push(contentData);
        }
      } catch (error) {
        console.error("영상 저장/제거 실패:", error);
        // 백엔드 실패 시 localStorage 사용
        toggleVideoLocalStorage(videoId, videoData);
      }
    } else {
      toggleVideoLocalStorage(videoId, videoData);
    }
  }

  // 채널 토글
  async function toggleChannel(channelId, channelData = null) {
    const isCurrentlySaved = isChannelSaved(channelId);
    
    if (userStore.isLogin) {
      try {
        if (isCurrentlySaved) {
          // 제거
          await axios.delete("/api/accounts/youtube/", {
            data: {
              type: "channel",
              content_id: channelId
            }
          });
          savedChannels.value = savedChannels.value.filter(channel => 
            channel.channel_id !== channelId
          );
        } else {
          // 추가
          const contentData = channelData || {
            channel_id: channelId,
            title: "Unknown Channel",
            thumbnail_url: "",
            subscriber_count: 0,
            added_at: new Date().toISOString()
          };
          
          await axios.post("/api/accounts/youtube/", {
            type: "channel",
            content_data: contentData
          });
          savedChannels.value.push(contentData);
        }
      } catch (error) {
        console.error("채널 저장/제거 실패:", error);
        // 백엔드 실패 시 localStorage 사용
        toggleChannelLocalStorage(channelId, channelData);
      }
    } else {
      toggleChannelLocalStorage(channelId, channelData);
    }
  }

  // localStorage 영상 토글 (비로그인 사용자용)
  function toggleVideoLocalStorage(videoId, videoData) {
    const index = savedVideos.value.findIndex(video => video.video_id === videoId);
    
    if (index > -1) {
      savedVideos.value.splice(index, 1);
    } else {
      const contentData = videoData || {
        video_id: videoId,
        title: "Unknown Video",
        channel_title: "Unknown Channel",
        thumbnail_url: "",
        added_at: new Date().toISOString()
      };
      savedVideos.value.push(contentData);
    }
    
    localStorage.setItem("savedVideos", JSON.stringify(savedVideos.value));
  }

  // localStorage 채널 토글 (비로그인 사용자용)
  function toggleChannelLocalStorage(channelId, channelData) {
    const index = savedChannels.value.findIndex(channel => channel.channel_id === channelId);
    
    if (index > -1) {
      savedChannels.value.splice(index, 1);
    } else {
      const contentData = channelData || {
        channel_id: channelId,
        title: "Unknown Channel",
        thumbnail_url: "",
        subscriber_count: 0,
        added_at: new Date().toISOString()
      };
      savedChannels.value.push(contentData);
    }
    
    localStorage.setItem("savedChannels", JSON.stringify(savedChannels.value));
  }

  // 상태 체크
  function isVideoSaved(videoId) {
    return savedVideos.value.some(video => video.video_id === videoId);
  }

  function isChannelSaved(channelId) {
    return savedChannels.value.some(channel => channel.channel_id === channelId);
  }

  // 초기화
  function initialize() {
    if (userStore.isLogin) {
      loadUserData();
    } else {
      loadFromLocalStorage();
    }
  }

  // 로그아웃 시 데이터 클리어
  function clearData() {
    savedVideos.value = [];
    savedChannels.value = [];
  }

  return {
    savedVideos,
    savedChannels,
    toggleVideo,
    toggleChannel,
    isVideoSaved,
    isChannelSaved,
    initialize,
    clearData,
    loadUserData
  };
});
