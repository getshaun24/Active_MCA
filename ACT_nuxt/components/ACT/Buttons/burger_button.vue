<template>
    

  
    <div v-show="burger_active_show" class="menu_background_top">
        <img class="dahboard_logo" src='~/assets/content/logos/active_logo.png'>
        <div class="menu_paper"></div>

    <FunderMenu class="menu_comp_style" />

    </div>
    <div v-show="burger_active_show" class="menu_background_bottom">
    </div>


  <div class="burger_container">
    <div @click="burger_click" :class="{active:burger_active}" class="burger">
      <span></span>
    </div>
  </div>



</template>


<script setup>
       function sleep (time) {
          return new Promise((resolve) => setTimeout(resolve, time));
        }


const burger_active = ref(false);
const burger_active_show = ref(false);
const border_size = ref('1px');
const menu_opacity = ref(0);
const menu_opacity_delay = ref('0s');

function burger_click() {
  if (!burger_active.value) {
    burger_active_show.value = !burger_active_show.value;
    sleep(1).then(() => { burger_active.value = !burger_active.value; border_size.value = '0px'; menu_opacity.value = 1; menu_opacity_delay.value = '.7s';});
  } else {
    burger_active.value = !burger_active.value;
    border_size.value = '1px';
    menu_opacity.value = 0;
    menu_opacity_delay.value = '0s';
    sleep(500).then(() => { burger_active_show.value = !burger_active_show.value; });
  }
  // burger_active_show.value = !burger_active_show.value;
  // sleep(1).then(() => { burger_active.value = !burger_active.value; });
}



</script>


<style scoped>



.dahboard_logo{
  width:150px;
  margin-left:30px;
  margin-top:25px;
  cursor:pointer;
  z-index:100;
  opacity:v-bind(burger_active ? 1 : 0);
  transition:all .5s ease-in-out .85s;
}



.menu_background_top{
    position:fixed;
    top:0;
    left:0;
    width:100vw;
    height:50vh;
    background-color:#000;
    z-index:100;
    overflow: visible;
    border:var(--border-color) v-bind(border_size) solid;
    transition:all .5s ease-in-out;
    transform: translateX(v-bind(burger_active ? 0 : '100vw'));
    /* display: v-bind(burger_active ? 'block' : 'none'); */
}


.menu_background_bottom{
    position:fixed;
    top:50vh;
    left:0;
    width:100vw;
    height:50vh;
    background-color:#000;
    z-index:90;
    border:var(--border-color) v-bind(border_size) solid;
    transform: translateX(v-bind(burger_active ? 0 : '-100vw'));
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


.menu_comp_style{
 opacity: v-bind(menu_opacity);
  transition: all 0.5s ease-in-out v-bind(menu_opacity_delay);
}




/* ------- burger animation ----------- */
/* ------- burger animation ----------- */
/* ------- burger animation ----------- */



.burger_container{
    margin-top:25px;
    margin-right:50px;
    z-index:100
}

.croix span {
  width: 100%;
  height: 4px;
  border-radius: 12px;
  display: block;
}

.croix span::before,
.croix span::after {
  content: "";
  width: 30px;
  background-color: var(--theme-icon-color);
  display: block;
  border-radius: 12px;
  height: 4px;
}

.croix span::before {
  transform: translateY(-10px);
  transform: rotate(45deg);
  
}

.croix span::after {
  transform: translateY(10px);
  transform: rotate(-45deg);
  margin-top: -4px;
}

/*===============================*/

.burger {
  width: 32px;
  height: 24px;
  cursor: pointer;
  right: 2rem;
  top: 2rem;
  z-index: 20;
}

.burger span {
  width: 100%;
  height: 4px;
  background-color: var(--theme-icon-color);
  border-radius: 12px;
  display: block;
  transition: background-color 0.5s ease-in-out;
}

.burger span::before,
.burger span::after {
  content: "";
  width: 100%;
  background-color:  var(--theme-icon-color);
  display: block;
  transition: all 0.5s ease-in-out;
  border-radius: 12px;
  height: 4px;
}

.burger span::before {
  transform: translateY(-10px);
}

.burger span::after {
  transform: translateY(10px);
  margin-top: -4px;
}

.burger.active span {
  background-color: transparent;
}

.burger.active span::before {
  transform: rotateZ(45deg) translateY(0);
}

.burger.active span::after {
  transform: rotateZ(-45deg) translateY(0);
}




</style>