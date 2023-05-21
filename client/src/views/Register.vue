<template>
  <div class="registration-form">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="input-group">
        <input class="input-field email-input" type="text" v-model="email" required />
        <span class="input-bar"></span>
        <label class="input-label">
          <span class="input-label-char" style="--index: 0">E</span>
          <span class="input-label-char" style="--index: 1">m</span>
          <span class="input-label-char" style="--index: 2">a</span>
          <span class="input-label-char" style="--index: 3">i</span>
          <span class="input-label-char" style="--index: 4">l</span>
        </label>
      </div>
      <div class="input-group">
        <input class="input-field password-input" type="password" v-model="password" required />
        <span class="input-bar"></span>
        <label class="input-label">
          <span class="input-label-char" style="--index: 0">P</span>
          <span class="input-label-char" style="--index: 1">a</span>
          <span class="input-label-char" style="--index: 2">s</span>
          <span class="input-label-char" style="--index: 3">s</span>
          <span class="input-label-char" style="--index: 4">w</span>
          <span class="input-label-char" style="--index: 5">o</span>
          <span class="input-label-char" style="--index: 6">r</span>
          <span class="input-label-char" style="--index: 7">d</span>
        </label>
      </div>
      <transition name="slide-fade">
        <div v-if="email && password">
          <div class="input-group">
            <input class="input-field username-input" type="text" v-model="username" required />
            <span class="input-bar"></span>
            <label class="input-label">
              <span class="input-label-char" style="--index: 0">U</span>
              <span class="input-label-char" style="--index: 1">s</span>
              <span class="input-label-char" style="--index: 2">e</span>
              <span class="input-label-char" style="--index: 3">r</span>
              <span class="input-label-char" style="--index: 4">n</span>
              <span class="input-label-char" style="--index: 5">a</span>
              <span class="input-label-char" style="--index: 6">m</span>
              <span class="input-label-char" style="--index: 7">e</span>
            </label>
          </div>
        </div>
      </transition>
      <button class="submit-button" type="submit">
        Register
      </button>
    </form>
    <p>
      Already have an account? <router-link class="login-link" to="/">Login</router-link>
    </p>
  </div>
  <alert-modal ref="alertModal"></alert-modal>
</template>

<style scoped>
.registration-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  box-sizing: border-box;
}

h2 {
  margin-bottom: 2rem;
}

.input-field {
  display: none;
}

.input-group {
  position: relative;
  margin-bottom: 1rem;
}

.input-group .input-field {
  font-size: 16px;
  padding: 10px 10px 10px 5px;
  display: block;
  width: 100%;
  border: none;
  border-bottom: 1px solid #515151;
  background: transparent;
  color: white;
}

.input-group .input-field:focus {
  outline: none;
}

.input-group .input-label {
  color: #999;
  font-size: 18px;
  font-weight: normal;
  position: absolute;
  pointer-events: none;
  left: 5px;
  top: 10px;
  display: flex;
}

.input-group .input-label-char {
  transition: 0.2s ease all;
  transition-delay: calc(var(--index) * .05s);
}

.input-group .input-field:focus ~ .input-label .input-label-char,
.input-group .input-field:valid ~ .input-label .input-label-char {
  transform: translateY(-20px);
  font-size: 14px;
  color: #6C8BA6;
}

.input-group .input-bar {
  position: relative;
  display: block;
  width: 100%;
}

.input-group .input-bar:before,
.input-group .input-bar:after {
  content: '';
  height: 2px;
  width: 0;
  bottom: 1px;
  position: absolute;
  background: #6C8BA6;
  transition: 0.2s ease all;
  -moz-transition: 0.2s ease all;
  -webkit-transition: 0.2s ease all;
}

.input-group .input-bar:before {
  left: 50%;
}

.input-group .input-bar:after {
  right: 50%;
}

.input-group .input-field:focus ~ .input-bar:before,
.input-group .input-field:focus ~ .input-bar:after {
  width: 50%;
}

.submit-button {
  width: 100%;
  padding: 0.5em;
  font-size: 1rem;
  color: #fff;
  background-color: #6C8BA6;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #0056b3;
}


.login-link {
  color: #6C8BA6;
  text-decoration: none;
}

.login-link:hover {
  text-decoration: underline;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>

<script>
import { socket } from "../socket";
import AlertModal from "../components/AlertModal.vue";

export default {
  components: {
    AlertModal,
  },
  data() {
    return {
      username: "",
      password: "",
      email: "",
      alertMessage: '',
    };
  },
  methods: {
    async sha256(message) {
      const msgBuffer = new TextEncoder().encode(message);
      const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
      return hashHex;
    },
    async register() {
      console.log("Register")
      const hashedPassword = await this.sha256(this.password);
      socket.emit("register", { username: this.username, password: hashedPassword, email: this.email });
      socket.on("register", (data) => {
        if (data.success) {
          console.log(data.success);
          this.$store.commit("setUserData", data.user);
          this.$router.push("/main");
        } else if (data.error) {
          this.$refs.alertModal.showAlert(data.error);
        }
      });
    },
  },
};
</script>
