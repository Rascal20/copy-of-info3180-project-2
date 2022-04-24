<template>
    <div class="card container  h-100  flex-row flex-nowrap car-details-cont">
        <div class="car_img_div">
            <img :src="'/uploads/' + car.photo"  class="car_details_img" /> 
        </div>
        
        <div class="car-info ">
            <h2> {{ car.year }} {{ car.make }}</h2>
            <h3 class="text-secondary"> {{ car.model }} </h3>
            <p class="text-secondary desc"> {{ car. description }}
            </p>
            <br>
            <br>
            <div class="d-flex ">
                <div class="mr-auto p-2">
                <p> Colour: {{ car.colour }} </p>
                <p> Price: {{ car.price }} </p>
                </div>

                <div class="p-2">
                <p> Body Type: {{ car.car_type }}</p>
                <p>Transmission: {{ car.transmission}} </p>
                </div>

            </div>
            <div class="d-flex justify-content-between">
            <button class="btn btn-primary green"> Email owner </button>

            <button v-if="isFavourite === true" @click.prevent="removeFromFavourites" class="fav">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
                </svg></button>

            <button v-else-if="isFavourite === false" @click.prevent="addToFavourites" class="fav ">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
                </svg>
            </button>
            </div>

        </div>

        
    </div>
</template>

<script>
export default {
    data() {
        return{
            csrf_token: '',
            car: {},
            isFavourite: false,
        };
    },

    created(){
        this.getCsrfToken();
        this.getCar();
        if (!localStorage.getItem(this.$route.params.car_id)){ 
            this.isFavourite=false;
            console.log(this.isFavourite);
        }
        else{
            this.isFavourite=true;
            console.log(this.isFavourite);
        }
        
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

        getCar(){
            let car_id = this.$route.params.car_id;
            let self = this;

            fetch("/api/cars/" + car_id, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': this.csrf_token,
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                }
            })
                .then(function(response) {
                    return response.json();
                })
                .then(function(data) {
                    console.log(data);
                    self.car = data.data;

                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        addToFavourites(){
            let car_id = this.$route.params.car_id;
            let self = this;

            fetch("/api/cars/" + car_id + "/favourite", {
                method: 'POST',
                //body: JSON.stringify({car_id: car_id, user_id: "1"}),
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': this.csrf_token,
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                }
            })
                .then(function(response) {
        
                    return response.json();

                })
                .then(function(data) {
                    console.log(data);
                    localStorage.setItem(car_id, "1");
                    self.isFavourite = true;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },

        removeFromFavourites(){
            let car_id = this.$route.params.car_id;

            fetch("/api/cars/" + car_id + "/favourite/remove",{
                method: 'POST',
                body: JSON.stringify({car_id: car_id, user_id: 1}),
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': this.csrf_token,
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                }
            })
                .then(function(response) {
        
                    return response.json();

                })
                .then(function(data) {
                    console.log(data);
                    localStorage.removeItem(car_id);
                    self.isFavourite = false;
                    console.log(self.isFavourite);

                })
                .catch(function (error) {
                    console.log(error);
                });
        }

    }
}
</script>

<style>

.card{
    margin-top: 60px;
    
}

.car-details-cont{
    width:65vw;

}

.container{
    padding-left: 0px;
    border-radius: .5em;
}

.car-info{
    align-items: stretch;
    padding-top:2em;
}

.btns{
    justify-content: flex-end;
}

.car_img_div{
    margin-right: 2em;
    overflow:hidden;
}
.car_details_img{
    max-width: 50vw;
    object-fit:cover;
    border-radius: .5em 0em 0em .5em;
   
}

.desc{
    max-width:70%;
}
.d-flex{
    gap:.5em;
}
.fav{
    background-color:white;
    border-radius: 100%;
    border: 1px solid black;
    
    width:40px;
    height:40px;
}
</style>