<template>
  <header>


  
      <nav class="navbar  navbar-dark bg-dark fixed-top ">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">
        <img src="./assets/logo.png" width="24" height="24" class="d-inline-block align-center" alt="lo">
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
        <div id="navbarSupportedContent">
          <ul class="nav justify-content-end">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link" >Home</RouterLink>
            </li>
            <li class="nav-item active">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
            <li class="nav-item active">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
 

  </header>
</template>

<script>
import { RouterLink } from "vue-router";
</script>

<style>

.nav-link{
  color: white;
}

</style>