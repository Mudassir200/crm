<template>
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
    </div>
  </template>
  
  <script>
  import { useLoadingStore } from "@/stores/loading";
  import { storeToRefs } from "pinia";
  
  export default {
    setup() {
      const loadingStore = useLoadingStore();
      const { loading } = storeToRefs(loadingStore);
  
      return { loading };
    },
  };
  </script>
  
  <style>
  /* Basic Full-Screen Loader */
  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
  }
  
  .spinner {
    border: 5px solid rgba(255, 255, 255, 0.3);
    border-top: 5px solid #fff;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  </style>
  