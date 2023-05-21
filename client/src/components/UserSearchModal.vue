<template>
  <div id="myModal" class="modal" v-if="showModal">
    <div class="modal-content">
      <h1>Add Server Member</h1>
      <input type="text" v-model="searchText" @keyup="searchUser" placeholder="Search user...">
      <ul>
        <li v-for="user in searchedUsers" :key="user.id">
          <div class="user-container">
            <span>{{ user.username }}:{{ user.discriminator }}</span>
            <button class="add" @click="addMemberToServer(user.id)">Add</button>
          </div>
        </li>
      </ul>
      <button class="cancel" @click="$emit('close-modal')">Cancel</button>
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

input[type="text"] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
  border-radius: 4px;
  border: 2px solid #ccc;
}

.user-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.add {
  background-color:#2E8B57;
  border: none;
  width: 40%;
  border-radius: 4px;
  color: #ffffff;
  cursor: pointer;
  font-size: 14px;
  padding: 8px 16px;
  text-align: center;
  text-decoration: none;
  transition-duration: 0.2s;
  float: right;
  vertical-align: middle;
}

.cancel {
  background-color:#CD5C5C;
  border: none;
  width: 40%;
  margin: 5% 0; 
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
</style>