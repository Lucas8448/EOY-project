<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input class="input-field" type="email" v-model="email" placeholder="Email" />
      <input class="input-field" type="password" v-model="password" placeholder="Password" />
      <transition name="slide-fade">
        <div v-if="email && password">
          <input class="input-field" type="text" v-model="username" placeholder="Username" onkeypress="return event.charCode != 32"/>
        </div>
      </transition>
      <button class="submit-button" type="submit">Register</button>
    </form>
    <p>
      Already have an account? <router-link class="login-link" to="/">Login</router-link>
    </p>
  </div>
</template>


<style scoped>
.register {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  box-sizing: border-box;
}

h2 {
  margin-bottom: 2rem;
}

.input-field {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1rem;
  outline: none;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.submit-button {
  width: 100%;
  padding: 0.5rem;
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
export default {
  data() {
    return {
      username: "",
      password: "",
      email: ""
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
          alert(data.error);
        }
      });
    },
  },
};
</script>
