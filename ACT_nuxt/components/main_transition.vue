
<template>
    
    <Teleport to="body">

    <!-- <div v-show="transition_display" class="transition_overlay" ></div> -->
    <div v-show="transition_open_display"  class="menu_background_top_open"><div class="menu_paper"></div></div>
    <div v-show="transition_open_display" class="menu_background_bottom_open"><div class="menu_paper"></div></div>
    <div v-show="transition_close_display"  class="menu_background_top_close"><div class="menu_paper"></div></div>
    <div v-show="transition_close_display" class="menu_background_bottom_close"><div class="menu_paper"></div></div>

  </Teleport>


</template>










<script setup>




// sleep time expects milliseconds
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}


const transition_open = ref(false)
const transition_close = ref(true)
const transition_open_display = ref(false)
const transition_close_display = ref(true)
const overlay_opacity = ref(0)
const blur_amount = ref('0px')


function animation_and_route(route_to){
  transition_open_display.value = true
  sleep(1).then(() => {transition_open.value = true})
  overlay_opacity.value = 1
  blur_amount.value = '5px'
  sleep(600).then(() => {navigateTo(route_to)})
  sleep(610).then(() => {close_transition()})
}

function close_transition(){
  sleep(1).then(() => {transition_close.value = true, transition_open.value = false})
  overlay_opacity.value = 1
  sleep(10).then(() => {transition_close.value = false, blur_amount.value = '5px', overlay_opacity.value = 0})
  sleep(1500).then(() => {transition_close_display.value = false})

}


onBeforeMount(() => {
  close_transition()

})



defineExpose({
    animation_and_route
})

</script>





<style scoped>


.menu_background_top_open{
    position:fixed;
    top:0;
    left:0;
    width:100vw;
    height:50vh;
    background-color:rgb(255, 255, 255);
    z-index:90;
    transition:all .5s ease-in-out;
    transform: translateX(v-bind(transition_open ? 0 : '100vw'));
    /* display: v-bind(burger_active ? 'block' : 'none'); */
}


.menu_background_bottom_open{
    position:fixed;
    top:50vh;
    left:0;
    width:100vw;
    height:50vh;
    background-color:rgb(255, 255, 255);
    z-index:90;
    transform: translateX(v-bind(transition_open ? 0 : '-100vw'));
    /* display: v-bind(burger_active ? 'block' : 'none'); */
    transition:all .5s ease-in-out;
}


.menu_background_top_close{
    position:fixed;
    top:0;
    left:0;
    width:100vw;
    height:50vh;
    background-color:rgb(255, 255, 255);
    z-index:90;
    transition:all .5s ease-in-out;
    transform: translateX(v-bind(transition_close ? 0 : '100vw'));
    /* display: v-bind(burger_active ? 'block' : 'none'); */
}


.menu_background_bottom_close{
    position:fixed;
    top:50vh;
    left:0;
    width:100vw;
    height:50vh;
    background-color:rgb(255, 255, 255);
    z-index:90;
    transform: translateX(v-bind(transition_close ? 0 : '-100vw'));
    /* display: v-bind(burger_active ? 'block' : 'none'); */
    transition:all .5s ease-in-out;
}

.menu_paper{
    position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  opacity:.5;
  background-size: 35%;
  background-repeat: repeat;
  background-image: url("~/assets/content/paper/paper_overlay_3.jpg");
  mix-blend-mode: multiply;
  pointer-events: none;
}

.transition_overlay{
    width:100vw;
    height:200vh;
    background-color:rgba(222, 241, 255, 0.25);
    z-index:80;
    position:fixed;
    bottom:0;
    left:0;
    backdrop-filter: blur(v-bind(blur_amount));
    transition: all 1s ease-in-out;
    opacity: v-bind(overlay_opacity);
}



/* --------------------------------------------------------------------- */







.white_circle_1{
  width:50vw;
  height:50vw;
  border-radius:100%;
  background-color:#fff;
  z-index:2500;
  margin-left:v-bind(circle_white_margin_left);
  /* left:150%;
  top:0%; */
  margin-top:v-bind(circle_white_margin_top);
  opacity:v-bind(circle_white_opacity);
  position:fixed;
  transform: scale(v-bind(white_scale));
  transition: margin-top 3.5s ease-in-out, margin-left 3.5s ease-in-out, transform 2.5s ease-in;
  display: v-bind(display_it);
  mix-blend-mode: normal;
}


.white_circle_2{
  width:100vw;
  height:100vw;
  border-radius:100%;
  background-color:#000;
  z-index:2400;
  margin-left:v-bind(circle_black_margin_left);
  left:-100%;
  top:100%;
  margin-top:v-bind(circle_black_margin_top);
  opacity:v-bind(circle_black_opacity);
  position:fixed;
  transform: scale(v-bind(black_scale));
  transition: margin-top 2s ease-in-out, margin-left 2s ease-in, transform 2.5s ease-in;
  display: v-bind(display_it);
  mix-blend-mode: normal;
}








</style>
