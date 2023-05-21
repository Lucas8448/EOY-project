<template>
  <div class="main">
    <div class="navbar">
      <div class="navbar-items">
        <h1 v-if="userInfo" class="username">{{ userInfo.username }}#{{ userInfo.discriminator }}</h1>
        <h1 v-else>Loading...</h1>
      </div>
    </div>
    <div class="servers">
      <div v-for="server in servers" :key="server.id" @click="changeServer(server.id)" class="server-icon">
        <div class="server-item">
          <h3>{{ server.name }}</h3>
        </div>
      </div>
      <button @click="showAddServerModal = true">Add Server</button>
    </div>
    <div class="channels">
      <div v-for="channel in channels" :key="channel.id" @click="fetchMessages(channel.id)" class="channel" v-show="currentServer">
        <div class="channel-item">
          <h3>{{ channel.name }}</h3>
        </div>
      </div>
      <button @click="showUserSearchModal = true" v-show="currentServer">Add user</button>
      <button @click="showAddChannelModal = true" v-show="currentServer">Add Channel</button>
    </div>
    <div class="messages">
      <div v-for="message in messages" :key="message.id" class="message">
        <p>{{ message.content }}</p>
      </div>
      <div class="message-input">
        <input type="text" v-model="message" @keyup.enter="sendMessage" placeholder="Type your message...">
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
        this.messages.push(data.message);
      } else if (data.error) {
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
      socket.emit("add_member", { serverId: this.currentServer, userId });
      socket.on("add_member", (data) => {
        if (data.success) {
          // handle successful addition of member
        } else if (data.error) {
          this.$refs.alertModal.showAlert(data.error);
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

.message {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  margin: 10px;
  padding: 10px;
  border-radius: 10px;
  background-color: #838383;
  color: #fff;
}

.message p {
  margin: 0;
  padding: 0;
  word-wrap: break-word;
}

h1 {
  color: #fff;
  margin: 1%;
}

.username {
  width: 70px;
  white-space: nowrap;
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
