<template>
    <div class="card">
        <img :src="'/uploads/' + car.photo"/>
        <h1> {{ car.year }} {{ car.make }}</h1>
        <p> {{ car.model }}</p>
        <p> {{ car. description }}</p>
        <p> Colour: {{ car.colour }}</p>
        <p> Body Type: {{ car.car_type }}</p>
        <p> Price: {{ car.price }}</p>
        <p>Transmission: {{ car.transmission}}</p>

        <button> Email owner </button>

        <button v-if="isFavourite === true" @click.prevent="removeFromFavourites">Favourite</button>

        <button v-else-if="isFavourite === false" @click.prevent="addToFavourites">Favourite</button>

        
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
                self.csrf_token = data.token;
            })
        },

        getCar(){
            let car_id = this.$route.params.car_id;
            let self = this;

            fetch("/api/cars/" + car_id, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': this.csrf_token,
                    //'Authorization': `Bearer ` + localStorage.getItem('auth_token')
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
                body: JSON.stringify({car_id: car_id, user_id: "1"}),
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': this.csrf_token,
                    //'Authorization': `Bearer ` + localStorage.getItem('auth_token')
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
                    //'Authorization': `Bearer ` + localStorage.getItem('auth_token')
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

img{
    width: 200px;
}
</style>