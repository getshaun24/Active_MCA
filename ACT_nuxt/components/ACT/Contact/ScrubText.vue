<template>
    

<div class="wrapperRollingText">
  <div class="rollingText" data-lag=".6" data-speed=".7">
    {{ text }}<span class="period_color">.</span> {{ text }}<span class="period_color">.</span>
    {{ text }}<span class="period_color">.</span> {{ text }}<span class="period_color">.</span>
    {{ text }}<span class="period_color">.</span> {{ text }}<span class="period_color">.</span>
    {{ text }}<span class="period_color">.</span> {{ text }}<span class="period_color">.</span>
    {{ text }}<span class="period_color">.</span> {{ text }}<span class="period_color">.</span>&nbsp;

  </div>
</div>



</template>



<script setup>

import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
gsap.registerPlugin(ScrollTrigger);



const props = defineProps(['text', 'duration'])



onMounted(() => {

  

// NOTE: for a responsive version, see https://codepen.io/GreenSock/pen/QWqoKBv

let direction = 1; // 1 = forward, -1 = backward scroll

const roll1 = roll(".rollingText", { duration: props.duration}),
  scroll = ScrollTrigger.create({
    onUpdate(self) {
      if (self.direction !== direction) {
        direction *= -1;
        gsap.to([roll1], { timeScale: direction, overwrite: true });
      }
    }
  });

// helper function that clones the targets, places them next to the original, then animates the xPercent in a loop to make it appear to roll across the screen in a seamless loop.
function roll(targets, vars, reverse) {
  const tl = gsap.timeline({
    repeat: -1,
    onReverseComplete() {
      this.totalTime(this.rawTime() + this.duration() * 100); // otherwise when the playhead gets back to the beginning, it'd stop. So push the playhead forward 10 iterations (it could be any number)
    }
  });
  vars = vars || {};
  vars.ease || (vars.ease = "none");
  gsap.utils.toArray(targets).forEach((el) => {
    let clone = el.cloneNode(true);
    el.parentNode.appendChild(clone);
    gsap.set(clone.value, {
      position: "absolute",
    });
    tl.to([el, clone], { xPercent: reverse ? 100 : -100, ...vars }, 0);
  });
  return tl;
}

// make sure there is a background to the text to mask the overlapping text








})


</script>





<style scoped>




         .rollingText {
   font-size: 12vw;
   padding-left: 10px;
   font-weight: 900;
   word-spacing: 20px;
   color:#fff;
   white-space: nowrap;
     margin-top:15%;
    width:5000vw;
    text-shadow: -1px 0 rgb(6, 100, 162, 0.5), 0 1px rgb(6, 100, 162, 0.5), 1px 0 rgb(6, 100, 162, 0.5), 0 -1px rgb(6, 100, 162, 0.5);



 }


.wrapperRollingText{
  position:relative;
  display: flex;
  margin-top:25%
}




.period_color{
    color:rgb(6, 100, 162);
}


</style>