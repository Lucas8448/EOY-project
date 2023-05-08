<template>
  <div class="main">
    <div class="navbar">
      <div class="navbar-items">
        <img class="avatar" v-if="avatar" :src="avatar" />
        <h1 v-if="userInfo">{{ userInfo.username }}</h1>
        <h1 v-else>Loading...</h1>
      </div>
    </div>
    <div class="servers"></div>
    <div class="channels"></div>
    <div class="messages"></div>
  </div>
</template>

<script>
import socket from "@/socket";

export default {
  data() {
    return {
      userInfo: null,
      avatar: null,
      userId: null,
      currentServer: null,
      currentChannel: null,
      
    };
  },
  mounted() {
    try {
      this.userInfo = this.$store.getters.CurrentUser;
      this.avatar = "http://127.0.0.1:3055/image/" + this.userInfo.avatar;
      this.userId = this.userInfo.userId
    } catch (err) {
      this.$router.push("/");
    }
  },
};
</script>

<style scoped>
.main {
  display: grid;
  grid-template-columns: 80px 240px 1fr;
  grid-template-rows: 60px 1fr;
  grid-column-gap: 0px;
  grid-row-gap: 0px;
  height: 100vh;
}

.navbar {
  grid-area: 1 / 1 / 2 / 4;
  display: flex;
  align-items: center;
  background-color: #545454;
  padding: 0 20px;
  height: 60px;
}

.navbar-items {
  display: flex;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.servers {
  grid-area: 2 / 1 / 3 / 2;
  background-color: #e1e1e1;
}

.channels {
  grid-area: 2 / 2 / 3 / 3;
  background-color: #1d1d1d;
}

.messages {
  grid-area: 2 / 3 / 3 / 4;
  background-color: #400000;
}

h1 {
  color: #fff;
  margin: 0;
}
</style>
