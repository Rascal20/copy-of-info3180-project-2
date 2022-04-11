<template>
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
</template>

<script>
export default {
    name: 'LoginForm',
    data() {
            return {
                csrf_token: ''
            };
    },methods:{
        loginUser(){
            let loginForm = document.getElementById('loginForm');
            let form_data = new FormData(loginForm);
            console.log(this.errors)
            fetch("/api/auth/login", {
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
                        if ('errors' in data){
                            this.isSuccess = false
                        }
                        
                    //this.successmessage = "File Uploaded Successfully"
                    // display a success message
                    console.log(response);
                })
                .catch(function (error) {
                //this.errormessage = "Something went wrong"
                console.log(error);
                });
            },
            getCsrfToken() {
                let self = this;
                fetch('/api/csrf-token')
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    self.csrf_token = data.token;
                    console.log(self.csrf_token);
                    console.log(self.other_data)
                })
            }
    },
     created() {
            this.getCsrfToken();
     }
}
</script>

<style scoped>

</style>
