<template>
    <!--
    <div class="form-container">
        <h1>Register New User</h1>
        <form @submit.prevent="register" id="registerForm" method="POST" enctype="multipart/form-data">
            <div class="form-row">
                <div class="form-group">
                    <label>Username</label><br>
                    <input type="text" name="username">
                </div>
                <div class="form-group">
                    <label>Password</label><br>
                    <input type="password" name="password">
                </div>
            </div>

             <div class="form-row">
                <div class="form-group">
                    <label>Fullname</label><br>
                    <input type="text" name="fullName">
                </div>
                <div class="form-group">
                    <label>Email</label><br>
                    <input type="text" name="email">
                </div>
            </div>

            <div class="form-group">
                <label> Location </label><br>
                <input type="text" name="location">
            </div>

            <div class="form-group">
                <label> Biography </label><br>
                <textarea name="biography"></textarea>
            </div>

            <div class="form-group">
                <label> Upload Photo </label>
                <input type="file" name="photo">
            </div>

            <button type="submit" name="submit" class="form-btn">Register</button>
        </form>
    </div>

    -->
        <section class="vh-80" >
      
      <div class="container py-5 h-100" >
        <div class="row d-flex justify-content-center align-items-center h-100">
         <div class="col-12 col-md-8 col-lg-6 col-xl-5 " > 

           <h1 class="text-left">Register New User</h1>
            <div class="card card-reg shadow-2-strong" >
              
              <div class="card-body p-5 text-left">
    
                <form  @submit.prevent="register" id="registerForm" method="POST" enctype="multipart/form-data" class="row g-3">
                <div class="form-group-reg">

                
                
                <div class="form-outline mb-4 ">
                  <label class="form-label" >Username</label>
                  <input type="text" class="form-control form-control-lg" name="username"/>
                  
                </div>
    
                <div class="form-outline mb-4 ">
                  <label class="form-label" >Password</label>
                  <input type="password"  class="form-control form-control-lg" name="password" />
                 
                </div>

                <div class="form-outline mb-4">
                  <label class="form-label" >Fullname</label>
                  <input type="text" class="form-control form-control-lg" name="fullName"/>
                  
                </div>
    
                <div class="form-outline mb-4">
                  <label class="form-label" >Email</label>
                  <input type="text"  class="form-control form-control-lg" name="email" />
                 
                </div>

                <div class="form-outline mb-4">
                  <label class="form-label" >Location</label>
                  <input type="text"  class="form-control form-control-lg" name="location" />
                 
                </div>

                <div class="form-outline mb-4 bio">
                  <label class="form-label" >Biography</label>
                  <textarea type="password"  class="form-control form-control-lg" name="biography" ></textarea>
                 
                </div>
                
               <div class="form-outline mb-4 upload">
                  <label class="form-label" >Upload Photo</label>
                  <input type="file"  class="form-control form-control-lg" name="photo" style="border:none;" />
                 
                </div>
    
                <button class="btn btn-primary btn-lg btn-block reg" type="submit">Register</button>
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
    data() {
        return{
            csrf_token: ''
        };
    },
    created() {
        this.getCsrfToken();
    },
    methods: {
        register() {
            let registerForm = document.getElementById('registerForm');
            let form_data = new FormData(registerForm);
            fetch("/api/register", {
                method: 'POST',
                body: form_data,
                headers: {
                    'X-CSRFToken': this.csrf_token
                }
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                // display a success message
                console.log(data);
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

<style>
.card-reg{
 
  border-radius: .5rem;
}

.btn-primary{
  background-color: rgb(71, 173, 111);
  border:none;

}

.btn-block{
  width: 60%;
}

.form-group-reg{
    display:grid;
    grid-template-columns: 50% 50% ;
    column-gap: 2rem;

}

.bio{
    grid-area: 4/span 2;
}

.upload{
    grid-area: 5/span 2;
}

.reg{
    grid-area: 6;
}

.text-left{
    padding-top: 30px;
    padding-bottom: 20px;
}

</style>