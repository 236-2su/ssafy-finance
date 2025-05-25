<template>
  <div class="signup-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-6">
            <div class="signup-card">
              <div class="signup-header">
                <h2 class="signup-title">Join MyFin</h2>
                <p class="signup-subtitle">Create your account to get started</p>
              </div>
              
              <form @submit.prevent="signup" class="signup-form">
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="username" class="form-label">Username *</label>
                      <input
                        id="username"
                        type="text"
                        v-model="username"
                        placeholder="Enter your username"
                        required
                        class="form-control"
                      />
                    </div>
                  </div>
                  
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="email" class="form-label">Email</label>
                      <input
                        id="email"
                        type="email"
                        v-model="email"
                        placeholder="Enter your email"
                        class="form-control"
                      />
                    </div>
                  </div>
                </div>
                
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="password" class="form-label">Password *</label>
                      <input
                        id="password"
                        type="password"
                        v-model="password"
                        placeholder="Enter your password"
                        required
                        class="form-control"
                      />
                    </div>
                  </div>
                  
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="passwordConfirm" class="form-label">Confirm Password *</label>
                      <input
                        id="passwordConfirm"
                        type="password"
                        v-model="passwordConfirm"
                        placeholder="Confirm your password"
                        required
                        class="form-control"
                      />
                    </div>
                  </div>
                </div>
                
                <div class="form-group">
                  <label for="home_address" class="form-label">Home Address</label>
                  <input
                    id="home_address"
                    type="text"
                    v-model="home_address"
                    placeholder="Enter your home address (optional)"
                    class="form-control"
                  />
                </div>
                
                <div class="form-group">
                  <label for="company_address" class="form-label">Company Address</label>
                  <input
                    id="company_address"
                    type="text"
                    v-model="company_address"
                    placeholder="Enter your company address (optional)"
                    class="form-control"
                  />
                </div>
                
                <button type="submit" class="btn btn-primary btn-signup" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Creating Account...' : 'Create Account' }}
                </button>
              </form>
              
              <div v-if="message" class="alert alert-danger mt-3">
                <i class="fas fa-exclamation-circle me-2"></i>
                {{ message }}
              </div>
              
              <div class="signup-footer">
                <p class="text-center">
                  Already have an account? 
                  <router-link to="/login" class="login-link">Sign in here</router-link>
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

const router = useRouter();

const username = ref("");
const email = ref("");
const password = ref("");
const passwordConfirm = ref("");
const home_address = ref("");
const company_address = ref("");
const message = ref("");
const loading = ref(false);

const signup = async () => {
  if (password.value !== passwordConfirm.value) {
    message.value = "Passwords do not match.";
    return;
  }

  loading.value = true;
  message.value = "";

  try {
    await axios.post("/api/accounts/signup/", {
      username: username.value,
      email: email.value || undefined,
      password: password.value,
      home_address: home_address.value || undefined,
      company_address: company_address.value || undefined,
    });
    router.push("/login");
  } catch (err) {
    message.value = "Signup failed: " + (err.response?.data?.detail || "Please try again.");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.signup-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  padding: 40px 0;
}

.hero-section {
  width: 100%;
  padding: 80px 0;
}

.signup-card {
  background: white;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.signup-header {
  text-align: center;
  margin-bottom: 2rem;
}

.signup-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.signup-subtitle {
  color: #666;
  font-size: 1rem;
  margin-bottom: 0;
}

.signup-form {
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

.btn-signup {
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

.btn-signup:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.btn-signup:disabled {
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

.signup-footer {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.login-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .signup-card {
    margin: 1rem;
    padding: 2rem;
  }
  
  .signup-title {
    font-size: 1.5rem;
  }
  
  .hero-section {
    padding: 40px 0;
  }
  
  .row .col-md-6 {
    margin-bottom: 0;
  }
}
</style>
