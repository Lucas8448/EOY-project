<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input class="input-field" type="text" v-model="username" placeholder="Username" />
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
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #0056b3;
}

.register-link {
  color: #007bff;
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
}
</style>

<script>
import socket from "../socket";
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    login() {
      socket.emit("login", { username: this.username, password: this.password });
      socket.on("login", (data) => {
        if (data.error) {
          alert(data.error);
        } else {
          this.$store.commit("setUserData", data.user);
          this.$store.commit("LogIn", true);
          this.$router.push("/main");
        }
      });
    },
  },
};
</script>
