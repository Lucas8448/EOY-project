<template>
  <div class="main">
    <div class="navbar">
      <div class="navbar-items">
        <h1 v-if="userInfo">{{ userInfo.username }}:{{ userInfo.discriminator }}</h1>
        <h1 v-else>Loading...</h1>
      </div>
    </div>
    <div class="servers">
      <div v-for="server in servers" @click="fetchChannels(server.id)" class="server-icon">
        <h1>{{ server.name }}</h1>
      </div>
      <button @click="showAddServerModal = true">Add Server</button>
    </div>
    <div class="channels">
      <div v-for="channel in channels" @click="fetchMessages(channel.id)" class="channel">
        <h2>{{ channel.name }}</h2>
      </div>
      <button @click="showAddChannelModal = true">Add Channel</button>
    </div>
    <div class="messages">
      <div v-for="message in messages" class="message">
        <p>{{ message.content }}</p>
      </div>
      <div class="message-input">
        <input type="text" v-model="message" @keyup.enter="sendMessage" placeholder="Type your message...">
      </div>
    </div>
    <add-server-modal v-if="showAddServerModal" @close="showAddServerModal = false" @add="addServer"></add-server-modal>
    <add-channel-modal v-if="showAddChannelModal" @close="showAddChannelModal = false"
      @add="addChannel"></add-channel-modal>
  </div>
</template>

<script>
import { socket } from "../socket";
import AddServerModal from "../components/AddServerModal.vue";
import AddChannelModal from "../components/AddChannelModal.vue";

export default {
  components: {
    AddServerModal,
    AddChannelModal,
  },
  data() {
    return {
      userInfo: null,
      userId: null,
      currentServer: null,
      currentChannel: null,
      channels: [],
      messages: [],
      showAddServerModal: false,
      showAddChannelModal: false,
    };
  },
  mounted() {
    try {
      this.userInfo = this.$store.getters.CurrentUser;
      this.userId = this.userInfo.Id
      this.servers = this.fetchServers()
    } catch (err) {
      this.$router.push("/");
    }
  },
  methods: {
    async fetchServers() {
      socket.emit("get_servers");
      socket.on("get_servers", (data) => {
        if (data.success) {
          console.log(data);
          return data.servers
        } else if (data.error) {
          alert(data.error);
          return data.error
        }
      });
    },
    async fetchChannels(server_id) {
      socket.emit("get_channels", { server_id });
      socket.on("get_channels", (data) => {
        if (data.success) {
          this.channels = data.channels;
        } else {
          alert("Failed to fetch channels");
        }
      });
    },
    async fetchMessages(channel_id) {
      socket.emit("get_messages", { channel_id });
      socket.on("get_messages", (data) => {
        if (data.success) {
          this.messages = data.messages;
        } else {
          alert("Failed to fetch messages");
        }
      });
    },
    async sendMessage() {
      socket.emit("send_message", { content: this.message,  });
      socket.on("send_message", (data) => {
        if (data.success) {
          this.messages.push(data.message);
        } else {
          alert("Failed to send message");
        }
      });
    },
    async addChannel() {
      socket.emit("add_channel", { name: this.channelName });
      socket.on("add_channel", (data) => {
        if (data.success) {
          this.channels.push(data.channel);
        } else {
          alert("Failed to add channel");
        }
      });
    },
    async addServer() {
      socket.emit("add_server", { name: this.serverName });
      socket.on("add_server", (data) => {
        if (data.success) {
          console.log("Added server", data);
          this.servers.push(data.server);
        } else {
          alert("Failed to add server");
        }
      });
    },
    async addServer(serverName) {
      socket.emit("add_server", { name: serverName });
      socket.on("add_server", (data) => {
        if (data.success) {
          this.servers.push(data.server);
          this.showAddServerModal = false;
        } else {
          alert("Failed to add server");
        }
      });
    },
    async addChannel(channelName) {
      socket.emit("add_channel", { name: channelName });
      socket.on("add_channel", (data) => {
        if (data.success) {
          this.channels.push(data.channel);
          this.showAddChannelModal = false;
        } else {
          alert("Failed to add channel");
        }
      });
    },
  },
};
</script>

<style scoped>
.main {
  display: grid;
  grid-template-columns: 12rem 12rem 1fr;
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
  background-color: #C4C4C4;
}

.channels {
  grid-area: 2 / 2 / 3 / 3;
  background-color: #4B4B4B;
}

.messages {
  grid-area: 2 / 3 / 3 / 4;
  background-color: #626262;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding-bottom: 10px;
}

.message-input {
  display: flex;
  align-items: center;
  padding: 10px;
}

.message-input input {
  flex: 1;
  margin-right: 10px;
  border: none;
  border-radius: 4px;
  padding: 8px;
  font-size: 16px;
  outline: none;
}

h1 {
  color: #fff;
  margin: 0;
}

button {
  background-color: #6C8BA6;
  border: none;
  width: 90%;
  margin: 5% 5%;
  border-radius: 4px;
  color: #ffffff;
  cursor: pointer;
  font-size: 14px;
  margin-top: 10px;
  padding: 8px 16px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  transition-duration: 0.2s;
}

button:hover {
  background-color: #5a7bb2;
  color: white;
}

.channel {
  color: #ffffff;
  margin-bottom: 10px;
}
</style>
