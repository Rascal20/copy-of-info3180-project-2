<template>

<div v-if="error" class="error">
    <h1>{{ error }}</h1>
</div>
<div v-else-if="user != undefined" class="container py-5 h-100 profile-cont">

<!-- <div class="container py-5 h-100 explore" >
    <div class="card">
        <img :src="user.photo" class="card-img-left"/>
            <div>
            <p> {{ user.name }} </p>
            <p> {{ user.username }}</p>
            <p> {{ user.biography }}</p>

            <p>Email: {{ user.email }}</p>
            <p>Location:  {{ user.location }}</p>
            <p>Joined:  {{ user.date_joined }}</p>
            </div>
        </div>

    </div> -->


    <div class="d-flex  profile">
        <img class="profile_img" :src="user.photo" >
        <!-- <img :src="user.photo" class="card-img-left"/> -->
        <div class="profile_data ">
            <h1> {{ user.name }}</h1>
            <h3 class="text-secondary">{{ user.username }}</h3>
            <p class="text-secondary">  {{ user.biography }} </p>
            <div class="d-flex">
            <div class="text-secondary">
                <p >Email:</p>
                <p >Location:</p>
                <p >Joined: </p>
            </div>
            <div class="mr">
                <p >{{ user.email }} </p> 
                <p > {{ user.location }} </p> 
                <p > {{ user.date_joined }} </p> 
            </div>
            </div>

        </div>
    </div>

    
    <h2>Cars Favourited</h2> 
    
     <div v-if="error" class="error">
        <h1>{{ error }}</h1>
    </div> 

       <div v-else-if="favourites.length" class="grid-container">
        <div  v-for="car in favourites" class="card shadow car-card">
              
                <img :src="'uploads/' + car.photo" class="card-img-top"  alt="Card image cap"/>
                <div class="card-body ">
                  <h5 class="card-title"> {{ car.year }} {{ car.model }} <span class=" text-light price" >  <img src="/src/assets/tag.png" > {{ car.price }} </span> </h5>
                    <p class="text-secondary"> {{ car.make }} </p>

                </div>

            <button @click="$router.push({name:'view-car', params: {car_id: car.id},})" class="btn btn-primary"> View more details </button>            
            </div>
         
        </div> 

   <!--  <div v-else-if="favourites.length" class="grid-container">
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
    </div> -->


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

.profile-cont{
    width: 65%;
}

.profile{
    background-color:white;
    padding: 2em;
    margin-bottom: 3em;
}


.d-flex{
    gap: 2em;
}

.profile_img{
    max-width:  15vw;
    max-height:15vw;
    object-fit:cover;
    border-radius: 100%;
    align-self: top;
}

.profile_data{
    padding: 1em;
}


.grid-container {
    display: grid;
    grid-template-columns: 20vw 20vw 20vw;
    margin-top: 1em;
    gap: 1em;
    width: 100%;
    
}

.card_btn{
    margin:.8em;
}

.card{
    max-width: 100%;
    border-radius: .4em;

}

.mt-50{
    margin-top: 1em;
}

.price{
    background-color: rgb(71, 173, 111);
    padding: .2em .5em;
    border-radius: .2em;
    margin-left:.5em;
}




</style>