<template>
  <div class="register-page">
    <h2>Register</h2>
    <form class="register-form">
      <!-- Registration form fields -->
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" />
      </div>
      <button class="register-button" @click="register">Register</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'RegisterComponent',
  data() {
    return {
      username: '',
      password: '',
      id:''
    };
  },
  methods: {
    async register() {
      try {
        // Send registration data to the server
        const response = await fetch("http://localhost:8000/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
            id:this.id
          })
        });

        if (response.ok) {
          console.log("Registration successful");
        } else {
          console.error("Registration failed");
        }
      } catch (error) {
        console.error("An error occurred:", error);
      }
    }
  }
};
</script>

<style scoped>
.register-page {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f7f7f7;
  border-radius: 10px;
  box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.register-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
}

input[type="text"],
input[type="password"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
}

.register-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.register-button:hover {
  background-color: #0056b3;
}

/* Add additional styling to enhance the form's appearance */
</style>