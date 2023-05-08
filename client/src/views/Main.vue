<template>
  <div class="main">
    <div class="navbar">
      <div class="navbar-items">
        <img class="avatar" v-if="avatar" :src="imageSource + avatar" />
        <h1 v-if="userInfo">{{ userInfo.username }}</h1>
        <h1 v-else>Loading...</h1>
      </div>
    </div>
    <div class="servers">
      <div v-for="server in servers" class="server-icon">
        <img :src="imageSource + server.icon" class="server" alt="server">
      </div>
    </div>
    <div class="channels">
      <div v-for="channel in channels" @click="fetchMessages(channel.id)" class="channel">
        <h2>{{ channel.name }}</h2>
      </div>
    </div>
    <div class="messages">
      <div v-for="message in messages" class="message">
        <p>{{ message.content }}</p>
      </div>
    </div>
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
      channels: [],
      messages: []
    };
  },
  mounted() {
    try {
      this.userInfo = this.$store.getters.CurrentUser;
      this.imageSource = "http://127.0.0.1:3055/image/"
      this.avatar = this.userInfo.avatar;
      this.userId = this.userInfo.userId
      this.servers = this.fetchServers
    } catch (err) {
      this.$router.push("/");
    }
  },
  methods: {
    fetchServers() {
      socket.emit("get_servers", { Id: this.userId });
      socket.on("get_servers", (data) => {
        if (data.success) {
          console.log(data.success);
          return data.servers
        } else if (data.error) {
          alert(data.error);
          return data.error
        }
      });
    },
    fetchChannels(server_id) {
      socket.emit("get_channels", { server_id });
      socket.on("get_channels", (data) => {
        if (data.success) {
          this.channels = data.channels;
        } else {
          alert("Failed to fetch channels");
        }
      });
    },
    fetchMessages(channel_id) {
      socket.emit("get_messages", { channel_id });
      socket.on("get_messages", (data) => {
        if (data.success) {
          this.messages = data.messages;
        } else {
          alert("Failed to fetch messages");
        }
      });
    }
  }
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
