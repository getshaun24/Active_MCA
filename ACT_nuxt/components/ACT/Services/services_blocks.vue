<template>
    
<div class="service_blocks" data-speed="1.2">

<div class="upper_block">


        <div class="upper_inner_block" data-lag="0.02">
            <img class="icon" src="~/assets/content/services/icon_1.png" alt="">
            <h6 class="block_title">AI-Powered Negotiation</h6>
            <p class="block_description">ACT's platform offers an AI-powered negotiation tool that provides real-time guidance and recommendations during the negotiation process. This can help users achieve more favorable settlement outcomes and avoid costly mistakes that could prolong the settlement process.</p>
        </div>

        <div class="upper_inner_block" style="grid-column:1; grid-column-start: span 2;">
            <div class="big_block_grid_outer">
            <img class="profile_img" src="~/assets/content/services/services_8.jpg" alt="">
            <div class="big_block_grid_inner">
                <h6 class="big_block_text">Manage And Organize All Your Deals And Settlements</h6>
                <h6 class="big_block_text">Instant Payments On Deal Close</h6>
                <h6 class="big_block_text">Full Tracking Transparency To Your Team and Clients</h6>
                
                </div>
        </div>
    </div>


</div>

<div class="lower_block">

    <div class="lower_inner_block" data-lag="0.005">

    </div>

    <div class="lower_inner_block" data-lag="0.01">

</div>

<div style="background-color:rgb(6, 100, 162);" class="lower_inner_block" data-lag="0.02">
    <img class="icon" src="~/assets/content/services/icon_1.png" alt="">
    <h6 class="block_title_white">Streamlining Settlements</h6>
    <ACTButtonsSignupLoginButton style="margin-left:7%" v-bind="sign_up_props"/>
</div>

</div>


</div>


</template>

<script setup>

const sign_up_props = {
  button_text: 'Sign Up',
  background_color: '#fafdff',
  color: '#000'
}

</script>

<style scoped>

.service_blocks{
display: grid;
grid-template-columns: 1fr;
grid-template-rows: repeat(2, 1fr);
grid-column-gap: 0px;
grid-row-gap: 20px;
margin-top:10%;
width:90%;
margin-left:5%;
}

.upper_block{
    height:450px;
    grid-column: span 3;
    display: grid;
grid-template-columns: repeat(3, 1fr);
grid-template-rows: 1fr;
grid-column-gap: 20px;
grid-row-gap:20px;
}

.lower_block{
    height:350px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: 1fr;
    grid-column-gap: 20px;
    grid-row-gap: 20px;
}

.lower_inner_block{
    border-radius: 30px;
    background-color: #a7d3e861;
    border: #a7d3e8 1px solid;
}

.upper_inner_block{
    border-radius: 30px;
    background-color: #a7d3e861;
    border: #a7d3e8 1px solid;
}

/* .upper_inner_block:first-child {
  grid-column: 1 / 3; 
} */

.icon{
    width:90px;
    margin-left:30px;
    margin-top:30px;
}


.profile_img{
    width:300px;
    border-radius:100%;
    margin-top:75px;
    margin-left:4%;
}

.block_title{
    font-size:250%;
    text-align: center;
    margin-top:-85px;
    margin-left:90px;
    margin-bottom:70px;
}

.block_title_white{
    font-size:250%;
    text-align: center;
    margin-top:-85px;
    margin-left:0px;
    margin-bottom:70px;
    color:#fff
}
.block_description{
    font-size:100%;
    text-align: center;
    margin-left:10%;
    margin-right:10%;
    margin-top:5%;
}

.big_block_grid_outer{
    display: grid;
grid-template-columns: repeat(2, 1fr);
grid-template-rows: 1fr;
grid-column-gap: 0px;
grid-row-gap: 0px;
}

.big_block_grid_inner{
    display: grid;
grid-template-columns: 1fr;
grid-template-rows: repeat(3, 1fr);
grid-column-gap: 0px;
grid-row-gap: 0px;
height:200px;
margin-top:70px
}

.big_block_text{
    font-size:25px;
    border-bottom: 1px solid #000;
    margin-left:-15%;
    width:100%;
    padding-bottom:10px;
    margin-top:-10px;
    line-height: 1.5;
}






@media only screen and (min-width: 0px) and (max-width: 576px) {

    .service_blocks{
grid-row-gap: 60px;
}

}

@media only screen and (min-width: 576px) and (max-width: 768px) {

    .service_blocks{
grid-row-gap: 60px;
}
}

@media only screen and (min-width: 768px) and (max-width: 992px) {
    .service_blocks{
grid-row-gap: 20px;
}

.big_block_text{
    font-size:20px;
    margin-left:-6%;
    width:90%;
    padding-bottom:10px;
    margin-top:5px;
}

.profile_img{
    width:250px;
    border-radius:100%;
    margin-top:100px;
    margin-left:4%;
}

.icon{
    width:70px;
    margin-left:15px;
    margin-top:30px;
}

.block_title{
    font-size:190%;
    text-align: center;
    margin-top:-65px;
    margin-left:65px;
    margin-bottom:40px;
}

}


@media only screen and (min-width: 992px) and (max-width: 1200px) {

    .big_block_text{
    font-size:20px;
    margin-left:-6%;
    width:90%;
    padding-bottom:10px;
    margin-top:5px;
}

.profile_img{
    width:250px;
    border-radius:100%;
    margin-top:100px;
    margin-left:4%;
}

.icon{
    width:70px;
    margin-left:15px;
    margin-top:30px;
}

.block_title{
    font-size:190%;
    text-align: center;
    margin-top:-65px;
    margin-left:65px;
    margin-bottom:40px;
}

}

@media only screen and (min-width: 1200px) and (max-width: 1400px) {
    .big_block_text{
    font-size:23px;
    border-bottom: 1px solid #000;
    margin-left:-10%;
    width:100%;
    padding-bottom:10px;
    margin-top:-5px;
    line-height: 1.5;
}

.profile_img{
    width:275px;
    border-radius:100%;
    margin-top:87.5px;
    margin-left:6%;
}

.block_title{
    font-size:220%;
    text-align: center;
    margin-top:-85px;
    margin-left:100px;
    margin-bottom:70px;
}


}

@media only screen and (min-width: 1400px) and (max-width: 1600px) {

    .big_block_text{
    font-size:22px;
    border-bottom: 1px solid #000;
    margin-left:-10%;
    width:100%;
    padding-bottom:10px;
    margin-top:0px;
    line-height: 1.5;
}

.profile_img{
    width:275px;
    border-radius:100%;
    margin-top:87.5px;
    margin-left:8%;
}

.block_title{
    font-size:220%;
    text-align: center;
    margin-top:-85px;
    margin-left:100px;
    margin-bottom:70px;
}


}

@media only screen and (min-width: 1600px) and (max-width: 1700px) {
}

@media only screen and (min-width: 1700px) and (max-width: 1800px) {

}

@media only screen and (min-width: 1800px) and (max-width: 1900px) {

}

@media only screen and (min-width: 1900px) and (max-width: 2000px) {

}

@media only screen and (min-width: 2000px) and (max-width: 5600px) {

}


</style>