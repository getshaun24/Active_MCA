<template>
    

    <div class="logo_container" @click="$emit('logo_cube_clicked')">
  <div  class="cube-container" @mouseenter="startTurning" @mouseleave="stopTurning">
    <div class="cube" :style="{ transform: `rotateY(${cube}deg)` }">
      <div class="face front">
        <img class="header_logo" src="~/assets/content/homepage/ACT_logo.png" alt="">
      </div>
      <div class="face back">E</div>
      <div class="face top"></div>
      <div class="face bottom"></div>
      <div class="face left">T</div>
      <div class="face right">G</div>
  </div>
</div>
            </div>

</template>



<script setup>
import { ref, nextTick } from 'vue';
import { page_to } from "../../stores/page_to.js"


const cube = ref(0);
    const cube_not_reset = ref(true);
    let i = ref(0)



    async function startTurning() {
      await nextTick();
function myLoop() {         //  create a loop function
    setTimeout(function() {   //  call a 3s setTimeout when the loop is called
    cube.value -= 10   //  your code here
    i++;                    //  increment the counter
    if (i < 5000 || cube_not_reset.value == true) {           //  if the counter < 10, call the loop function
    myLoop();             //  ..  again which will trigger another 
    } else{
    cube_not_reset.value = true;    
    cube.value=0;
    }                      //  ..  setTimeout()
    }, 30)
    }
    myLoop(); 
}

function stopTurning() {

    cube.value = 0;
    cube_not_reset.value = false;

}



        // sleep time expects milliseconds
        function sleep (time) {
          return new Promise((resolve) => setTimeout(resolve, time));
        }


const route_to = page_to()

const nuxtApp = useNuxtApp()
nuxtApp.hook('page:finish', () => {
  startTurning()
  if (String(route_to.current_page_to).includes('fund_pages')){
  sleep(1600).then(() => { stopTurning()})
  } else if (String(route_to.current_page_to) == '/'){
    sleep(2700).then(() => { stopTurning()})
  }
  else{
    sleep(1000).then(() => { stopTurning()})
  }

})




</script>







<style scoped>




.logo_container{
    width:125px;
    height:100px;
    margin-left:0px;
    cursor: pointer;
    z-index:1000;
      position:relative;
    
}




.header_logo{
    width:60px;
    mix-blend-mode: difference;
}


.cube-container {
    perspective: 1000px;
  }

  .cube {
    width: 60px;
    height: 60px;
    position: relative;
    transform-style: preserve-3d;
    transform: rotateY(45deg);
    transition: transform 0.5s;
    margin-left:10px;
    margin-top:30px;
  }

  .cube {
    transform: translateY(180px);
  }

  .face {
    position: absolute;
    width: 60px;
    height: 60px;
    text-align: center;
    font-size: 50px;
    color: white;
    background-color: #000;
    border: #fff 1px solid;
    line-height: 60px;
  }

  .front {
    transform: translateZ(30px);;
  }
  

  .back {
    transform: rotateY(180deg) translateZ(30px);
  }

  .top {
    transform: rotateX(90deg) translateZ(30px);
  }

  .bottom {
    transform: rotateX(-90deg) translateZ(30px);
  }

  .left {
    transform: rotateY(-90deg) translateZ(30px);
  }

  .right {
    transform: rotateY(90deg) translateZ(30px);
  }



/* 

  @media only screen and (min-width: 0px) and (max-width: 576px) {



.cube {
width: 40px;
height: 40px;
position: relative;
transform-style: preserve-3d;
transform: rotateY(45deg);
transition: transform 0.5s;
margin-left:25px;
margin-top:2px;
}

.cube {
transform: translateY(180px);
}

.face {
position: absolute;
width: 40px;
height: 40px;
text-align: center;
font-size: 50px;
color: white;
background-color: #000;
border: #fff 1px solid;
line-height: 40px;
}

.front {
transform: translateZ(20px);;
}


.back {
transform: rotateY(180deg) translateZ(20px);
}

.top {
transform: rotateX(90deg) translateZ(20px);
}

.bottom {
transform: rotateX(-90deg) translateZ(20px);
}

.left {
transform: rotateY(-90deg) translateZ(20px);
}

.right {
transform: rotateY(90deg) translateZ(20px);
}

.header_logo{
width:40px;
mix-blend-mode: difference;
}

}





@media only screen and (min-width: 576px) and (max-width: 768px) {


.header_container{
width:82%;
}



.cube {
width: 40px;
height: 40px;
position: relative;
transform-style: preserve-3d;
transform: rotateY(45deg);
transition: transform 0.5s;
margin-left:25px;
margin-top:2px;
}

.cube {
transform: translateY(180px);
}

.face {
position: absolute;
width: 40px;
height: 40px;
text-align: center;
font-size: 50px;
color: white;
background-color: #000;
border: #fff 1px solid;
line-height: 40px;
}

.front {
transform: translateZ(20px);;
}


.back {
transform: rotateY(180deg) translateZ(20px);
}

.top {
transform: rotateX(90deg) translateZ(20px);
}

.bottom {
transform: rotateX(-90deg) translateZ(20px);
}

.left {
transform: rotateY(-90deg) translateZ(20px);
}

.right {
transform: rotateY(90deg) translateZ(20px);
}

.header_logo{
width:40px;
mix-blend-mode: difference;
}




}






@media only screen and (min-width: 768px) and (max-width: 992px) {


.cube {
width: 60px;
height: 60px;
position: relative;
transform-style: preserve-3d;
transform: rotateY(45deg);
transition: transform 0.5s;
margin-left:25px;
margin-top:2px;
}

.cube {
transform: translateY(180px);
}

.face {
position: absolute;
width: 60px;
height: 60px;
text-align: center;
font-size: 50px;
color: white;
background-color: #000;
border: #fff 1px solid;
line-height: 60px;
}

.front {
transform: translateZ(30px);;
}


.back {
transform: rotateY(180deg) translateZ(30px);
}

.top {
transform: rotateX(90deg) translateZ(30px);
}

.bottom {
transform: rotateX(-90deg) translateZ(30px);
}

.left {
transform: rotateY(-90deg) translateZ(30px);
}

.right {
transform: rotateY(90deg) translateZ(30px);
}

.header_logo{
width:60px;
mix-blend-mode: difference;
}





} */



</style>