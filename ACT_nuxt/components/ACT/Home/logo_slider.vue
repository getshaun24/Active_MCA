<template>
    
    <p class="slider_title">Trusted By Industry Leaders</p>

    <div class="logo_container">

    <swiper :modules="modules" :loop="true" :freemode="true" :speed="6000" :freeModeMomentum="true" :autoplay='{"delay": 0,"disableOnInteraction": true}' :grabCursor="true" :slides-per-view="6" :space-between="0" class="swiper_wrapper" style="transition-timing-function:linear">
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
    <swiper-slide><img class="logo" src="~/assets/content/homepage/GET_logo_white.png"></swiper-slide>
  </swiper>

    </div>


</template>



<script setup>
import { ref } from 'vue'
import { useIntersectionObserver } from '@vueuse/core'
import { Swiper, SwiperSlide } from 'swiper/vue';
import SwiperCore, { Autoplay } from 'swiper/core';

import 'swiper/css/bundle';

const modules = [Autoplay]










</script>




<style scoped>

.swiper_wrapper {
  -webkit-transition-timing-function:linear!important; 
  -o-transition-timing-function:linear!important;
  transition-timing-function:linear!important; 
  transition:linear !important
}

swiper-slide{
    -webkit-transition-timing-function:linear!important; 
  -o-transition-timing-function:linear!important;
  transition-timing-function:linear!important; 
  transition:linear !important
}


.slider_title{
    margin-left:40%;
    text-align: center;
    width:20%;
    white-space: nowrap;
    margin-top:3%
}

.logo_container{
    border-top: 1px solid rgba(0, 0, 0, 0.25);
    border-bottom: 1px solid rgba(0, 0, 0, 0.25);
    height:100px;
    cursor: pointer;
}

.logo{
    height:60px;
    width:auto;
    margin:20px 0
}



</style>