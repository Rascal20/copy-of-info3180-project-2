<template>
   <!--  
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
       -->

    <section class="vh-80" >
      
      <div class="container py-5 h-100" >
        <div class="row d-flex justify-content-center align-items-center h-100">
         <div class="col-12 col-md-8 col-lg-6 col-xl-5 " > 

           <h1 class="text-left">Add New Car</h1>
            <div v-if="success_msg" class="alert alert-success">
                {{ success_msg }}
                
            </div>
            <div v-if="errors.length!=0" class="alert alert-danger">
                <ul>
                    <li v-for="error in errors">{{ error }}</li>
                </ul>
            </div>
            
            <div class="card card-reg shadow-2-strong" >
              
              <div class="card-body p-5 text-left">
    
                <form  @submit.prevent="addCar" id="carForm" method="POST" enctype="multipart/form-data" class="row g-3">
                <div class="form-group-reg">

              
                
                <div class="form-outline mb-4 ">
                  <label class="form-label" >Make</label>
                  <input type="text" class="form-control form-control-lg" name="make"/>
                  
                </div>
    
                <div class="form-outline mb-4 ">
                  <label class="form-label" >Model</label>
                  <input type="text"  class="form-control form-control-lg" name="model" />
                 
                </div>

                <div class="form-outline mb-4">
                  <label class="form-label" >Colour</label>
                  <input type="text" class="form-control form-control-lg" name="colour"/>
                  
                </div>
    
                <div class="form-outline mb-4">
                  <label class="form-label" >Year</label>
                  <input type="text"  class="form-control form-control-lg" name="year" />
                 
                </div>

                <div class="form-outline mb-4">
                  <label class="form-label" >Price</label>
                  <input type="text"  class="form-control form-control-lg" name="price" />
                 
                </div>

                <div class="form-outline mb-4">
                  <label class="form-label" >Car Type</label>
                   <select type="text" class="form-control form-control-lg"  name="car_type" >
                        <option value="suv">SUV</option> 
                        <option value="sedan">SEDAN</option> 
                        <option value="cvt">CVT Transmission </option>
                    </select>
                 
                </div>

                <div class="form-outline mb-4 trans">
                    <label for="transmission">Transmission</label>
                    <select type="text" class="form-control form-control-lg"  name="transmission" >
                        <option value="manual">Manual</option> 
                        <option value="automatic">Automatic</option> 
                        <option value="cvt">CVT Transmission </option>
                    </select>
                </div>

                <div class="form-outline mb-4 desc">
                  <label class="form-label" >Description</label>
                  <textarea type="password"  class="form-control form-control-lg" name="description" ></textarea>
                 
                </div>
                
               <div class="form-outline mb-4 upload">
                  <label class="form-label" >Upload Photo</label>
                  <input type="file"  class="form-control form-control-lg" name="photo" style="border:none;" />
                 
                </div>
    
                <button class="btn btn-primary btn-lg btn-block green reg" type="submit">Save</button>
                </div>
                 </form>
              </div>
            </div>

          </div>
        </div>
        </div>
        </section>
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
        //this.getAuthToken();
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
                    'Authorization': 'Bearer ' + this.auth_token
                }
			})
			.then(function (response){
                return response.json();
            })
			.then(function (data){
                console.log(data);
                if(data.message != undefined){
                    self.success_msg= data.message;
                    self.$router.push({name:'explore', params:{succes_msg: data.message}})
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
                    self.csrf_token = data.csrf_token;
                    console.log(data);
                })
        },
        
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
/* .form{
    margin-top: 80px;
} */

.form-group-reg{
    display:grid;
    grid-template-columns: 50% 50% ;
    column-gap: 2rem;
}

.trans{
    grid-area: 4;
}

.desc{
    grid-area: 5/span 2;
}

.upload{
    grid-area: 6/span 2;
}

.reg{
    grid-area: 7;
}
</style>