<template>
  <div class="login-form">
    <h2>Login</h2>
    <form @submit.prevent="login">
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
      <button class="submit-button" type="submit">
        Login
      </button>
    </form>
    <p>
      Don't have an account?
      <router-link class="register-link" to="/register">Register</router-link>
    </p>
  </div>
  <div class="container">
    <div class="tree">
      <div class="branch" style="--x:0">
        <span style="--i:0;"></span>
        <span style="--i:1;"></span>
        <span style="--i:2;"></span>
        <span style="--i:3;"></span>
      </div>
      <div class="branch" style="--x:1">
        <span style="--i:0;"></span>
        <span style="--i:1;"></span>
        <span style="--i:2;"></span>
        <span style="--i:3;"></span>
      </div>
      <div class="branch" style="--x:2">
        <span style="--i:0;"></span>
        <span style="--i:1;"></span>
        <span style="--i:2;"></span>
        <span style="--i:3;"></span>
      </div>
      <div class="branch" style="--x:3">
        <span style="--i:0;"></span>
        <span style="--i:1;"></span>
        <span style="--i:2;"></span>
        <span style="--i:3;"></span>
      </div>
      <div class="stem">
        <span style="--i:0;"></span>
        <span style="--i:1;"></span>
        <span style="--i:2;"></span>
        <span style="--i:3;"></span>
      </div>
      <span class="shadow"></span>
    </div>
  </div>
  <alert-modal ref="alertModal"></alert-modal>
</template>

<style scoped>
.container {
  position: absolute;
  top: 80vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.tree {
  position: relative;
  width: 50px;
  height: 50px;
  transform-style: preserve-3d;
  transform: rotateX(-20deg) rotateY(30deg);
  animation: treeAnimate 5s linear infinite;
}

@keyframes treeAnimate {
  0% {
    transform: rotateX(-20deg) rotateY(360deg);
  }

  100% {
    transform: rotateX(-20deg) rotateY(0deg);
  }
}

.tree div {
  position: absolute;
  top: -50px;
  left: 0;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transform: translateY(calc(25px * var(--x))) translateZ(0px);
}

.tree div.branch span {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #69c069, #77dd77);
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
  border-bottom: 5px solid #00000019;
  transform-origin: bottom;
  transform: rotateY(calc(90deg * var(--i))) rotateX(30deg) translateZ(28.5px);
}

.tree div.stem span {
  position: absolute;
  top: 110px;
 /* updated top value */
  left: calc(50% - 7.5px);
  width: 15px;
  height: 50%;
  background: linear-gradient(90deg, #bb4622, #df7214);
  border-bottom: 5px solid #00000019;
  transform-origin: bottom;
  transform: rotateY(calc(90deg * var(--i))) translateZ(7.5px);
}

.shadow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  filter: blur(20px);
  transform-style: preserve-3d;
  transform: rotateX(90deg) translateZ(-65px);
}

.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1200px;
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

.register-link {
  color: #6C8BA6;
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
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
      email: "",
      password: "",
      alertMessage: '',
    };
  },
  methods: {
    async sha256(message) {
      const hashHex = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(message)))).map(b => b.toString(16).padStart(2, '0')).join('');
      return hashHex;
    },
    async login() {
      console.log("Login")
      const hashedPassword = await this.sha256(this.password);
      socket.emit("login", { email: this.email, password: hashedPassword });
      socket.on("login", (data) => {
        console.log("response")
        if (data.success) {
          this.$store.commit("setUserData", data.user);
          console.log("Redirecting")
          this.$router.push("/main");
        } else if (data.error) {
          this.$nextTick(() => {
            this.$refs.alertModal.showAlert(data.error);
          });
        }
      });
    },
  },
};
</script>