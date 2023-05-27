<template>
    




    <div class="left_side" :class="{left_side_closed:minimized}">

      <MainTransition ref="main_tansition"/>


        <div class="side_wrapper">

            <div class="close_container" :class="{left_side_closed:minimized, hide_it:minimized}" @click="minimize_side"><span class="close_text">Close Menu</span> <span class="left_side_minimize">⤵</span></div>
            <div class="close_container" :class="{left_side_closed:!minimized, hide_it:!minimized}" @click="minimize_side"><span class="left_side_maximize">⤴ </span><span class="verticle_text">Open Menu</span></div>


            <div :class="{hide_it:minimized}">

          <div class="side_title">Pages</div>
          <div class="side_menu">


    <div :class="[is_active == 'overview_active' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/dashboard_home')" class="side_menu_link"> Overview </div>


    <div :class="[is_active == 'request_settlement_active' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/request_settlement')" class="side_menu_link"> Request Settlement </div>

    <div :class="[is_active == 'demo' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/settlement_demo_page')" class="side_menu_link"> Demo Settlement Page</div>

    <div :class="[is_active == 'chat' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/chat')" class="side_menu_link">Chat</div>
   
    <!-- <div :class="[is_active == 'instant_invest' ? 'is_active': '']" @click="transition_and_route('/investor_dashboard/investor_home')" class="side_menu_link">Instant Invest</div> -->

    <div :class="[is_active == 'alerts' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/dashboard_home')" class="side_menu_link">Incoming Settlements</div>

    <div :class="[is_active == 'transactions' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/dashboard_home')" class="side_menu_link" >Messages</div>

    <div :class="[is_active == 'notifications' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/dashboard_home')" class="side_menu_link">Closed Settlements</div>

    <div :class="[is_active == 'contact' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/dashboard_home')" class="side_menu_link">Settlement Stats</div>

    <div  :class="[is_active == 'agreements_active' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/dashboard_home')" class="side_menu_link">Payments</div>

    <div :class="[is_active == 'documents_active' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/dashboard_home')" class="side_menu_link">Notifications</div>

    
    <div :class="{hide_it:!extra_menu_items}">

    <div  :class="[is_active == 'agreements_active' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/dashboard_home')" class="side_menu_link">Payments</div>

    <div :class="[is_active == 'documents_active' ? 'is_active': '']" @click="transition_and_route('/user_dashboard/dashboard_home')" class="side_menu_link">Notifications</div>

    <div class="side_menu_link">Logout</div>

    </div>
 
           
          </div>

        <div class="side_wrapper contact_wrapper">
          <div class="side_title">Contacts Online<span class="updates">300</span></div>

            <div class="side_menu">
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 1 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 2 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 3 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 4 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 5 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 6 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div style="background-color:orange; filter: drop-shadow(1px 1px 3px orange);" class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 7 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div style="background-color:orange; filter: drop-shadow(1px 1px 3px orange);" class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 8 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div style="background-color:orange; filter: drop-shadow(1px 1px 3px orange);" class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 9 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>

            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 1 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 2 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 3 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 4 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 5 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 6 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div style="background-color:orange; filter: drop-shadow(1px 1px 3px orange);" class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 7 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div style="background-color:orange; filter: drop-shadow(1px 1px 3px orange);" class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 8 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>
            <a class="chat_menu_link" href="#">
                <img class="sidebar_chat_img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
                <div style="background-color:orange; filter: drop-shadow(1px 1px 3px orange);" class="chat_status_circle"></div>
             <p class="chat_menu_text">Person 9 <br><span class="chat_menu_link_subtext">Company xyz</span></p> 
            </a>



          </div>


            <!-- <Nuxt-link to="/fund_pages/helpful" class="chat_menu_link">
                <img class="sidebar_chat_img" src="~/assets/content/investments/invest_5.jpg" alt="">
                <div class="chat_status_circle_closing_soon"></div>
             <p class="chat_menu_text">Helpful </p> 
            </Nuxt-Link> -->
           
            <div class="fund_padding"></div>
          </div>
        </div>

    </div>

    </div>
        
     




</template>


<script setup>

import { useWindowSize } from '@vueuse/core'

const props = defineProps(['is_active'])


const { width, height } = useWindowSize()


const minimized = ref(false);
const extra_menu_items = ref(false);


function minimize_side() {
    minimized.value = !minimized.value;
    extra_menu_items.value = true;
}



watch(width, (newWidth) => {
    if (newWidth < 768) {
    minimized.value = true;
    extra_menu_items.value = true;
    } else{
    minimized.value = false;
    extra_menu_items.value = false;
    }
})

onMounted(() => {

    if (width.value < 768) {
    console.log('minimized')
    minimized.value = true;
    extra_menu_items.value = true;
} else{
    minimized.value = false;
    extra_menu_items.value = false;
}

})

const main_tansition = ref(null);
function transition_and_route(route_to) {
    main_tansition.value.animation_and_route(route_to);
}



</script>



<style scoped>


    
.left_side::-webkit-scrollbar {
        width: 3px !important;
        border-radius: 10px !important;
    }
    
    .left_side::-webkit-scrollbar-thumb {
        background: rgba(0, 149, 255, 0.676) !important;
        border-radius: 10px !important;
    }
    


.is_active {
  border: 1px solid #198de679
}


.left_side {
width: 250px;
border-right: 1px solid var(--border-color);
padding: 15px 15px;
height:100vh;
overflow-y: scroll !important;
transition: all .5s ease-in-out;
position: fixed;
z-index:10;
background-color: var(--theme-bg-color);
top:80px;
left:0
}


.hide_it {
    display:none !important
}

.sidebar_chat_img {
width: 70px;
height: 70px;
border-radius: 100%;
-o-object-fit: cover;
object-fit: cover;
border: 2px solid #198de6;
margin-right:20px
}

.chat_status_circle {
  border-radius: 50%;
  width: 15px;
  height: 15px;
  background-color:green;
  position: relative;
    margin-left:-38px;
    margin-top:52px;
    margin-right:20px;
    filter: drop-shadow(1px 1px 3px green);
    border:.25px solid rgba(255, 255, 255, 0.5);
}

.chat_status_circle_closing_soon {
  border-radius: 50%;
  width: 15px;
  height: 15px;
  background-color:orange;
  position: relative;
  margin-left:-38px;
    margin-top:52px;
    margin-right:20px;
    filter: drop-shadow(1px 1px 3px orange);
    border:.25px solid rgba(255, 255, 255, 0.5);
}


.chat_menu_text{
    margin-top:25px;
    font-size:18px
}



.side_wrapper  {
margin-top: 20px;
}

.contact_wrapper{
    margin-top: 50px;
}

.side_title {
color: var(--inactive-color);
margin-bottom: 14px;
white-space: nowrap;
}

.side_menu {
display: flex;
flex-direction: column;
white-space: nowrap;
}

.side_menu_link {
text-decoration: none;
color: var(--theme-color);
display: flex;
align-items: center;
font-weight: 400;
padding: 10px;
font-size: 18px;
border-radius: 6px;
transition: 0.3s;
cursor: pointer;
margin-top:10px
}

.side_menu_link:hover {
background-color: var(--hover-menu-bg);
}


.chat_menu_link {
text-decoration: none;
color: var(--theme-color);
display: flex;
align-items: center;
font-weight: 400;
padding: 0px 10px;
font-size: 18px;
border-radius: 6px;
transition: 0.3s;
cursor: pointer;
}

.chat_menu_link_subtext {
text-decoration: none;
color: var(--theme-color);
display: flex;
align-items: center;
font-weight: 200;
padding: 7px;
padding-left:0;
font-size: 12px;
border-radius: 6px;
transition: 0.3s;
cursor: pointer;
}

.chat_menu_link:hover {
background-color: var(--hover-menu-bg);
}



.side_menu svg {
width: 16px;
margin-right: 10px;
}

.updates {
position: relative;
top: 0px;
margin-left: 70px;
width: 18px;
height: 18px;
font-size: 13px;
background-color: #3a6df0;
padding:5px;
border-radius:10px;
color:#fff
}





.left_side_minimize{
    display:none
}

.left_side_maximize{
    display:none
}



.close_text{
    display: none;
}

.fund_padding{
    padding-bottom:25vh
}

@media only screen and (min-width: 0px) and (max-width: 576px) {
    .side_menu_link {
        font-size: 12px;
        }

        .chat_menu_text{
    margin-top:10px;
    font-size:12px
}

.sidebar_chat_img {
width: 50px;
height: 50px;
margin-right:15px
}


.chat_status_circle {
  width: 12px;
  height: 12px;
    margin-left:-32px;
    margin-top:40px;
    margin-right:20px;
}

.chat_status_circle_closing_soon {
    width: 12px;
  height: 12px;
    margin-left:-32px;
    margin-top:40px;
    margin-right:20px;
}


.left_side {
width: 150px;
padding: 15px 7px 15px 10px;
}


.side_title {
font-size: 12px;
white-space: normal;
}


.chat_menu_link {
padding: 8px 2px;
}

.left_side_minimize{
    color:#000;
    display:block;
    margin-left:70%;
    margin-top:7px;
    font-size:20px;
    cursor:pointer;
    transform: rotate(105deg);
}

.left_side_maximize{
    color:#000;
    display:block;
    margin-top:50%;
    font-size:20px;
    cursor:pointer;
    transform: rotate(105deg);
}


.close_container{
    margin-top:5%;
        margin-bottom:20%;
    height:200%;
    padding-top:10px;
    cursor: pointer;
    z-index:20;
}



.left_side_closed{
    width: 20px !important;
    transition: all 0.5s ease-in-out;
}

.verticle_text{
    writing-mode: vertical-rl;
  text-orientation: upright;
  color:#000;
  margin-top:30px;
  cursor:pointer;
}

.close_text{
    color:#000;
    display:block;
    position:absolute;
    cursor:pointer;
}

}

@media only screen and (min-width: 576px) and (max-width: 768px) {

    .side_menu_link {
        font-size: 12px;
        }

        .chat_menu_text{
    margin-top:10px;
    font-size:12px
}

.sidebar_chat_img {
width: 50px;
height: 50px;
margin-right:15px
}


.chat_status_circle {
  width: 12px;
  height: 12px;
    margin-left:-32px;
    margin-top:40px;
    margin-right:20px;
}

.chat_status_circle_closing_soon {
    width: 12px;
  height: 12px;
    margin-left:-32px;
    margin-top:40px;
    margin-right:20px;
}


.left_side {
width: 150px;
padding: 15px 7px 15px 10px;
}



.side_title {
font-size: 12px;
white-space: normal;
}


.chat_menu_link {
padding: 8px 2px;
}


.left_side_minimize{
    color:#000;
    display:block;
    margin-left:70%;
    margin-top:7px;
    font-size:20px;
    cursor:pointer;
    transform: rotate(105deg);
}

.left_side_maximize{
    color:#000;
    display:block;
    margin-top:50%;
    font-size:20px;
    cursor:pointer;
    transform: rotate(105deg);
}


.close_container{
    margin-top:5%;
        margin-bottom:20%;
    height:200%;
    padding-top:10px;
    cursor: pointer;
    z-index:20;
}

.left_side_closed{
    width: 20px !important;
    transition: all 0.5s ease-in-out;
}

.verticle_text{
    writing-mode: vertical-rl;
  text-orientation: upright;
  color:#000;
  margin-top:30px;
  cursor:pointer;
}

.close_text{
    color:#000;
    display:block;
    position:absolute;
    margin-top:-7px;
    cursor:pointer;
}



}

@media only screen and (min-width: 768px) and (max-width: 992px) {

    .side_menu_link {
        font-size: 12px;
        }

        .chat_menu_text{
    margin-top:10px;
    font-size:13px
}

.sidebar_chat_img {
width: 60px;
height: 60px;
margin-right:15px
}


.chat_status_circle {
  width: 13px;
  height: 13px;
    margin-left:-32px;
    margin-top:40px;
    margin-right:20px;
}

.chat_status_circle_closing_soon {
    width: 13px;
  height: 13px;
    margin-left:-32px;
    margin-top:40px;
    margin-right:20px;
}


.left_side {
width: 180px;
padding: 15px 7px 15px 2px;
margin-left:7px
}



.side_title {
font-size: 12px;
white-space: normal;
}


.chat_menu_link {
padding: 8px 6px;
}




}

@media only screen and (min-width: 992px) and (max-width: 1200px) {
}

@media only screen and (min-width: 1200px) and (max-width: 1400px) {
}

@media only screen and (min-width: 1400px) and (max-width: 1600px) {
}

@media only screen and (min-width: 1600px) and (max-width: 5600px) {
}




</style>






