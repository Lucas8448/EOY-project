<template>
  <div class="modal">
    <div class="modal-content">
      <h2>Add Channel</h2>
      <input type="text" v-model="channelName" placeholder="Channel name" @keyup.enter="addChannel" />
      <div class="modal-actions">
        <button class="confirm" @click="addChannel">Add</button>
        <button class="cancel" @click="$emit('close')">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      channelName: "",
    };
  },
  methods: {
    addChannel() {
      this.$emit("add", this.channelName);
      this.channelName = "";
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

.confirm {
  background-color:#2E8B57;
}

.cancel {
  background-color:#CD5C5C;
}
</style>
