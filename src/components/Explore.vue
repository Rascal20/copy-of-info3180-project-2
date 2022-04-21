<template>
        <div class="container py-5 h-100" >
            <div class="row d-flex justify-content-center align-items-center h-100 mt-50">
               
                <h1 class="text-left font-weight-bold">Explore</h1>
                <div v-if="success_msg" class="alert alert-success">
                    {{ success_msg }}
                    
                </div>
                <div class="card  search"> 
                    <form @submit.prevent="searchCars" class="d-flex flex-row justify-content-around justify-content-center align-items-center " >
                        <div class="form-label">
                            <label for="make">Make</label> <br/>
                            <input type="search" class="form-control form-control-lg" name="make" v-model="searchMake" />
                        </div>

                        <div class="form-label">
                            <label for="model">Model</label> <br/>
                            <input type="search" class="form-control form-control-lg" name="model" v-model="searchModel"/>
                        </div>

                        <button class="btn btn-primary btn-lg green btn_search" type="submit">Search</button>
                    </form>
              
                </div>
            </div>
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
    props: ['success_msg'],
    data() {
        return{
            csrf_token: '',
            auth_token: '',
            cars: [],
            searchMake: '',
            searchModel: '',
            success_msg: this.success_msg
        };
    },

    created(){
        this.getCsrfToken();
        this.getCars();
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
                method: 'GET',
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
    padding:4em;
}
.btn_search{
    height: 2.5em;
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

.mt-50{
    margin-top: 5em;
}
</style>