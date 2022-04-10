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
            <p>United Auto Sales provides the fastest easiest and most user friendly 
            way to buy or sell cars online. Find a Great Price on the Vehicle You Want</p>
            <div class="btn-group">
            <button class="register">Register</button>
            <button class="register">Login</button>
        </div>
        </div>
        <div class="right">
            <p>Place image here</p>
        </div>       
    </div>
</template>

<style>
.bold{
    font-size: 60px;
}
.home{
    width: 100%;
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
    font-size: 30px;
    width:50%;
    float: right;
}
</style>