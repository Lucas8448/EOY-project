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
    },
    logIn(state){
      state.loggedIn = true;
    },
    logOut(state){
      state.loggedIn = false;
    }
  },
  actions: {},
  getters: {},
});

export default store;
