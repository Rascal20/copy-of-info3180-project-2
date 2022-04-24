<template>
 <!--
    <div>
        <h2> Login to your account </h2>
        <div  v-if="isSuccess">
             </div>

        <form @submit.prevent="loginUser" id="loginForm">
        <div class="form-group">
        
            <label> Username </label><br>
            <input type="text" name="username"><br>

            <label> Password </label><br>
            <input type="password" name="password"><br>

        </div>
        <button type="submit" class="btn btn-primary mb-2" > Login </button>
        </form>
    </div>
   -->

     <section class="vh-80" >
      
      <div class="container py-5 h-100">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col-12 col-md-8 col-lg-6 col-xl-5 ">

            <h3 class="mb-5 text-center">Login to your account</h3>
            <div v-if="success_msg" class="alert alert-success">
                {{ success_msg }}
            </div>
            <div v-if="errors_exist == 1" class="alert alert-danger">
                <ul>
                    <li v-for= "error in errors">{{ error }}</li>
                </ul>
            </div>
            <div class="card shadow-2-strong" >
              
              <div class="card-body p-5 text-left">
    
                <form  @submit.prevent="loginUser" id="loginForm" enctype="multipart/form-data">
                    <div class="form-group">
                <div class="form-outline mb-4">
                  <label class="form-label" for="typeEmailX">Username</label>
                  <input type="text" id="typeEmailX" class="form-control form-control-lg" name="username"/>
                  
                </div>
    
                <div class="form-outline mb-4">
                  <label class="form-label" for="typePasswordX">Password</label>
                  <input type="password" id="typePasswordX" class="form-control form-control-lg" name="password" />
                 
                </div>
    
               
    
                <button class="btn btn-primary btn-lg btn-block" type="submit">Login</button>
                </div>
                 </form>
              </div>
            </div>
          </div>
        </div>
        </div>
        </section>
 
</template>


<script>
export default {
    name: 'LoginForm',
    data() {
            return {
                csrf_token: '',
                success_msg: '',
                errors: [],
                errors_exist: 0
            };
    },
    created() {
            this.getCsrfToken();
    },

    methods: {
        loginUser(){
            let self = this;
            let loginForm = document.getElementById('loginForm');
            let form_data = new FormData(loginForm);
            self.errors_exist = 0
            fetch("/api/auth/login", {
                method: 'POST',
                body: form_data,
                headers: {
                    'X-CSRFToken': this.csrf_token
                }
            })
            .then(function (response) {
                console.log(response.status)
                if (response.status != 200){
                    self.errors_exist = 1;
                }
                return response.json();
            })
            .then(function (data) {
                // display a success message
                console.log(data);
                if(self.errors_exist == 0){
                    //self.success_msg= data.message;
                    self.$router.push({name:'explore'});
                    localStorage.setItem('user_id', data.data.id);
                    localStorage.setItem('auth_token', data.data.token);
                    self.emitter.emit('isLoggedIn', {'eventContent': 'User logged in!'});
                }
                else {
                  self.errors = data.errors;
                }
            })
            .catch(function (error) {
                console.log(error);
            });  
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

<style scoped>


.card{
  border-radius: .5rem;
}

.btn-primary{
  background-color: rgb(71, 173, 111);
  border:none;

}

.btn-block{
  width: 100%;
}

h3{
  padding-top: 100px;
}

</style>
