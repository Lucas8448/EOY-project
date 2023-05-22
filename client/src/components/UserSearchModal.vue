<template>
  <div id="myModal" class="modal" v-if="showModal">
    <div class="modal-content">
      <h1>Add Server Member</h1>
      <input type="text" class="input" v-model="searchText" @keyup="searchUser" placeholder="Search user...">
      <ul>
        <li v-for="user in searchedUsers" :key="user.id">
          <div class="user-container">
            <span>{{ user.username }}:{{ user.discriminator }}</span>
            <button class="add" @click="addMemberToServer(user.id)">
              Add
              <span></span>
            </button>
          </div>
        </li>
      </ul>
      <button class="cancel" @click="$emit('close-modal')">
        Exit
        <span></span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserSearchModal',
  props: ['userInfo', 'searchedUsers', 'showModal'],
  data() {
    return {
      searchText: ''
    }
  },
  methods: {
    addMemberToServer(id) {
      this.$emit('add-member', id);
    },
    searchUser() {
      this.$emit('search-user', this.searchText);
    }
  }
}
</script>

<style scoped>
.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  color: #000;
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 500px;
  border-radius: 10px;
}

.close {
  color: #aaaaaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

ul {
  list-style-type: none;
  padding: 0;
  max-height: 50vh;
  overflow: scroll;
  scroll-behavior: smooth;
}

li {
  margin: 2.5% 2.5%;
  padding: 2.5% 2.5%;
  border: 2px darkgrey solid;
  border-radius: 20px;
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

.user-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.add {
  border: none;
  display: block;
  position: relative;
  padding: 0.7em 2em;
  font-size: 14px;
  background: #2E8B57;
  cursor: pointer;
  user-select: none;
  overflow: hidden;
  color: #ffffff;
  z-index: 1;
  font-family: inherit;
  font-weight: 500;
  text-align: center;
}

.add:before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #2E8B57;
  z-index: -1;
  transition: all 0.3s;
  transform: scale(0.1);
  transform-origin: left center;
}

.add:hover:before {
  transform: scale(1);
}

.add:active {
  background: #2E8B57;
  color: #ffffff;
}

.cancel {
  margin-top: 1em;
  border: none;
  display: block;
  position: relative;
  padding: 0.7em 2em;
  font-size: 14px;
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
