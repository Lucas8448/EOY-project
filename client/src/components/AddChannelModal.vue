<template>
  <div class="modal">
    <div class="modal-content">
      <h2>Add Channel</h2>
      <input type="text" class="input" v-model="channelName" placeholder="Channel name" @keyup.enter="addChannel" />
      <div class="modal-actions">
        <button class="confirm" @click="addChannel()">
          Add
          <span></span>
        </button>
        <button class="cancel" @click="$emit('close')">
          Cancel
          <span></span>
        </button>
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

.input {
  width: 100%;
  height: 45px;
  padding: 12px;
  border-radius: 12px;
  border: 1.5px solid lightgrey;
  outline: none;
  transition: all 0.3s cubic-bezier(0.19, 1, 0.22, 1);
  box-shadow: 0px 0px 20px -18px;
}

.input:hover {
  border: 2px solid lightgrey;
  box-shadow: 0px 0px 20px -17px;
}

.input:active {
  transform: scale(0.95);
}

.input:focus {
  border: 3px solid grey;
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
  justify-content: space-between;
  margin-top: 10px;
}

.modal-actions button {
  flex: 1;
  margin-right: 10px;
  /* Add spacing between buttons */
}

.modal-actions button:last-child {
  margin-right: 0;
  /* Remove margin from last button */
}

.confirm {
  border: none;
  display: block;
  position: relative;
  padding: 0.7em 2em;
  font-size: 18px;
  background: transparent;
  cursor: pointer;
  user-select: none;
  overflow: hidden;
  color: #2E8B57;
  z-index: 1;
  font-family: inherit;
  font-weight: 500;
  text-align: center;
}

.confirm span {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: transparent;
  z-index: -1;
  border: 4px solid #2E8B57;
}

.confirm span::before {
  content: "";
  display: block;
  position: absolute;
  width: 8%;
  height: 500%;
  background: var(--lightgray);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-60deg);
  transition: all 0.3s;
}

.confirm:hover span::before {
  transform: translate(-50%, -50%) rotate(-90deg);
  width: 100%;
  background: #2E8B57;
}

.confirm:hover {
  color: white;
}

.confirm:active span::before {
  background: #2E8B57;
}

.cancel {
  border: none;
  display: block;
  position: relative;
  padding: 0.7em 2em;
  font-size: 18px;
  background: transparent;
  cursor: pointer;
  user-select: none;
  overflow: hidden;
  color: #CD5C5C;
  z-index: 1;
  font-family: inherit;
  font-weight: 500;
  text-align: center;
}

.cancel span {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: transparent;
  z-index: -1;
  border: 4px solid #CD5C5C;
}

.cancel span::before {
  content: "";
  display: block;
  position: absolute;
  width: 8%;
  height: 500%;
  background: var(--lightgray);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-60deg);
  transition: all 0.3s;
}

.cancel:hover span::before {
  transform: translate(-50%, -50%) rotate(-90deg);
  width: 100%;
  background: #CD5C5C;
}

.cancel:hover {
  color: white;
}

.cancel:active span::before {
  background: #CD5C5C;
}
</style>