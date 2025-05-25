<template>
  <div class="login-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-5">
            <div class="login-card">
              <div class="login-header">
                <h2 class="login-title">Welcome Back</h2>
                <p class="login-subtitle">Sign in to your MyFin account</p>
              </div>
              
              <form @submit.prevent="login" class="login-form">
                <div class="form-group">
                  <label for="username" class="form-label">Username</label>
                  <input
                    id="username"
                    type="text"
                    v-model="username"
                    placeholder="Enter your username"
                    required
                    class="form-control"
                  />
                </div>
                
                <div class="form-group">
                  <label for="password" class="form-label">Password</label>
                  <input
                    id="password"
                    type="password"
                    v-model="password"
                    placeholder="Enter your password"
                    required
                    class="form-control"
                  />
                </div>
                
                <button type="submit" class="btn btn-primary btn-login" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Signing in...' : 'Sign In' }}
                </button>
              </form>
              
              <div v-if="error" class="alert alert-danger mt-3">
                <i class="fas fa-exclamation-circle me-2"></i>
                {{ error }}
              </div>
              
              <div class="login-footer">
                <p class="text-center">
                  Don't have an account? 
                  <router-link to="/signup" class="signup-link">Sign up here</router-link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";

const router = useRouter();
const userStore = useUserStore();

const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

const login = async () => {
  loading.value = true;
  error.value = "";
  
  try {
    const res = await axios.post("/api/accounts/login/", {
      username: username.value,
      password: password.value,
    });
    userStore.login(res.data.username);
    router.push("/");
  } catch (err) {
    error.value = "Login failed: Please check your username and password.";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
}

.hero-section {
  width: 100%;
  padding: 80px 0;
}

.login-card {
  background: white;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.login-subtitle {
  color: #666;
  font-size: 1rem;
  margin-bottom: 0;
}

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.form-control {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-control::placeholder {
  color: #adb5bd;
}

.btn-login {
  width: 100%;
  padding: 0.875rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  transition: all 0.3s ease;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.alert {
  border-radius: 10px;
  border: none;
  padding: 1rem;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}

.login-footer {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.signup-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.signup-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-card {
    margin: 1rem;
    padding: 2rem;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
  
  .hero-section {
    padding: 40px 0;
  }
}
</style>
