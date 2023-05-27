<template>

    <div>
      
      <div :class="{ transition_overlay: menu_modal_open, menu_modal_open: menu_modal_open }" ></div>
      <div :class="{ white_circle_1: menu_modal_open, menu_modal_open: menu_modal_open }" ></div>
      <div :class="{ white_circle_2: menu_modal_open, menu_modal_open: menu_modal_open }" ></div>
      <div :class="{ white_circle_3: menu_modal_open, menu_modal_open: menu_modal_open }" ></div>
      <div :class="{ transition_overlay_2: menu_modal_open, menu_modal_open: menu_modal_open }" ></div>
  
      <CircleTransition ref="cicle_tansition"/>
  
          <div class="header_container">
  
  

  
  
              <div class="header_menu">
               
  
  
                  
                  <div class="header_menu_item">
  
                      <div @click="modal_open" style="cursor: pointer;" class="cube_container_modal" @mouseenter="startTurning_modal" @mouseleave="stopTurning_modal">
      <div class="cube_modal" :style="{ transform: `rotateY(${cube_modal}deg)` }">
        <div class="face_modal front_modal"><img class="header_logo_modal" src="~/assets/content/homepage/burger.png" alt=""></div>
        <div class="face_modal back_modal">X</div>
        <div class="face_modal top_modal"></div>
        <div class="face_modal bottom_modal">X</div>
        <div class="face_modal left_modal">X</div>
        <div class="face_modal right_modal"><img class="header_logo_modal" src="~/assets/content/homepage/burger.png" alt=""></div>
      </div>
    </div>
                  </div>
              </div>
          </div>
          
  
  
          <div :class="{ menu_modal_open: menu_modal_open }" class="menu_modal">
  
              <div class="menu_modal_container">
                  <div class="menu_modal_grid">
                      <div class="menu_modal_item">
                          <div @click="close_and_route('/')"><img class="menu_arrow" src="../../assets/content/homepage/arrow_medium_light.svg"><span class="move">Home</span></div>
                      </div>
                      <div class="menu_modal_item">
                          <div @click="close_and_route('/investments')" ><img class="menu_arrow" src="../../assets/content/homepage/arrow_medium_light.svg"><span class="move">Investments</span></div>
                      </div>
                      <div class="menu_modal_item">
                          <div @click="close_and_route('/HowItWorks')"><img class="menu_arrow" src="../../assets/content/homepage/arrow_medium_light.svg"><span class="move">How It Works</span></div>
                      </div>
                      <div class="menu_modal_item">
                          <div @click="close_and_route('/about')"><img class="menu_arrow" src="../../assets/content/homepage/arrow_medium_light.svg"><span class="move">About Us</span></div>
                      </div>
                      <div class="menu_modal_item">
                          <div @click="close_and_route('/contact')"><img class="menu_arrow" src="../../assets/content/homepage/arrow_medium_light.svg"><span class="move">Contact</span></div>
                      </div>
              </div>
  
  
  
                  <div class="modal_info">
                          <div class="info_grid">
                              <div class="info_item">
                                  <div class="info_item_title">GET Resources Group</div>
                                  <div class="info_item_sub_text">Private Equity</div>
                              </div>
  
                              <div class="info_item">
                                  <div class="info_item_title">Financial District</div>
                                  <div class="info_item_sub_text">New York, New York</div>
                              </div>
                              <div class="info_item">
                                  <div class="info_item_title">Historic Navy Yard</div>
                                  <div class="info_item_sub_text">Charleston, South Carolina</div>
                              </div>
                              <div class="info_item">
                                  <div class="info_item_title">Chrysler Building</div>
                                  <div class="info_item_sub_text">New York, New York</div>
                              </div>
  
  
  
                              <div class="info_item contact_item">
                                  <div class="info_item_title">contact@thisisget.com</div>
                                  <div class="info_item_title">press@thisisget.com</div>
                              </div>
    
  
                  </div>
  
  
          </div>
      </div>
  </div>
  
  </div>
  
  </template>
  
  
  <script setup>
  import { ref, onMounted, onUnmounted, nextTick } from 'vue';
  import { from_header_menu } from "../../stores/menu_transition.js"
  import { page_to } from "../../stores/page_to.js"
  
  
  const cube = ref(0);
      const cube_not_reset = ref(true);
      let i = ref(0)
      const menu_modal_open = ref(false);
      const cube_modal = ref(true);
      const cube_not_reset_modal = ref(true);
  
  
  
  
  const circle_white_margin_left = ref("-100%")
  const circle_white_margin_top = ref("-100%")
  const circle_white_opacity = ref(0)
  const circle_black_margin_left = ref("-100%")
  const circle_black_margin_top = ref("100%")
  const circle_black_opacity = ref(0)
  
  const circle_3_margin_top = ref("0vh")
  const circle_3_opacity = ref(0)
  
  
  const menu_item_margin_top = ref("100%")
  const menu_item_opacity = ref(0)
  const modal_info_left = ref("100%")
  const modal_info_top = ref("0%")
  const overlay_opacity = ref(0)
  const overlay_2_opacity = ref(0)
  const overlay_visibility = ref("hidden")
  
  
  const menu_container_margin = ref("25vh")
  const menu_container_opacity = ref(0)
  
  
  
  // sleep time expects milliseconds
  function sleep (time) {
    return new Promise((resolve) => setTimeout(resolve, time));
  }
  
  
  const header_opacity = ref(0)
  
  
  
  
  const route_to = page_to()
  const menu_store = from_header_menu()
  
  
  
  
  if (menu_store.from_menu == true){
    menu_store.toggle_from_menu()
  
  
  
  
    header_opacity.value = 1;
  
  
    menu_modal_open.value = true;
  
  
    circle_3_opacity.value = 1
    circle_3_margin_top.value = "0vw"
    overlay_opacity.value = 1 
    overlay_visibility.value = "visible"
    menu_container_margin.value = "25vh"
    menu_item_margin_top.value = "0%"
    menu_item_opacity.value = 1
    modal_info_left.value = "0%"
    menu_container_opacity.value = 1
  
    sleep(100).then(() => { circle_white_opacity.value = 0})
        sleep(200).then(() => { menu_item_margin_top.value = "100%"})
        sleep(0.1).then(() => {menu_item_opacity.value = 0})
        sleep(550).then(() => { menu_container_margin.value = "150vh"})
        sleep(1000).then(() => { modal_info_left.value = "100%"})
        sleep(0.1).then(() => { circle_3_margin_top.value = "100vw"})
        sleep(900).then(() => { overlay_opacity.value = 0})
        sleep(1500).then(() => { overlay_visibility.value = 0, menu_container_opacity.value = 0})
        sleep(1600).then(() => { circle_3_opacity.value = 0})
  
      sleep(1600).then(() => {  menu_modal_open.value = false})
      cube_modal.value = (-90);
  
  }
  else if (!String(route_to.current_page_to).includes('fund_pages')){
  
  
    menu_modal_open.value = true;
    header_opacity.value = 1;
  
    circle_3_opacity.value = 1
    circle_3_margin_top.value = "0vw"
    overlay_opacity.value = 1 
    overlay_visibility.value = "visible"
    menu_container_opacity.value = 0
  
  
    sleep(0.1).then(() => { circle_3_margin_top.value = "100vw"})
    sleep(900).then(() => { overlay_opacity.value = 0})
    sleep(1400).then(() => { overlay_visibility.value = 0})
    sleep(1500).then(() => { circle_3_opacity.value = 0})
  
    sleep(1500).then(() => {  menu_modal_open.value = false})
  
  } 
  
  else{
    menu_modal_open.value = false;
    sleep(1400).then(() => { header_opacity.value = 1; })
    
  }
  
  
  
  
  
  
  
      
  
  
  const pause_click = ref(false);
  
  function modal_open() {
  
    if (pause_click.value == false){
    pause_click.value = true
    sleep(1500).then(() => { pause_click.value = false })
    }else{
        pause_click.value = true
        return
      }
  
  
  
      cube_modal.value = (-180);
  
  
  
      if (menu_modal_open.value == false){
        menu_modal_open.value = !menu_modal_open.value
  
  
      sleep(0.1).then(() => { circle_white_margin_left.value = "-80%", menu_container_opacity.value = 0})
      sleep(0.1).then(() => { circle_white_margin_top.value = "100%"})
      sleep(0.1).then(() => { circle_white_opacity.value = 1})
      sleep(0.1).then(() => { circle_black_margin_left.value = "180%"})
      sleep(0.1).then(() => { circle_black_margin_top.value = "-150%"})
      sleep(0.1).then(() => { circle_black_opacity.value = 1})
      sleep(0.1).then(() => { overlay_2_opacity.value = 0})
      sleep(1800).then(() => { circle_3_opacity.value = 1})
      sleep(1).then(() => { circle_3_margin_top.value = "0vw"})
  
  
      
      sleep(0.1).then(() => { menu_container_margin.value = "25vh", menu_container_opacity.value = 1})
      sleep(0.1).then(() => { overlay_opacity.value = 1})
      sleep(0.1).then(() => { overlay_visibility.value = "visible"})
      sleep(250).then(() => { menu_item_margin_top.value = "0%"})
      sleep(250).then(() => { menu_item_opacity.value = 1})
      sleep(400).then(() => { modal_info_left.value = "0%"})
  
      }else{
        
        sleep(100).then(() => { circle_white_opacity.value = 0})
        sleep(100).then(() => { circle_black_opacity.value = 0})
        sleep(1000).then(() => { overlay_opacity.value = 0})
        sleep(1000).then(() => { overlay_visibility.value = "hidden"})
        sleep(300).then(() => { menu_item_margin_top.value = "100%"})
        sleep(0.1).then(() => {menu_item_opacity.value = 0})
        sleep(600).then(() => { menu_container_margin.value = "150vh", menu_container_opacity.value = 1})
        sleep(1000).then(() => { modal_info_left.value = "100%"})
        sleep(0.1).then(() => { circle_3_margin_top.value = "100vw"})
        sleep(1600).then(() => {  menu_modal_open.value = !menu_modal_open.value;})
        sleep(1500).then(() => { circle_3_opacity.value = 0})
        sleep(1700).then(() => { cube_modal.value = (-90);})
        
      }
  
  
      
  }
  
  
  
  
  function startTurning_modal() {
  
      if (menu_modal_open.value == true){
          cube_modal.value = (-180);
      }else{
          cube_modal.value = (-90);
      }
  }
  
  async function startTurning_modal_ticker() {
        await nextTick();
  function myLoop() {         //  create a loop function
      setTimeout(function() {   //  call a 3s setTimeout when the loop is called
        cube_modal.value -= 10   //  your code here
      i++;                    //  increment the counter
      if (i < 5000 || cube_not_reset_modal.value == true) {           //  if the counter < 10, call the loop function
      myLoop();             //  ..  again which will trigger another 
      } else{
        cube_not_reset_modal.value = true;    
      cube_modal.value=0;
      }                      //  ..  setTimeout()
      }, 30)
      }
      myLoop(); 
  }
  
  function stopTurning_modal() {
  
      if (menu_modal_open.value == true){
          cube_modal.value = (-270);
      }else{
          cube_modal.value = 0;
      }
      cube_not_reset_modal.value = false;
  }
  
  
  const nuxtApp = useNuxtApp()
  nuxtApp.hook('page:start', () => {
    startTurning_modal_ticker()
    if (String(route_to.current_page_to).includes('fund_pages')){
    sleep(1600).then(() => { stopTurning_modal()})
    } else {
      sleep(1000).then(() => { stopTurning_modal()})
    }
  })
  
  
  
  
  
  function close_and_route(route_to){
    menu_store.toggle_from_menu()
    console.log(route_to)
  
  navigateTo(route_to)
  }
  
  
  
  onBeforeRouteLeave(() => {
  
    if (String(route_to.current_page_to).includes('fund_pages')){
      header_opacity.value = 0;
    } else {
      header_opacity.value = 1;
    }
  
   })
  
  
  
  const cicle_tansition = ref(null);
  
  function transition_and_route(route_to) {
  
  cicle_tansition.value.animation_and_route(route_to);
  }
  
  
  
  </script>
  
  <style scoped>
  
  
  
  .menu_modal_open{
      display:inline !important;
  }
  
  
  
  
  .white_circle_1{
    width:50vw;
    height:50vw;
    border-radius:100%;
    background-color:#fff;
    z-index:500;
    margin-left:v-bind(circle_white_margin_left);
    left:70%;
    top:-70%;
    margin-top:v-bind(circle_white_margin_top);
    opacity:v-bind(circle_white_opacity);
    position:fixed;
    transform: scale(6.5);
    transition: margin-top 3s ease-in-out, margin-left 3s ease-in-out, transform 2.5s ease-in;
    display:none
  }
  
  
  .white_circle_2{
    width:100vw;
    height:100vw;
    border-radius:100%;
    background-color:#000;
    z-index:400;
    margin-left:v-bind(circle_black_margin_left);
    left:-100%;
    top:100%;
    margin-top:v-bind(circle_black_margin_top);
    opacity:v-bind(circle_black_opacity);
    position:fixed;
    transition: margin-top 2.25s ease-in-out, margin-left 2.25s ease-in;
    display:none
  }
  
  
  .white_circle_3{
    width:150vw;
    height:120vw;
    border-top-left-radius: 50%;
    border-top-right-radius: 50%;
    background-color:#fff;
    z-index:300;
    left:-25vw;
    top:-30vw;
    margin-top:v-bind(circle_3_margin_top);
    opacity:v-bind(circle_3_opacity);
    position:fixed;
    transition:  margin-top 1.5s ease-in;
    display:none
  }
  
  
  
  .menu_modal_container{
      margin-top:25vh;
      display:flex;
      transition:  margin-top 1.25s ease-out;
  }
  
  
  .menu_modal{
      display:none;
      width:100%;
      height:100vh;
      position:fixed;
      z-index:900;
      top:0;
      left:0;
  }
  
  
  
  
  .menu_modal_item{
          color:#000;
          font-size:6.5vw;
          line-height: 1;
          cursor:pointer;
          margin-top:v-bind(menu_item_margin_top);
          opacity:v-bind(menu_item_opacity);
          transition: margin-top 1.55s ease-in-out, opacity 2s ease-in-out;
      }
  
  
  
  
      .modal_info{
          width:35%;
          height:66vh;
          border-left:#000 solid 4px;
          transform: translate(v-bind(modal_info_left), v-bind(modal_info_top));
          transition: all 1s ease-in-out .75s;
      }
  
  
  
  
  
      .transition_overlay{
      width:100vw;
      height:100vh;
      background-color:rgba(114, 114, 114, 0.3);
      z-index:100;
      position:fixed;
      top:0;
      left:0;
      transition: all .5s ease-in-out;
      opacity: v-bind(overlay_opacity);
      visibility: v-bind(overlay_visibility)
  }
  
  .transition_overlay_2{
      width:100vw;
      height:100vh;
      background-color:rgba(114, 114, 114, 0.9);
      z-index:100;
      position:fixed;
      top:0;
      left:0;
      transition: all 1.5s ease-in-out;
      opacity: v-bind(overlay_2_opacity);
      visibility: v-bind(overlay_visibility)
  }
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  .menu_modal_container{
      margin-top:v-bind(menu_container_margin);
      opacity:v-bind(menu_container_opacity);
      display:flex;
  }
  
  .menu_modal_grid{
      width:65%;
      height:70vh;
      display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: repeat(5, 1fr);
  grid-column-gap: 0px;
  grid-row-gap: 0px;
  width:90%;
  margin-left:7%;
  overflow: hidden;
      }
  
      .info_grid{
          display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: repeat(6, 1fr);
  grid-column-gap: 0px;
  grid-row-gap: 20px;
      }
  
      .contact_item{
          margin-top:5px;
      }
      .info_item_title{
          font-size:20px;
          color:#000;
          padding:5px 40px
      }
      .info_item_sub_text{
          font-size:20px;
          color:#000;
          padding:5px 40px
      }
  
  
      .modal_info{
          width:35%;
          height:66vh;
          border-left:#000 solid 4px;
      }
  
      .menu_arrow{
      width:15%;
      margin-left:-15%;
      margin-top:-25%;
      margin-right:5%
  }
  
  
  .menu_modal_item:hover .menu_arrow{
      transition: all ease 1s;
      margin-left:-260px;
      margin-right:20px;
  }
  
  .menu_modal_item:hover{
      padding-left:320px;
      transition: all ease 1s;
  }
  
  .menu_modal{
      display:none;
  
      width:100%;
      height:100vh;
      position:fixed;
      z-index:900;
      top:0;
      left:0
  }
  
  .move{
      position: absolute;
      margin-top:1%;
      color:#000
  }
  
  .header_container{
        margin-top:75px;
      padding: 0 10px;
      align-items: center;
      height: 100px;
      mix-blend-mode: difference;
      opacity:v-bind(header_opacity);
      transition: all 0s ease;
      z-index:1000;
      position:relative;
  }
  
  .header_logo{
      display: flex;
      justify-content: center;
      align-items: center;
  }
  
  .header_menu{
      margin-right:80px;
  }
  
  .header_menu_item{
      transition: all ease .4s;
      mix-blend-mode: difference;
      z-index:5000
  }
  
  .login_item{
      margin-top:-30px
  }
  
  
  
  
  
  
  .cube_container_modal {
      width: 100px;
      height: 80px;
      perspective: 1000px;
      margin-top:-30px;
      margin-left:-50px;
    }
  
    .cube_modal {
      width: 50px;
      height: 50px;
      position: relative;
      transform-style: preserve-3d;
      transform: rotateY(0deg);
      transition: transform 0.5s;
      margin-top:25px;
      margin-left:50px;
    }
  
  
    .face_modal {
      position: absolute;
      width: 50px;
      height: 50px;
      text-align: center;
      font-size: 30px;
      color: white;
      background-color: #000;
      border: #fff 1px solid;
      line-height: 50px;
    }
  
    .front_modal {
      transform: translateZ(25px);;
    }
    
  
    .back_modal {
      transform: rotateY(180deg) translateZ(25px);
    }
  
    .top_modal {
      transform: rotateX(90deg) translateZ(25px);
    }
  
    .bottom_modal {
      transform: rotateX(-90deg) translateZ(25px);
    }
  
    .left_modal {
      transform: rotateY(-90deg) translateZ(25px);
    }
  
    .right_modal {
      transform: rotateY(90deg) translateZ(25px);
    }
  
    .header_logo_modal{
      width:30px;
      mix-blend-mode: difference;
      filter: invert(1);
      margin-top:8px
  }
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  @media only screen and (min-width: 0px) and (max-width: 576px) {
  
  
      .header_container{
      width:65%;
      margin-top:105px
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
  
  
  
  
  .face_modal {
      position: absolute;
      width: 25px;
      height: 25px;
      text-align: center;
      font-size: 15px;
      color: white;
      background-color: #000;
      border: #fff 1px solid;
      line-height: 25px;
    }
  
    .front_modal {
      transform: translateZ(12.5px);;
    }
    
  
    .back_modal {
      transform: rotateY(180deg) translateZ(12.5px);
    }
  
    .top_modal {
      transform: rotateX(90deg) translateZ(12.5px);
    }
  
    .bottom_modal {
      transform: rotateX(-90deg) translateZ(12.5px);
    }
  
    .left_modal {
      transform: rotateY(-90deg) translateZ(12.5px);
    }
  
    .right_modal {
      transform: rotateY(90deg) translateZ(12.5px);
    }
  
  
    .header_logo_modal{
      width:15px;
      mix-blend-mode: difference;
      filter: invert(1);
      margin-top: 5px;
  }
  
  .header_menu_item{
      font-size: 15px;
      color: #fff;
      margin-top:-5px
  }
  
  .login_item{
      margin-top:-60px;
      margin-right:25px;
  }
  
  .info_item_title{
    font-size:80%
  }
  
  .info_item_sub_text{
    font-size:60%
  }
  
  .info_grid{
    margin-left:-10%
  }
  
  .white_circle_3{
    width:280vw;
    height:280vw;
    left:-90vw;
    top:-90vw;
  }
  
  .modal_info{
        width:48%;
    }
    .menu_modal_grid{

margin-left:3%;
    }
  }
  
  
  
  
  
  @media only screen and (min-width: 576px) and (max-width: 768px) {
  
  
  .header_container{
    width:82%;
    margin-top:105px
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
  
  
  
  
  .face_modal {
  position: absolute;
  width: 25px;
  height: 25px;
  text-align: center;
  font-size: 15px;
  color: white;
  background-color: #000;
  border: #fff 1px solid;
  line-height: 25px;
  }
  
  .front_modal {
  transform: translateZ(12.5px);;
  }
  
  
  .back_modal {
  transform: rotateY(180deg) translateZ(12.5px);
  }
  
  .top_modal {
  transform: rotateX(90deg) translateZ(12.5px);
  }
  
  .bottom_modal {
  transform: rotateX(-90deg) translateZ(12.5px);
  }
  
  .left_modal {
  transform: rotateY(-90deg) translateZ(12.5px);
  }
  
  .right_modal {
  transform: rotateY(90deg) translateZ(12.5px);
  }
  
  
  .header_logo_modal{
  width:15px;
  mix-blend-mode: difference;
  filter: invert(1);
  margin-top: 5px;
  }
  
  .header_menu_item{
  font-size: 15px;
  color: #fff;
  margin-top:-5px
  }
  
  .login_item{
  margin-top:-60px;
  margin-right:25px;
  }
  
  
  .info_item_title{
    font-size:100%
  }
  
  .info_item_sub_text{
    font-size:70%
  }
  
  .info_grid{
    margin-left:-10%
  }
  
  
  
  .white_circle_3{
    width:280vw;
    height:280vw;
    left:-90vw;
    top:-90vw;
  }
  
  
  }
  
  
  
  
  
  
  @media only screen and (min-width: 768px) and (max-width: 992px) {
  
  
  .header_container{
  width:92%;
  margin-top:92px
  }
  
  
  
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
  
  
  
  
  .face_modal {
  position: absolute;
  width: 35px;
  height: 35px;
  text-align: center;
  font-size: 15px;
  color: white;
  background-color: #000;
  border: #fff 1px solid;
  line-height: 35px;
  }
  
  .front_modal {
  transform: translateZ(17.5px);;
  }
  
  
  .back_modal {
  transform: rotateY(180deg) translateZ(17.5px);
  }
  
  .top_modal {
  transform: rotateX(90deg) translateZ(17.5px);
  }
  
  .bottom_modal {
  transform: rotateX(-90deg) translateZ(17.5px);
  }
  
  .left_modal {
  transform: rotateY(-90deg) translateZ(17.5px);
  }
  
  .right_modal {
  transform: rotateY(90deg) translateZ(17.5px);
  }
  
  
  .header_logo_modal{
  width:25px;
  mix-blend-mode: difference;
  filter: invert(1);
  margin-top: 5px;
  }
  
  .header_menu_item{
  font-size: 20px;
  color: #fff;
  margin-top:-5px
  }
  
  .login_item{
  margin-top:-47.5px;
  margin-right:25px;
  }
  
  .info_item_title{
    font-size:100%
  }
  
  .info_item_sub_text{
    font-size:70%
  }
  
  .info_grid{
    margin-left:-10%
  }
  
  
  .white_circle_3{
    width:150vw;
    height:140vw;
    left:-25vw;
    top:-100vw;
  }
  
  
  
  
  }
  
  
  
  @media only screen and (min-width: 992px) and (max-width: 1200px) {
  
      .header_container{
  width:95%;
  }
  .login_item{
  margin-top:-30px;
  margin-right:25px;
  
  }
  
  .info_item_title{
    font-size:100%
  }
  
  .info_item_sub_text{
    font-size:70%
  }
  
  .info_grid{
    margin-left:-10%
  }
  
  }
  /* 
  @media only screen and (min-width: 992px) and (max-width: 1100px) {
  
  
  .white_circle_3{
    width:130%;
    height:130%;
    left:-15%;
    top:-130%;
    margin-top:v-bind(circle_3_margin_top);
  }
  
  }
  
  @media only screen and (min-width: 1100px) and (max-width: 1200px) {
  
  
  .white_circle_3{
    width:130%;
    height:130%;
    left:-15%;
    top:-150%;
    margin-top:v-bind(circle_3_margin_top);
  }
  } */
  
  
  @media only screen and (min-width: 1200px) and (max-width: 1400px) {
  
  .header_container{
  width:97%;
  }
  
  .login_item{
  margin-top:-30px;
  margin-right:25px;
  
  }
  
  .info_item_title{
    font-size:100%
  }
  
  .info_item_sub_text{
    font-size:70%
  }
  
  .info_grid{
    margin-left:-10%
  }
  
  
  
  }
  
  /* @media only screen and (min-width: 1200px) and (max-width: 1300px) {
  
    .white_circle_3{
    width:120%;
    height:140%;
    left:-10%;
    top:-170%;
    margin-top:v-bind(circle_3_margin_top);
  }
  }
  
  @media only screen and (min-width: 1300px) and (max-width: 1400px) {
  
    .white_circle_3{
    width:120%;
    height:140%;
    left:-10%;
    top:-190%;
    margin-top:v-bind(circle_3_margin_top);
  }
  }
  
  
  @media only screen and (min-width: 1400px) and (max-width: 1600px) {
  
    .white_circle_3{
    width:120%;
    height:140%;
    left:-10%;
    top:-210%;
    margin-top:v-bind(circle_3_margin_top);
  }
  }
  
  @media only screen and (min-width: 1600px) and (max-width: 5600px) {
  
    .white_circle_3{
    width:130%;
    height:150%;
    left:-15%;
    top:-235%;
    margin-top:v-bind(circle_3_margin_top);
  }
  
  
  } */
  
  

  @media only screen and (min-width: 0px) and (max-width: 768px) {
  .white_circle_2{
  margin-left:calc(v-bind(circle_black_margin_left) + 100px);
  margin-top:calc(v-bind(circle_black_margin_top) - 800px);
  width:300vw;
  height:300vw;
}

.white_circle_1{
  width:200vw;
  height:200vw;
  margin-left:v-bind(circle_white_margin_left);
  margin-top:v-bind(circle_white_margin_top);
}

}

  
  </style>