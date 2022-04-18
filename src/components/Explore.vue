<template>
    <div class="card  search"> 
        <form @submmit.prevent="searchCars" class="d-flex flex-row" >
            <div class="">
                <label for="make">Make</label>
                <input type="search" name="make" v-model="searchMake" />
            </div>

            <div class="">
                <label for="model">Model</label>
                <input type="search" name="model" v-model="searchModel"/>
            </div>

            <button class="btn btn-primary green" type="submit">Search</button>
        </form>
    </div>

    <div class="grid-container">
        <div v-for="car in cars" class="card shadow car-card">
            <img :src="'uploads/' + car.photo" class="card-img-top"/>
            <div class="card-body">
                <p class="card-title"> {{ car.year }}</p>
                <p> {{ car.model }}</p>
                <p> {{ car.price }}</p>
                <p> {{ car.make }}</p>
            </div>

            <button @click="$router.push({name:'view-car', params: {car_id: car.id},})" class="btn btn-primary"> View more details </button>
        </div>
    </div>
    
</template>

<script>
export default {
    data() {
        return{
            csrf_token: '',
            auth_token: '',
            cars: [],
            searchMake: '',
            searchModel: ''
        };
    },

    created(){
        this.getCsrfToken();
        this.getCars();
        //this.getAuthToken();
    },


    methods:{
        getCsrfToken() {
            let self = this;
            fetch("/api/csrf-token")
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                self.csrf_token = data.token;
                console.log(self.other_data)
            })
        },

        getAuthToken(){
            let self = this;

            fetch("/api/auth/login")
                .then((response) => response.json())
                .then((data) => {
                    self.auth_token = data.token;
                    console.log(data.token);
                })
        },


        getCars(){
            let self = this;
            fetch("/api/cars", {
                method: 'GET',
                headers: {
                    'X-CSRFToken': self.csrf_token,
                    //'Authorization': `Bearer ` + self.auth_token
                }
            })
                .then(function(response) {
                    return response.json();
                })
                .then(function(data) {
                    console.log(data);
                    self.cars = data.cars;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        searchCars() {
            let self = this;

            fetch('api/search?make='+ self.searchMake + '&model='+ self.searchModel,{
                headers:{
                    'X-CSRFToken': this.csrf_token
                    //'Authorization': `Bearer ${import.meta.env.VITE_API_TOKEN}`,
                }
            })
                .then(function(response){
                return response.json();
            })
                .then(function(data){
                console.log(data);
                self.cars = data.cars;
            });
        }
    }
}

</script>


<style>
.search{
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