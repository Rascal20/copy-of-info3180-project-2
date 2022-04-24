<template>
  <header>
      <nav class="navbar  navbar-dark bg-dark fixed-top ">
      <div class="container-fluid">
        <a class="navbar-brand" :href="icon_path">
        <img src="/src/assets/logo.png" width="24" height="24" class="d-inline-block align-center" alt="logo">
        United Auto Sales</a>
        <div id="navbarSupportedContent" v-if="isLoggedIn()==false & logged_out==true & logged_in == false">
          <ul class="nav justify-content-end" >
            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>
          </ul>
        </div>
        <div id="navbarSupportedContent" v-else>
          <ul class="nav justify-content-end">
            <li class="nav-item">
              <RouterLink to="/cars/new" class="nav-link" >Add Car</RouterLink>
            </li>
            <li class="nav-item ">
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item ">
              <RouterLink class="nav-link" :to="{name:'profile', params: {user_id: user_id}}">My Profile</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink @click="logout()" class="nav-link" to="/logout">Logout</RouterLink>
            </li>
          </ul>
        </div>
      </div>

</nav>
 

  </header>
</template>

<script>
import { RouterLink } from "vue-router";
export default {
    data() {
      return {
        csrf_token: '',
        user_id: localStorage.getItem('user_id'),
        logged_out: true,
        icon_path: '/',
        logged_in: localStorage.getItem('auth_token') != null
      };     
    },
    created() {
            this.getCsrfToken();
            this.isLoggedIn();
            this.emitter.on('isLoggedIn', (evt)  => {
              console.log("event");
              console.log(evt.eventContent);
              this.isLoggedIn();
            })
    },
    methods: {
      isLoggedIn() {
        if (localStorage.getItem('auth_token') === null){
          console.log('User is not Logged in!');
          return false;
        }
        else{
          console.log('User is logged in!');
          this.logged_in = true;
          this.logged_out = false;
          this.icon_path = '/explore';
          this.user_id = localStorage.getItem('user_id')
          return true;
        }
      },
      logout(){
        let self = this;
        fetch("/api/auth/logout", {
                method: 'POST',
                //body:{} ,
                headers: {
                  'X-CSRFToken': this.csrf_token,
                  'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                }
            })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                localStorage.removeItem('auth_token');
                localStorage.removeItem('user_id');
                self.logged_out = true;
                self.logged_in = false;
                self.icon_path = '/';
                self.$router.push('/'); 
            })
      },
      getCsrfToken() {
            let self = this;
            fetch('/api/csrf-token')
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                self.csrf_token = data.csrf_token;
            })
      }
    }
}
</script>

<style>
</style>