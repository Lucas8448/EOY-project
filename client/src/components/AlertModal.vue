<template>
  <transition name="fade">
    <div class="alert-container" v-if="alertMessage">
      <div class="alert">
        {{ alertMessage }}
        <button @click="clearAlert">X</button>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  data() {
    return {
      alertMessage: '',
    }
  },
  methods: {
    showAlert(message) {
      this.alertMessage = message;
      setTimeout(() => {
        this.clearAlert();
      }, 3000); // auto clear after 3 seconds
    },
    clearAlert() {
      this.alertMessage = '';
    },
  },
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 1s ease-in-out;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.alert-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  /* changed from left to right */
  z-index: 999;
}

.alert {
  background-color: #f44336;
  color: white;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.alert button {
  background: none;
  border: none;
  color: white;
  font-size: 16px;
  padding: 0px 20px;
  cursor: pointer;
}</style>
