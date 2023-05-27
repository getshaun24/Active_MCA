<template>


  <div class="services_container">

    <div>
    <h5 class="landing_title">Services</h5>
    <span>Discover Your Savings</span>
    <p>People choose to use ACT because it offers a streamlined, cost-effective, and user-friendly solution for legal settlements that can save time, money, and hassle while achieving a fair and favorable outcome.</p>
    <ACTButtonsSlideButton button_text="Sign Up"/>
</div>



  <swiper data-lag="1" :effect="'coverflow'" :modules="modules" :coverflowEffect="{rotate: -15, stretch: 0, depth: 400, modifier: 1, slideShadows: false, }" :freemode="true" :loop="true" :speed="3000" :freeModeMomentum="true" :centeredSlides="true"  :grabCursor="true" :breakpoints="swiperOptions.breakpoints" :autoplay="{delay: 1500, disableOnInteraction: false}" style="transition-timing-function:linear" @slideChange="swiper_index" class="services_swiper_wrapper">





<swiper-slide><h6 class="swiper_title">AI-Powered Negotiation</h6><img class="swiper_img" src="~/assets/content/services/services_2a.jpg" /></swiper-slide>
<swiper-slide><h6 class="swiper_title">Secure Cloud Network</h6><img class="swiper_img" src="~/assets/content/services/services_3a.jpg" /></swiper-slide>
<swiper-slide><h6 class="swiper_title">Seamless Payments</h6><img class="swiper_img" src="~/assets/content/services/services_4a.jpg" /></swiper-slide>
<swiper-slide><h6 class="swiper_title">Algorithmically Fair</h6><img class="swiper_img" src="~/assets/content/services/services_5a.jpg" /></swiper-slide>
<swiper-slide><h6 class="swiper_title">Seamless Payments</h6><img class="swiper_img" src="~/assets/content/services/services_6a.jpg" /></swiper-slide>
<swiper-slide><h6 class="swiper_title">Saves You $$$</h6><img class="swiper_img" src="~/assets/content/services/services_1a.jpg" /></swiper-slide>

<!-- ------------------------------ Duplicates ------------------------------ -->
<swiper-slide><h6 class="swiper_title">AI-Powered Negotiation</h6><img class="swiper_img" src="~/assets/content/services/services_2a.jpg" /></swiper-slide>
<swiper-slide><h6 class="swiper_title">Secure Cloud Network</h6><img class="swiper_img" src="~/assets/content/services/services_3a.jpg" /></swiper-slide>
<swiper-slide><h6 class="swiper_title">Seamless Payments</h6><img class="swiper_img" src="~/assets/content/services/services_4a.jpg" /></swiper-slide>
<swiper-slide><h6 class="swiper_title">Algorithmically Fair</h6><img class="swiper_img" src="~/assets/content/services/services_5a.jpg" /></swiper-slide>
<swiper-slide><h6 class="swiper_title">Seamless Payments</h6><img class="swiper_img" src="~/assets/content/services/services_6a.jpg" /></swiper-slide>
<swiper-slide><h6 class="swiper_title">Saves You $$$</h6><img class="swiper_img" src="~/assets/content/services/services_1a.jpg" /></swiper-slide>
<!-- ------------------------------ Duplicates ------------------------------ -->

</swiper>

</div>
<div style="margin-top:10%">
<hr>
</div>
</template>



<script setup>

import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Autoplay, EffectCoverflow } from "swiper";


import 'swiper/css/bundle';
import "swiper/css/effect-coverflow";


  
const modules = [EffectCoverflow, Autoplay]



const swiperOptions = {
          breakpoints: {      
            0: {       
         slidesPerView: 1.5,
         spaceBetween: 40     
      }, 
      576: {       
         slidesPerView: 1.9,
         spaceBetween: 40     
      },          
      768: {       
         slidesPerView: 2.5,       
         spaceBetween: 40     
      },   
  
      992: {       
         slidesPerView: 1.5,       
         spaceBetween: 10     
      } 
   }   
}


</script>



<style scoped>

.services_container{
    display: grid;
grid-template-columns: repeat(2, 1fr);
grid-template-rows: 1fr;
grid-column-gap: 100px;
grid-row-gap: 0px;
width:80%;
margin-left:10%;
padding-top:10%;

}





.swiper_img{
    width:100%;
    border-radius:30px
}

.services_swiper_wrapper{
    margin-top:3%;
    width:100%
}


.swiper_line{
    width:1px;
    border-left:#fff solid 2px;
    height:v-bind(swiper_line_height);
    margin-left:30px;
    margin-top:v-bind(swiper_line_margin);
    opacity: v-bind(swiper_opacity);
    transition:all 1.5s ease;
}



/* .main_image:hover .swiper_line{
    height:110px;
    margin-top:0px;
} */

.swiper_title{
    text-align: center;
    margin-top:130%;
    font-size:150%;
    position:absolute;
    width:100%;
    filter: drop-shadow(5px 4px 4px rgba(6, 100, 162, 0.2));
    opacity: v-bind(swiper_opacity);
}
.swiper_subtitle{
    margin-left:50px;
    margin-top:-63px;
    opacity: v-bind(swiper_opacity);
}

.landing_title{
    margin-bottom:8%;
}

</style>













