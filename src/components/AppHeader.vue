<template>
  <header>


  
      <nav class="navbar  navbar-dark bg-dark fixed-top ">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">
        <img src="/src/assets/logo.png" width="24" height="24" class="d-inline-block align-center" alt="logo">
        United Auto Sales</a>
      <!--  <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button> -->

        <!--  When Logged in -->
         <div id="navbarSupportedContent" >
          <ul class="nav ">
            <li class="nav-item">
              <RouterLink to="/cars/new" class="nav-link" >Add Car</RouterLink>
            </li>
            <li class="nav-item ">
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item ">
              <RouterLink class="nav-link" to="/user">My Profile</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Logout</RouterLink>
            </li>
          </ul>

       <!--  When Logged out -->
        <div id="navbarSupportedContent">
<<<<<<< HEAD
          <ul class="nav justify-content-end" >
=======
          <ul class="nav justify-content-end">
            
>>>>>>> 6130fb65c6d0d2d4820049b915552a93e42b06b4
            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>
          </ul>
        </div>
<<<<<<< HEAD
        </div>
=======


        </div>
      </div>
>>>>>>> 6130fb65c6d0d2d4820049b915552a93e42b06b4
    </nav>
 

  </header>
</template>

<script>
import { RouterLink } from "vue-router";
import LoginForm from '@/components/LoginForm.vue'

export default {
    data() {
      return {}        
    },
    created() {
      this.checkLog();
    },
    methods: {
      checkLog() {
        let check = localStorage.getItem('user');
        console.log(check);

      }
    }
}
</script>

<style>



</style>