<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input class="input-field" type="text" v-model="username" placeholder="Username" />
      <input
        class="input-field"
        type="password"
        v-model="password"
        placeholder="Password"
      />
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
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #0056b3;
}

.login-link {
  color: #007bff;
  text-decoration: none;
}

.login-link:hover {
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
    register() {
      socket.emit("register", { username: this.username, password: this.password });
      socket.on("register", (data) => {
        if (data.success) {
          this.$store.commit("setUserData", data.user);
          this.$store.commit("LogIn", true);
          this.$router.push("/main");
        } else {
          alert("Registration failed. Please try again.");
        }
      });
    },
  },
};
</script>
