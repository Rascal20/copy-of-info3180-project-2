<template>
    <div class="form container">
        <div v-if="success_msg" class="alert alert-success">
            {{ success_msg }}
        </div>
        <div v-if="errors.length!=0" class="alert alert-danger">
            <ul>
                <li v-for="error in errors">{{ error }}</li>
            </ul>
        </div>

    
        <form @submit.prevent="addCar" id="carForm" method="post" enctype="multipart/form-data" class="d-flex flex-column">
            <label for="make">Make</label>
            <input type="text" name="make" placeholder="Enter make of car"/>
            
             <label for="model">Model</label>
            <input type="text" name="model" placeholder="Enter model of car"/>

             <label for="colour">Colour</label>
            <input type="text" name="colour" placeholder="Enter colour of car"/>

             <label for="year">Year</label>
            <input type="text" name="year" placeholder="Enter year of car"/>

             <label for="price">Price</label>
            <input type="text" name="price" placeholder="Enter price of car"/>

             <label for="car_type">Type</label>
            <input type="text" name="car_type" placeholder="Enter type of car"/>

             <label for="transmission">Transmission</label>
            <select type="text" name="transmission" >
                <option value="manual">Manual</option> 
                <option value="automatic">Automatic</option> 
                <option value="cvt">CVT Transmission </option>
            </select>

             <label for="description">Description</label>
            <textarea name="description" placeholder="Enter description"></textarea>

            <input type="file" name="photo"/>
            <button class="btn btn-primary" type="submit"> Submit </button>

        </form>
    </div>
</template>

<script>
export default {
    data() {
        return{
            csrf_token: '',
            auth_token: '',
            //car_types: []
            success_msg: '',
            errors: []
        };
    },

    created(){
        this.getCsrfToken();
        this.getAuthToken();
        //this.getCarTypes();
    },


    methods:{
        addCar() {
			let carForm = document.getElementById('carForm');
            let form_data = new FormData(carForm);
            let self = this;
			
			fetch("/api/cars", {
				method: 'POST',
                body: form_data,
                headers: {
                    'X-CSRFToken': this.csrf_token,
                    'Authorization': `Bearer ` + this.auth_token
                }
			})
			.then(function (response){
                return response.json();
            })
			.then(function (data){
                console.log(data);
                if(data.message != undefined){
                    self.success_msg= data.message;
                }else{
                    self.errors = data;
                }
            })
			.catch(function (error){
				console.log(error);
			});
		},

        getCsrfToken() {
            let self = this;
            fetch("/api/csrf-token")
                .then((response) => response.json())
                .then((data) => {
                    this.csrf_token = data.token;
                    //console.log(data);
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
        }


        /*getCarTypes(){
            let self=this;
            fetch("/api/car_types")
                .then((response) => response.json())
                .then((data)=> {
                    console.log(data);
                    self.car_types = data.car_types;
                })
        }*/

    }
}
</script>


<style>
.form{
    margin-top: 80px;
}
</style>