<template>
  <div class="main">
    <div class="servers">
      <h3>Servers</h3>
      <ul>
        <li v-for="server in servers" :key="server.id">
          <a href="#" @click="joinServer(server.id)">{{ server.name }}</a>
        </li>
      </ul>
      <div>
        <input type="text" v-model="newServerName" placeholder="New Server Name" />
        <button @click="createServer">Create Server</button>
      </div>
    </div>
    <div class="channels">
      <h3>Channels</h3>
      <ul>
        <li v-for="channel in channels" :key="channel.id">
          <a href="#" @click="joinChannel(channel.id)">{{ channel.name }}</a>
        </li>
      </ul>
      <div>
        <input type="text" v-model="newChannelName" placeholder="New Channel Name" />
        <button @click="createChannel">Create Channel</button>
      </div>
    </div>
    <div class="chat">
      <h3>Chat</h3>
      <ul>
        <li v-for="message in messages" :key="message.id">
          <strong>{{ message.author.username }}:</strong> {{ message.content }}
        </li>
      </ul>
      <div>
        <input type="text" v-model="newMessage" placeholder="Type a message..." />
        <button @click="sendMessage">Send</button>
      </div>
    </div>
    <div class="user">
      <p>Welcome, {{ userData.username }}!</p>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import socket from "@/socket";

export default {
  computed: {
    userData() {
      return this.$store.state.userData;
    },
  },
  data() {
    return {
      servers: [],
      channels: [],
      messages: [],
      newServerName: "",
      newChannelName: "",
      newMessage: "",
      currentServer: null,
      currentChannel: null,
    };
  },
  mounted() {
    socket.emit("getConnectedServers", { userId: this.userData.id });
  },
  methods: {
    async joinServer(serverId) {
      this.currentServer = serverId;
      this.channels = [];
      this.messages = [];
      await socket.emitAsync("joinServer", { serverId, userId: this.userData.id });
      await socket.emitAsync("getChannels", { serverId });
    },
    async createServer() {
      if (this.newServerName.trim() === "") {
        return;
      }
      await socket.emitAsync("createServer", {
        name: this.newServerName,
        owner_id: this.userData.id,
      });
      this.newServerName = "";
    },
    async joinChannel(channelId) {
      this.currentChannel = channelId;
      this.messages = [];
      await socket.emitAsync("joinChannel", { channelId, userId: this.userData.id });
      await socket.emitAsync("getMessages", { channelId });
    },
    async createChannel() {
      if (this.newChannelName.trim() === "") {
        return;
      }
      if (!this.currentServer) {
        return;
      }
      await socket.emitAsync("createChannel", {
        name: this.newChannelName,
        type: "text",
        server_id: this.currentServer,
      });
      this.newChannelName = "";
    },
    async sendMessage() {
      if (this.newMessage.trim() === "") {
        return;
      }
      if (!this.currentChannel) {
        return;
      }
      await socket.emitAsync("sendMessage", {
        content: this.newMessage,
        author_id: this.userData.id,
        channel_id: this.currentChannel,
      });
      this.newMessage = "";
    },
    logout() {
      this.$store.commit("clearUserData");
      this.$router.push("/");
    },
  },
  created() {
    this.$store.dispatch("fetchUserData");
    socket.on("getConnectedServers", (data) => {
      this.servers = data.servers;
    });
    socket.on("getChannels", (data) => {
      this.channels = data.channels;
    });
    socket.on("getMessages", (data) => {
      this.messages = data.messages;
    });
    socket.on("sendMessage", (data) => {
      this.messages.push(data);
    });
    socket.on("createServer", (data) => {
      this.servers.push(data);
    });
    socket.on("createChannel", (data) => {
      if (data.server_id === this.currentServer) {
        this.channels.push(data);
      }
    });
    socket.on("joinChannel", (data) => {
      this.currentChannel = data.channelId;
    });
  },
};
</script>
