<template>
  <div class="modal">
    <div class="modal-content">
      <h2>Add Server</h2>
            <input type="text" v-model="serverName" placeholder="Server name" @keyup.enter="addServer"   />
        <div class="modal-actions">
          <button @click="addServer">Add</button>
          <button @click="$emit('close')">Cancel</button>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      serverName: "",
    };
  },
  methods: {
    addServer() {
      this.$emit("add", this.serverName);
      this.serverName = "";
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

input[type="text"] {
  padding: 10px;
  font-size: 16px;
  border: 2px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  width: 100%;
}

input[type="text"]:focus {
  border-color: #5c5cff;
  outline: none;
}

.modal-content {
  background-color: #fff;
  color: black;
  padding: 20px;
  border-radius: 5px;
  width: 300px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

button {
  margin-left: 10px;
}
</style>
