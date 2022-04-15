<template>
<div v-if="error" class="error">
    <h1>{{ error }}</h1>
</div>
<div v-else-if="user != undefined" class="container">
    <div class="card">
        <img :src="user.photo" class="card-img-left"/>
        <p> {{ user.name }} </p>
        <p> {{ user.username }}</p>
        <p> {{ user.biography }}</p>

        <p>Email: {{ user.email }}</p>
        <p>Location:  {{ user.location }}</p>
        <p>Joined:  {{ user.date_joined }}</p>

    </div>

    <h2>Cars Favourited</h2> 
    <div v-if="error" class="error">
        <h1>{{ error }}</h1>
    </div>
    <div v-else-if="favourites.length" class="grid-container">
        <div v-for="car in favourites" class="card shadow car-card">
            <img :src="car.photo" class="card-img-top"/>
            <div class="card-body">
                <p class="card-title"> {{ car.year }}</p>
                <p> {{ car.model }}</p>
                <p> {{ car.price }}</p>
                <p> {{ car.make }}</p>
            </div>

            <button @click="$router.push({name:'view-car', params: {car_id: car.id},})" class="btn btn-primary"> View more details </button>
        </div>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return{
            csrf_token: '',
            auth_token: '',
            user: {} ,
            favourites: [],
            error: ''
        };
    },

    created(){
        this.getCsrfToken();
        this.getUserProfile();
        this.getFavourites();
    },


    methods:{
        getCsrfToken() {
            let self = this;
            fetch("/api/csrf-token")
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                self.csrf_token = data.token;
            })
        },

        getAuthToken() {
            let self = this;

            fetch("/api/auth/login")
                .then((response) => response.json())
                .then((data) => {
                    self.auth_token = data.token;
                    console.log(data.token);
                })
        },

        getUserProfile() {
            let user_id = this.$route.params.user_id;
            let self= this;

            fetch("/api/users/" + user_id, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': this.csrf_token,
                    //'Authorization': `Bearer ` + auth_token
                }
            })
                .then(function(response) {
                    return response.json();
                })
                .then(function(data) {
                    if(data.message == undefined){
                        console.log(data);
                        self.user = data.data;
                    }else{
                       self.error= data.message;
                       console.log(data.message);
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        getFavourites(){
            let user_id = this.$route.params.user_id;
            let self = this;

            fetch("/api/users/" + user_id + "/favourites", {
                method: 'GET',
                headers: {
                    'X-CSRFToken': this.csrf_token,
                    //'Authorization': `Bearer ` + auth_token
                }
            })
                .then(function(response) {
                    return response.json();
                })
                .then(function(data) {
                    console.log(data);
                    if (data.message != undefined){
                        console.log(data.message);
                        self.error = data.message;
                    }else {
                        console.log(data);
                        self.favourites = data.data;
                    }

                })
                .catch(function (error) {
                    console.log(error);
                });
        }

    }
}

</script>


<style>
.container{
    margin-top: 60px;
}

.error{
    margin-top: 60px;
}

.grid-container {
    display: grid;
    grid-template-columns: auto auto auto;
    padding: 10px;
    gap: 10px 10px;
    width: 100%
}

.car-card{
    max-width: 350px;
    max-height: fit-content;
}
</style>