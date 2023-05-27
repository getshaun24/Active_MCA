<template>
    <div>
      <MainTransition ref="main_tansition"/>
    <div class="header">
      <div class="menu_logo">


      
        <img class="dahboard_logo" src='~/assets/content/homepage/home_1.png'>


        
      </div>
      <div class="header_menu">
        <div class="top_header_link" :class="[is_active == 'overview_active' ? 'is_active': '']" @click="transition_and_route('/investor_dashboard/investor_home')">Overview</div>
        <div :class="[is_active == 'agreements_active' ? 'is_active': '']" class="top_header_link" @click="transition_and_route('/investor_dashboard/agreements')">Agreements</div>

        <!-- <div class="top_header_link notify" :class="[is_active == 'documents_active' ? 'is_active': '']" @click="transition_and_route('/investor_dashboard/document_upload')">Documents</div> -->

        
        <div class="top_header_link" @click="logout">Log Out</div>


      </div>


      
<!-- 
      <div class="search_bar_header">
        <input type="text" placeholder="Search a person or business">
      </div> -->



      <div class="header_profile">
        <a href="" class="notification" style="margin-top:8px">
          <span class="notification_number">{{ notification_count }}</span>
          <svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                stroke-linejoin="round">
                <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0" />
            </svg>
        </a>

        <!-- <img @click="show_dropdown" class="profile_img" src="~/assets/content/dashboard/default_user.png" alt=""> -->
      </div>



      <ACTButtonsBurgerButton/>

      <!-- <InvestorDashModalMenu/> -->


    </div>




    <div ref="profile_drop" class="profile_dropdown" :class="{dropdown_is_visible:dropdown_visible}">
      <div class="profile_menu">
        <div class="side-menu">
          <img class="profile_img_dropdown" src="~/assets/content/dashboard/default_user.png" alt="">
          <a class="side_menu_link" href="#">
           
            Profile
          </a>
          <a class="side_menu_link" href="#">
           
            Settings
          </a>
          <a class="side_menu_link" href="#">
            
            Security
          </a>
          <a class="side_menu_link" href="#" style="font-size:25px; padding:20px; margin-top:10px">
            <div class="logout_circle"></div>
            Log Out
          </a>
          <div class="background_profile"></div>
        </div>
      </div>
    </div>

</div>



</template>




<script setup>
import { onClickOutside } from '@vueuse/core'
const config = useRuntimeConfig()
const csrf_cookie = useCookie('csrf_access_token')
const props = defineProps(['is_active'])
const dropdown_visible = ref(false);
const profile_drop = ref(null)
const notification_count = useCookie('notification_count')

    onClickOutside(profile_drop, (event) => {
    if(dropdown_visible.value == true) {
        show_dropdown()
    }}) 



function show_dropdown() {
    dropdown_visible.value = !dropdown_visible.value;
}




const main_tansition = ref(null);
function transition_and_route(route_to) {
    main_tansition.value.animation_and_route(route_to);
}


const user_ID = useCookie('user_ID')
const rocket_chat_auth_token = useCookie('rocket_chat_auth_token')
function logout() {

  fetch(`${config.flask_url}/api/rocket_chat/rocket_chat_logout/`, {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({user_ID: user_ID.value, rocket_chat_auth_token:rocket_chat_auth_token.value})
  })
  .then((response) => response.json())
  .then((data) => {
    alert('Success')
  })
  .catch(error => {
      alert('Error')
  });

  const auth_cookie = useCookie('auth_cookie')
  auth_cookie.value = null
  const csrf_cookie = useCookie('csrf_access_token')
  csrf_cookie.value = null
  const access_cookie = useCookie('access_token_cookie')
  access_cookie.value = null
  transition_and_route('/login_pages/login')
}



</script>





<style scoped>


.dahboard_logo{
  width:110px;
  margin-left:15px;
  cursor:pointer;
  z-index:100
}
.dropdown_is_visible {
    display: block !important;
}


.profile_img {
border: 2px solid var(--theme-bg-color);
border-radius: 100%;
cursor: pointer;
}



.header {
    position:fixed;
    top:0;
    left:0;
    z-index:20;
display: flex;
align-items: center;
height: 80px;
width: 100%;
border-bottom: 1px solid var(--border-color);
white-space: nowrap;
background-color: var(--theme-bg-color);
}
@media screen and (max-width: 480px) {
.header {
padding: 0 16px;
}
}
.header_menu {
display: flex;
align-items: center;
}
.top_header_link:first-child {
margin-top:13px;
padding: 20px 30px;
padding-bottom: 30px;
text-decoration: none;
color: var(--inactive-color);
border-bottom: 2px solid transparent;
transition: 0.3s;
}
.top_header_link {
padding: 20px 30px;
padding-bottom: 30px;
text-decoration: none;
color: var(--inactive-color);
border-bottom: 2px solid transparent;
transition: 0.5s;
margin-top:13px;
cursor:pointer
}


.is_active {
color: var(--header_menu_hover) !important;
border-bottom: 3.5px solid var(--header_menu_hover) !important;
}

.top_header_link:hover {
color: var(--header_menu_hover);
border-bottom: 3.5px solid var(--header_menu_hover);
}

.top_header_link:first-child:hover {
color: var(--header_menu_hover);
border-bottom: 3.5px solid var(--header_menu_hover);
}




.notify {
position: relative;
}
.notify:before {
content: "";
position: absolute;
background-color: #3a6df0;
width: 6px;
height: 6px;
border-radius: 50%;
right: 20px;
top: 16px;
}


/* https://yoksel.github.io/url-encoder/ */
.menu_logo {
    margin-left:10px;
margin-right: 145px;
margin-top: 5px;
color: var(--theme-color)
}




.search_bar_header {
height: 40px;
display: flex;
width: 100%;
max-width: 400px;
padding-left: 16px;
border-radius: 4px;
margin-left:5%;
}
.search_bar_header input {
width: 100%;
height: 100%;
border: none;
background-color: var(--search-bg);
border-radius: 4px;
font-size: 15px;
font-weight: 500;
padding: 0 20px 0 40px;
box-shadow: 0 0 0 2px rgba(134, 140, 160, 0.02);
background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 56.966 56.966' fill='%23717790c7'%3e%3cpath d='M55.146 51.887L41.588 37.786A22.926 22.926 0 0046.984 23c0-12.682-10.318-23-23-23s-23 10.318-23 23 10.318 23 23 23c4.761 0 9.298-1.436 13.177-4.162l13.661 14.208c.571.593 1.339.92 2.162.92.779 0 1.518-.297 2.079-.837a3.004 3.004 0 00.083-4.242zM23.984 6c9.374 0 17 7.626 17 17s-7.626 17-17 17-17-7.626-17-17 7.626-17 17-17z'/%3e%3c/svg%3e");
background-size: 14px;
background-repeat: no-repeat;
background-position: 16px 48%;
color: var(--theme-color);
}
.search_bar_header input::-moz-placeholder {
    color: rgba(175, 175, 175, 0.3);
font-size: 15px;
font-weight: 500;
}
.search_bar_header input:-ms-input-placeholder {
    color: rgba(175, 175, 175, 0.3);
font-size: 15px;
font-weight: 500;
}
.search_bar_header input::placeholder {
    color: rgba(175, 175, 175, 0.3);
font-size: 15px;
font-weight: 500;
}

.header_profile {
display: flex;
align-items: center;
padding: 0 16px 0 40px;
margin-left: auto;
flex-shrink: 0;
margin-right:2.5%;
margin-top:5px
}
.header_profile svg {
width: 22px;
color: var(--theme-color);
flex-shrink: 0;
}

.notification {
position: relative;
cursor: pointer;
}
.notification_number {
position: absolute;
background-color: #3a6df0;
width: 105%;
height: 16px;
border-radius: 50%;
font-size: 10px;
display: flex;
align-items: center;
justify-content: center;
color: #fff;
right: -6px;
top: -6px;
}
.notification + svg {
margin-left: 22px;
}


.profile_img {
width: 32px;
height: 32px;
-o-object-fit: cover;
object-fit: cover;
border: 2px solid #198de6;
margin-left: 22px;
border-radius: 100%;
}



.profile_dropdown{
width:300px;
height:370px; 
position:absolute;
margin-top:80px;
z-index:100;
right:20px;
margin-right:30px;
display:none; 
background-size: cover;
}

.profile_menu{
width:100%;
height:100%;
padding:5%;
position:relative;
-webkit-backdrop-filter: blur(20px);
backdrop-filter: blur(20px);
background-color: var(--background_overlay);
border: #006bde40 1px solid
}

.logout_circle{
width:25px;
height:25px;
background-color: #cf560b;
border-radius:100%;
margin-right:5%
}


.side-menu {
display: flex;
flex-direction: column;
white-space: nowrap;
}



.side-menu svg {
width: 16px;
margin-right: 10px;
}

.profile_img_dropdown {
width: 100px;
height: 100px;
border-radius: 50%;
-o-object-fit: cover;
object-fit: cover;
border: 2px solid var(--header_menu_hover);
margin-left: 85px;
margin-bottom:15px;
object-position:top;
}



.side_menu_link {
text-decoration: none;
color: #000;
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


@media only screen and (min-width: 0px) and (max-width: 430px) {

.header_menu{
display:none;
}

.menu_logo {
    margin-left:22px;
margin-right: 15%;
}

}



@media only screen and (min-width: 430px) and (max-width: 576px) {

.header_menu{
display:none;
}

.menu_logo {
    margin-left:22px;
margin-right: 25%;
}

}

@media only screen and (min-width: 576px) and (max-width: 768px) {

    .header_menu{
display:none;
}

.menu_logo {
    margin-left:22px;
margin-right: 42%;
}

}

@media only screen and (min-width: 768px) and (max-width: 992px) {

    .menu_logo {
    margin-left:22px;
margin-right: 42px;
}


.top_header_link:first-child {
margin-top:27px;
padding: 20px 18px;
padding-bottom: 20px;
border-bottom: 2px solid transparent;
font-size:12px
}
.top_header_link {
    padding: 20px 18px;
    padding-bottom: 20px;
margin-top:27px;
font-size:12px
}


}


@media only screen and (min-width: 835px) and (max-width: 992px) {
.header_menu{
margin-right:7%
}
}

@media only screen and (min-width: 920px) and (max-width: 992px) {
.header_menu{
margin-right:15%
}
}


@media only screen and (min-width: 992px) and (max-width: 1200px) {

    .menu_logo {
    margin-left:22px;
margin-right: 134px;
}

    .top_header_link:first-child {
margin-top:25px;
padding: 20px 18px;
padding-bottom: 18px;
border-bottom: 2px solid transparent;
font-size:15px
}
.top_header_link {
    padding: 20px 18px;
    padding-bottom: 18px;
    margin-top:25px;
font-size:15px
}


}






@media only screen and (min-width: 1200px) and (max-width: 1400px) {
}

@media only screen and (min-width: 1400px) and (max-width: 1600px) {
}

@media only screen and (min-width: 1600px) and (max-width: 5600px) {
}





</style>





