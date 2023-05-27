<template>
    
    <div class="menu_container">
        <NuxtLink to="/"><img src="~/assets/content/logos/active_logo.png" loading="lazy" alt="" class="menu_logo" /></NuxtLink>
    <div class="menu_items">
        <NuxtLink to="/" class="menu_item">Home</NuxtLink>
        <NuxtLink to="/services" class="menu_item">Services</NuxtLink>
        <div class="menu_item ">About</div>
        <NuxtLink to="/contact" class="menu_item">Contact</NuxtLink>
        <ACTButtonsSignupLoginButton style="margin-left:7%" v-bind="sign_up_props"/>
        <ACTButtonsSignupLoginButton style="margin-left:7%" v-bind="login_props"/>
    </div>


</div>
</template>


<script setup>

const sign_up_props = {
  button_text: 'Sign Up',
  background_color: '#fafdff',
  color: '#000',
  link_to: '/login_pages/sign_up'
}

const login_props = {
  button_text: 'Login',
  background_color: '#000',
  color: '#fff',
  link_to: '/login_pages/login'
}


</script>

<style scoped>

.menu_logo{
    width: 70px;
    margin-top: 5px;
    margin-left: 30px;
}

.menu_container{
    position: fixed;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.25);
    z-index:100;
    height:80px;
    backdrop-filter: blur(30px);
    opacity: 1;
    margin-top:-8px;
    margin-left:-8px
}
.menu_items{
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    width: 50%;
    margin-left: 40%;
    margin-top: -50px;
    font-size: 20px;
    font-weight: 100;
    color: #fff;
}

.menu_item{
    padding:2px 25px;
    border-radius: 50px;
    width:120px;
    text-align: center;
    cursor: pointer;
    height:30px;
    margin:0px 1%;
    color:#fff;
    line-height: 1.5;
}

.menu_item:hover{
    background-color: #a7d3e8;
    color:#fff;
}

.mag_buttons{
    display: flex;
    flex-direction: row;
    }
</style>