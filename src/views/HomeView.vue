<script>
export default {
    data() {
        return {
            message: "Hello World! This is Lab 7"
        };
    },
}
</script>

<template>
    <div class="home">
        <div class="left">
            <h1 class="bold">Buy and Sell Cars Online</h1>
            <p class="text-secondary">United Auto Sales provides the fastest easiest and most user friendly 
            way to buy or sell cars online. Find a Great Price on the Vehicle You Want</p>
           
            <button class="btn btn-primary btn-lg btn-block">Register</button>
            <button class="btn green btn-primary btn-lg btn-block ">Login</button>
        
        </div>
        <div class="right">
            <img class="homeimg" src="src/assets/homeimg.jpeg" alt="bg">
        </div>       
    </div>
</template>

<style>

*{ 
    margin:0px;
    box-sizing: border-box;
}

.bold{
    font-size: 60px;
}
.home{
    
    width: 95%;
    height: 100vh;
}
.left{
    float: left;
    width: 50%;
    padding-top: 130px;
    padding-left: 130px;
    padding-right: 120px;
    color: black;
    font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;
}

.right{
    width:50%;
    float: right;
    overflow: hidden;
}

.btn-lg{
    width: 10rem;
}

.btn-primary{
  border:none;
  margin-right: 1.5rem;
}

.green{
     background-color: rgb(71, 173, 111);
}

.homeimg{
background-repeat: no-repeat;
    background-position: center top;
    
    width: 100%;
    height: 100vh;
    object-fit: cover;
    position: left;
}

</style>