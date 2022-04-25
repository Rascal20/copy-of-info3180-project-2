<template>
    <div class="container py-5 h-100 explore" >
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
        

        <div class=" grid-container">

             <div  v-for="car in cars" class="card shadow car-card">
                <!-- <img class="card-img-top" src="/src/assets/homeimg.jpeg"> -->
                <img :src="'../uploads/' + car.photo" class="card-img-top"  alt="Card image cap"/>
                <div class="card-body ">
                  <h5 class="card-title"> {{ car.year }} {{ car.model }} <span class=" text-light price" >  <img src="/src/assets/tag.png" > {{ car.price }} </span> </h5>
                    <p class="text-secondary"> {{ car.make }} </p>

                   <!--  <h5 class="card-title ">Year Model <span class=" text-light price " >    <img src="/src/assets/tag.png" > $389506</span></h5>
                    
                    <p class="text-secondary">Make</p> -->
                </div>

             <button @click="$router.push({name:'view-car', params: {car_id: car.id}})" class="btn btn-primary card_btn"> View more details </button>
               <!--  <button class="btn btn-primary card_btn">View more details</button> -->
            </div>
         
   
        
        </div>

    </div>
    
</template>

<script>
export default {
    props: ['success_msg'],
    data() {
        return{
            csrf_token: '',
            cars: [],
            searchMake: '',
            searchModel: '',
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
                self.csrf_token = data.csrf_token;
            })
        },

        getCars(){
            let self = this;
            fetch("/api/cars", {
                method: 'GET',
                headers: {
                    'X-CSRFToken': self.csrf_token,
                    'Authorization': 'Bearer  ' + localStorage.getItem('auth_token')
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
                    'X-CSRFToken': this.csrf_token,
                    'Authorization': 'Bearer  ' + localStorage.getItem('auth_token')
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

.explore{
    width: 65%;
}

.search{
    padding: 3em;
    border-radius: .5em;
}

.btn_search{
    margin-top: .65em;
    height: 2.5em;
}
.grid-container {
    display: grid;
    grid-template-columns: 20vw 20vw 20vw;
    margin-top: 3em;
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

.container{ 
    margin-top: 0; 
}
</style>