import { createApp } from 'vue';
import { createStore } from 'vuex';

const store = createStore({
  state: {
    loggedIn: false,
    userData: null,
  },
  mutations: {
    setUserData(state, userData) {
      state.userData = userData;
    },
    clearUserData(state) {
      state.userData = null;
    }
  },
  actions: {},
  getters: {
    CurrentUser(state){
      return state.userData;
    }
  },
});

export default store;
