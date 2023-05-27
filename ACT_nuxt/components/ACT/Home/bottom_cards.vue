<template>

    <div class="grid">
   
    
    <div class="image_section_1">
    <div>
        <h6 class="card_title">About Us</h6>
        <p class="sub_text">Our mission is to streamline your deals.</p>
        <div class="button_style" style="margin-top:110px; ">
        <ButtonsSignupLoginButton v-bind="about_props"/>
    </div>
        </div>
    </div>
    <div class="image_section_2">
        <div>
        <h6 class="card_title">Pricing</h6>
        <p class="sub_text">We offer an a-la-carte solution.</p>
        <div class="button_style">
        <ButtonsSignupLoginButton v-bind="pricing_props"/>
    </div>
        </div>
    </div>
    <div class="image_section_3">
        <div>
        <h6 class="card_title">Take Action</h6>
        <p class="sub_text">Our mission is to streamline your deals.</p>
        <div style="margin-top:45%">
        <ButtonsArrowButton/>
    </div>
        </div>
    </div>
        
    </div>
        </template>
        
        <script setup>
    
    const about_props = {
  button_text: 'About',
  background_color: '#fff',
  color: '#000'
}

const pricing_props = {
  button_text: 'Pricing',
  background_color: '#fff',
  color: '#000'
}



        </script>
        
        
        
        
        
        
        
        <style scoped>
    
    .grid {
display: grid;
grid-template-columns: repeat(3, 1fr);
grid-template-rows: 1fr;
grid-column-gap: 0px;
grid-row-gap: 0px;
width:90%;
margin:5%
}

.sub_text{
    width:70%;
    margin-left:8%;
    margin-top:240px;
}

.card_title{
    margin-top:-70px;
    margin-left:2%;
    transition: all 1s ease;
    position: absolute;
}

.button_style{
    margin-top:130px; 
    margin-left: -50%;
}


.image_section_1:hover  .card_title{
    margin-top:-85px;
}

.image_section_2:hover  .card_title{
    margin-top:-85px;
}

.image_section_3:hover  .card_title{
    margin-top:-85px;
}

.image_section_1{
        background-color:rgb(201, 230, 255);
        width:100%;
        height:500px;
        transition: all 2s ease;
        border-bottom-left-radius: 25px;
        border-top-left-radius: 25px;
    }



    .image_section_2{
        background-color:rgb(201, 230, 255);
        width:100%;
        height:500px;
        border-left: solid 1px rgba(121, 121, 121, 0.258);
        transition: all 2s ease;
    }

    .image_section_3{
        background-color:rgb(201, 230, 255);
        width:100%;
        height:500px;
        border-left: solid 1px rgba(121, 121, 121, 0.258);
        transition: all 2s ease;
        border-top-right-radius: 25px;
        border-bottom-right-radius: 25px;
    }

    .image_section_1:hover{
background-color:rgb(232, 216, 255);
border-bottom-left-radius: 10px;
        border-top-left-radius: 10px;
}

.image_section_2:hover{
background-color:rgb(255, 250, 203);
}

.image_section_3:hover{
background-color:rgb(210, 255, 208);
border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
}

    
        </style>