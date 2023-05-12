<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input class="input-field" type="text" v-model="email" placeholder="Email" />
      <input
        class="input-field"
        type="password"
        v-model="password"
        placeholder="Password"
      />
      <button class="submit-button" type="submit">Login</button>
    </form>
    <p>
      Don't have an account?
      <router-link class="register-link" to="/register">Register</router-link>
    </p>
  </div>
</template>

<style scoped>
.login {
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
export default {
  data() {
    return {
      email: "",
      password: "",
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
          alert(data.error);
        }
      });
    },
  },
};
</script>
