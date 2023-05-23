<template>
  <div class="main">
    <div class="navbar">
      <div class="navbar-items">
        <h1 v-if="userInfo" class="username">{{ userInfo.username }}#{{ userInfo.discriminator }}</h1>
        <h1 v-else>Loading...</h1>
      </div>
    </div>
    <div class="servers">
      <div v-for="server in servers" :key="server.id" @click="changeServer(server.id)" class="server-icon" :class="{ 'server-active': server.id === currentServer }">
        <div class="server-item">
          <h3>{{ server.name }}</h3>
        </div>
      </div>
      <button @click="showAddServerModal = true">Add Server</button>
    </div>
    <div class="channels">
      <div v-for="channel in channels" :key="channel.id" @click="fetchMessages(channel.id)" class="channel" :class="{ 'channel-active': channel.id === currentChannel }">
        <div class="channel-item">
          <h3>{{ channel.name }}</h3>
        </div>
      </div>
      <button @click="showUserSearchModal = true" v-show="currentServer">Add user</button>
      <button @click="showAddChannelModal = true" v-show="currentServer">Add Channel</button>
    </div>
    <div class="messages">
      <div v-for="message in messages" :key="message.id" class="message">
        <p class="message"><span class="username">{{ getUsername(message.author_id) }}</span> : {{ message.content }}</p>
      </div>
      <div class="message-input" v-if="currentChannel">
        <input type="text" v-model="message" @keyup.enter="sendMessage" placeholder="Type your message...">
      </div>
      <div v-else>
        <div class="loading-icon">
          <div class="finger"></div>
          <div class="finger"></div>
          <div class="finger"></div>
          <div class="finger"></div>
          <div class="palm"></div>		
          <div class="thumb"></div>
          <p class="nochannel">No channel selected</p>
        </div>
      </div>
    </div>
    <add-server-modal v-if="showAddServerModal" @close="showAddServerModal = false" @add="addServer"></add-server-modal>
    <add-channel-modal v-if="showAddChannelModal" @close="showAddChannelModal = false"
      @add="addChannel"></add-channel-modal>
    <user-search-modal
      v-if="showUserSearchModal"
      :userInfo="userInfo"
      :searchedUsers="searchedUsers"
      :showModal="showUserSearchModal"
      @close-modal="showUserSearchModal = false"
      @add-member="addMemberToServer"
      @search-user="searchUser"></user-search-modal>
      <alert-modal ref="alertModal"></alert-modal>
  </div>
</template>

<script>
import { socket } from "../socket";
import AddServerModal from "../components/AddServerModal.vue";
import AddChannelModal from "../components/AddChannelModal.vue";
import UserSearchModal from "../components/UserSearchModal.vue";
import AlertModal from "../components/AlertModal.vue";

export default {
  components: {
    AddServerModal,
    AddChannelModal,
    UserSearchModal,
    AlertModal,
  },
  data() {
    return {
      userInfo: null,
      userId: null,
      currentServer: null,
      currentChannel: null,
      servers: [],
      channels: [],
      messages: [],
      searchedUsers: [],
      message: "",
      showAddServerModal: false,
      showAddChannelModal: false,
      showUserSearchModal: false,
      alertMessage: '',
      usernames: {},
    };
  },
  created() {
    try {
      this.userInfo = this.$store.getters.CurrentUser;
      this.userId = this.userInfo.Id;
      socket.emit("get_servers");
      socket.on("get_servers", (data) => {
        if (data.success) {
          console.log(data);
          this.servers = data.servers
        } else if (data.error) {
          alert(data.error);
          this.servers = null;
        } else {
          console.log(data)
        }
      });
    } catch (err) {
      this.$router.push("/");
    }
  },
  mounted() {
    socket.on('message', (data) => {
      if (data.success) {
        this.messages.push(data.message);
      } else if (data.error) {
        this.$refs.alertModal.showAlert(data.error);
      }
    });
    socket.on("send_message", (data) => {
      if (data.success) {
        console.log(data);
        this.message = ""
        this.messages.push(data.message);
      } else if (data.error) {
        this.message = ""
        this.$refs.alertModal.showAlert(data.error);
      }
    });
  },
  methods: {
    async fetchServers() {
      socket.emit("get_servers");
      socket.on("get_servers", (data) => {
        if (data.success) {
          console.log(data);
          this.servers = data.servers
        } else if (data.error) {
          this.$refs.alertModal.showAlert(data.error);
        }
      });
    },
    async fetchChannels(server_id) {
      socket.emit("get_channels", { server_id });
      socket.on("get_channels", (data) => {
        if (data.success) {
          this.channels = data.channels;
        } else if (data.error) {
          this.$refs.alertModal.showAlert(data.error);
        }
      });
    },
    async fetchMessages(channel_id) {
      this.currentChannel = channel_id;
      socket.emit("get_messages", { channel_id:channel_id });
      socket.on("get_messages", (data) => {
        if (data.success) {
          this.messages = data.messages;
        } else if (data.error) {
          this.$refs.alertModal.showAlert(data.error);
        }
      });
    },
    async sendMessage() {
      socket.emit("send_message", { content: this.message, channel_id:this.currentChannel });
    },
    async addChannel(channelName) {
      console.log("Adding channel", channelName, this.currentServer)
      socket.emit("add_channel", { name: channelName, server_id:this.currentServer });
      socket.on("add_channel", (data) => {
        if (data.success) {
          this.channels = data.channels
          this.showAddChannelModal = false;
        } else if (data.error) {
          this.$refs.alertModal.showAlert(data.error);
        }
      });
    },
    async addServer(serverName) {
      socket.emit("add_server", { name: serverName });
      socket.on("add_server", (data) => {
        if (data.success) {
          this.servers = data.servers
          this.showAddServerModal = false;
        } else if (data.error) {
          this.$refs.alertModal.showAlert(data.error);
        }
      });
    },
    async changeServer(serverId) {
      this.currentServer = serverId;
      this.currentChannel = null;
      console.log("changed server to:", this.currentServer)
      this.fetchChannels(serverId);
    },
    searchUser(searchText) {
      socket.emit("search_user", { searchText });
      socket.on("search_user", (data) => {
        if (data.success) {
          this.searchedUsers = data.users;
        } else if (data.error) {
          this.$refs.alertModal.showAlert(data.error);
        }
      });
    },
    addMemberToServer(userId) {
      socket.emit("add_member", { serverId: this.currentServer, userId: userId });
      socket.on("add_member", (data) => {
        if (data.success) {
          // handle successful addition of member
        } else if (data.error) {
          this.$refs.alertModal.showAlert(data.error);
        }
      });
    },
    getUsername(userId) {
      if (!this.usernames[userId]) {
        socket.emit("get_username", { userId: userId });
        socket.on("get_username", (data) => {
          if (data.success) {
            this.usernames[userId] = data.username;
            console.log(this.username)
          } else if (data.error) {
            this.usernames[userId] = "Unknown";
          }
        });
        return "Loading...";
      }
      return this.usernames[userId];
    }
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

.server-item {
  display: flex;
  align-items: center;
  padding: 10px 10px;
  margin: 10px 10px;
  border-radius: 10px 0 10px 0;
  cursor: pointer;
  background-color: #626262;
  color: #fff;
}

.channels {
  grid-area: 2 / 2 / 3 / 3;
  background-color: #4B4B4B;
}

.channel-item {
  color: #000000;
  display: flex;
  align-items: center;
  padding: 10px 10px;
  margin: 10px 10px;
  border-radius: 10px 0 10px 0;
  cursor: pointer;
  background-color: #C4C4C4;
}

.server-active div {
  background-color: #7B7B7B;
}

.channel-active div {
  background-color: #EFEFEF;
}

.messages {
  grid-area: 2 / 3 / 3 / 4;
  background-color: #626262;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding-bottom: 10px;
  overflow: scroll;
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

.messages {
  grid-area: 2 / 3 / 3 / 4;
  background-color: #626262;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding-bottom: 10px;
  overflow-y: scroll;
  position: relative;
}

.message p {
  color: #000;
  margin: 0;
  padding: 0;
  word-wrap: break-word;
  /* style in white box with black text */
  background-color: #fff;
  padding: 10px;
  border-radius: 10px;
  margin: 10px;
  max-width: 60%;
  position: relative;
}

.message::before {
  content: attr(data-username);
  font-weight: bold;
  margin-bottom: 5px;
}

.loading-icon {
  --skin-color: #E4C560;
  --tap-speed: 0.6s;
  --tap-stagger: 0.1s;
  position: relative;
  width: 80px;
  height: 60px;
  margin-left: 80px;
  left: calc(50% - 40px);
  margin-bottom: 40vh;
}

.nochannel {
  top: 10vh;
  right: 50%;
  text-align: center;
}

.loading-icon:before {
  content: '';
  display: block;
  width: 180%;
  height: 75%;
  position: absolute;
  top: 70%;
  right: 20%;
  background-color: black;
  border-radius: 40px 10px;
  filter: blur(10px);
  opacity: 0.3;
}

.palm {
  display: block;
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  background-color: var(--skin-color);
  border-radius: 10px 40px;
}

.thumb {
  position: absolute;
  width: 120%;
  height: 38px;
  background-color: var(--skin-color);
  bottom: -18%;
  right: 1%;
  transform-origin: calc(100% - 20px) 20px;
  transform: rotate(-20deg);
  border-radius: 30px 20px 20px 10px;
  border-bottom: 2px solid rgba(0, 0, 0, 0.1);
  border-left: 2px solid rgba(0, 0, 0, 0.1);
}

.thumb:after {
  width: 20%;
  height: 60%;
  content: '';
  background-color: rgba(255, 255, 255, 0.3);
  position: absolute;
  bottom: -8%;
  left: 5px;
  border-radius: 60% 10% 10% 30%;
  border-right: 2px solid rgba(0, 0, 0, 0.05);
}

.finger {
  position: absolute;
  width: 80%;
  height: 35px;
  background-color: var(--skin-color);
  bottom: 32%;
  right: 64%;
  transform-origin: 100% 20px;
  animation-duration: calc(var(--tap-speed) * 2);
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
  transform: rotate(10deg);
}

.finger:before {
  content: '';
  position: absolute;
  width: 140%;
  height: 30px;
  background-color: var(--skin-color);
  bottom: 8%;
  right: 65%;
  transform-origin: calc(100% - 20px) 20px;
  transform: rotate(-60deg);
  border-radius: 20px;
}

.finger:nth-child(1) {
  animation-delay: 0;
  filter: brightness(70%);
  animation-name: tap-upper-1;
}

.finger:nth-child(2) {
  animation-delay: var(--tap-stagger);
  filter: brightness(80%);
  animation-name: tap-upper-2;
}

.finger:nth-child(3) {
  animation-delay: calc(var(--tap-stagger) * 2);
  filter: brightness(90%);
  animation-name: tap-upper-3;
}

.finger:nth-child(4) {
  animation-delay: calc(var(--tap-stagger) * 3);
  filter: brightness(100%);
  animation-name: tap-upper-4;
}

@keyframes tap-upper-1 {
  0%, 50%, 100% {
    transform: rotate(10deg) scale(0.4);
  }

  40% {
    transform: rotate(50deg) scale(0.4);
  }
}

@keyframes tap-upper-2 {
  0%, 50%, 100% {
    transform: rotate(10deg) scale(0.6);
  }

  40% {
    transform: rotate(50deg) scale(0.6);
  }
}

@keyframes tap-upper-3 {
  0%, 50%, 100% {
    transform: rotate(10deg) scale(0.8);
  }

  40% {
    transform: rotate(50deg) scale(0.8);
  }
}

@keyframes tap-upper-4 {
  0%, 50%, 100% {
    transform: rotate(10deg) scale(1);
  }

  40% {
    transform: rotate(50deg) scale(1);
  }
}

h1 {
  color: #fff;
  margin: 1%;
}

.username {
  width: 70px;
  white-space: nowrap;
  font-weight: bold;
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
