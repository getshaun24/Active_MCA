<template>
     <div class="header" ref="target">
        <NuxtLink to="/" class="menu_logo">
        <SvgLogo v-bind="svg_header"/>
            
        
    </NuxtLink>


    <div class="header_menu_links" :class="{ hide_elm: isHiddenn }">
    <HeadersDashboardHeaderTopHeaderLink v-bind="top_links"/>
    </div>
      


      <div class="search_bar_header" :style="{ marginLeft: search_header_margin_left, width: search_header_width,  Maxwidth: search_bar_header_max_width }">
        <input @input="search_filter" @blur="header_search_blur" @focus="header_search_focus" type="text" placeholder="Search a person or business">
      </div>




      <div class="header-profile" :class="{ hide_elm: isHiddenn }">

        <a href="" class="notification" style="margin-top:8px">
          <span class="notification-number">3</span>
          <svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                stroke-linejoin="round">
                <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0" />
            </svg>
        </a>


       
       
        <img @isactive="hover_listener" :isactive="active_el" class="profile-img" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
      </div>
    </div>


    <HeadersDashboardHeaderProfileDropdown/>


</template>



<script setup>


import { ref } from 'vue'

const svg_header = {
  width: 100,  
}




    const top_links = {
  links:[
  {button_title: 'xxx', notify: false, active: true},
  {button_title: 'xxx', notify: true, active: false},
  {button_title: 'xxx', notify: false, active: false},
  {button_title: 'Reminder', notify: true, active: false},
]
}



const isHiddenn = ref(false)
const search_header_margin_left = ref('5%')
const search_header_width = ref('20%')
const search_bar_header_max_width = ref('400px')




// expand the search bar in the table and remove other elements
function header_search_focus(){
    isHiddenn.value = true
    search_header_margin_left.value = '-10%'
    search_header_width.value = '50%'
    search_bar_header_max_width.value = '1000px'
}


function header_search_blur(){
isHiddenn.value = false
search_header_margin_left.value = '5%'
search_header_width.value = '20%'
search_bar_header_max_width.value = '400px'
}






</script>


<style scoped>
.hide_elm {
    visibility: hidden;
}
.header_menu_links {
    display: flex;
    align-items: center;
}
img {
    max-width: 100%;
}
.profile-img {
    border: 2px solid var(--theme-bg-color);
    border-radius: 100%;
}
.profile_menu {
    width: 100%;
    height: 100%;
    padding: 5%;
    position: relative;
    -webkit-backdrop-filter: blur(20px);
    backdrop-filter: blur(20px);
    background-color: var(--background_overlay);
    border: #deae0040 1px solid;
}
.header {
    display: flex;
    align-items: center;
    flex-shrink: 0;
    height: 80px;
    width: 100%;
    border-bottom: 1px solid var(--border-color);
    padding: 0 30px;
    white-space: nowrap;
    position: fixed;
    z-index: 2;
    background-color: #fff;
}
@media screen and (max-width: 480px) {
    .header {
        padding: 0 16px;
    }
}
.menu_logo {
    margin-right: 210px;
    margin-top: 15px;
    flex-shrink: 0;
    color: var(--theme-color);
}
.search_bar_header {
    height: 40px;
    display: flex;
    width: 30%;
    padding-left: 16px;
    border-radius: 4px;
    margin-left: 5%;
    transition: all 1s ease;
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
    color: rgba(175, 175, 175, 1);
    font-size: 15px;
    font-weight: 500;
}
.search_bar_header input:-ms-input-placeholder {
    color: rgba(175, 175, 175, 1);
    font-size: 15px;
    font-weight: 500;
}
.search_bar_header input::placeholder {
    color: rgba(175, 175, 175, 1);
    font-size: 15px;
    font-weight: 500;
}
.header-profile {
    display: flex;
    align-items: center;
    padding: 0 16px 0 40px;
    margin-left: auto;
    flex-shrink: 0;
    margin-right: 2.5%;
}
.header-profile svg {
    width: 22px;
    color: var(--theme-color);
    flex-shrink: 0;
}
.notification {
    position: relative;
    cursor: pointer;
}
.notification-number {
    position: absolute;
    background-color: #3a6df0;
    width: 16px;
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
.profile-img {
    width: 32px;
    height: 32px;
    -o-object-fit: cover;
    object-fit: cover;
    border: 2px solid #198de6;
    margin-left: 22px;
    border-radius: 100%;
}
input:focus {
    outline: 0;
}




</style>