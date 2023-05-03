<template>
  <div class="main">
    <h1 v-if="userInfo">{{ userInfo.username }}</h1>
    <h1 v-else>Loading...</h1>
  </div>
</template>

<script>
import socket from "@/socket";

export default {
  data() {
    return {
      userInfo: null
    };
  },
  mounted() {
    this.userInfo = this.$store.getters.CurrentUser;
  },
};
</script>
