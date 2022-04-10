<template>
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
                    <input type="text" name="fullname">
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
                <textarea name="bio"></textarea>
            </div>

            <div class="form-group">
                <label> Upload Photo </label>
                <input type="file" name="photo">
            </div>

            <button type="submit" name="submit" class="form-btn">Register</button>
        </form>
    </div>
</template>

<script>
export default {
    data(){
        return{
            csrf_token: ''
        }
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
</style>