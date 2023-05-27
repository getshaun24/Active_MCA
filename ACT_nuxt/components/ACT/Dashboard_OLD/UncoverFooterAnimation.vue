<template>
    
    <div class="uncover_container">
             
            </div>


</template>

<script setup>

import { onMounted } from 'vue';
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'


onMounted(() => {


gsap.set(".footer", { yPercent: -50 });

const uncover = gsap.timeline({ paused: true });

uncover.to(".footer", { yPercent: 0, ease: "none" });

ScrollTrigger.create({
  trigger: ".footer",
  start: "bottom bottom",
  end: "+=75%",
  animation: uncover,
  scrub: true
});

ScrollTrigger.refresh();


})


</script>


<style scoped>

.uncover_container {
    display: block;
    z-index:-1;
    width:100%;
    height:400px;
    position: -webkit-sticky;
    position: sticky;
    bottom: 0;
}


</style>