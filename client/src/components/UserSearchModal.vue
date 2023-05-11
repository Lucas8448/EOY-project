<template>
  <div id="myModal" class="modal" v-if="showModal">
    <div class="modal-content">
      <h1>Add Server Member</h1>
      <input type="text" v-model="searchText" @keyup="searchUser" placeholder="Search user...">
      <ul>
        <li v-for="user in searchedUsers" :key="user.id">
          {{ user.username }}:{{ user.discriminator }}
          <button @click="addMemberToServer(user.id)">Add</button>
        </li>
      </ul>
      <button @click="$emit('close-modal')">Cancel</button>
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

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 10px 0;
}

input[type="text"] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
  border-radius: 4px;
  border: 2px solid #ccc;
}
</style>