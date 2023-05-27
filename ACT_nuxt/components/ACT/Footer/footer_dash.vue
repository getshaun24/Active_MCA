<template>

    <footer>
     <div class="footer">
               <div class="footer_content">
                 <div class="footer_grid_left">
                   <div class="footer_elm_left">
                     <h5 style="margin:0">Footer</h5>
                     <span class="footer_subheading">In Progress.</span>
                   </div>
                   <NuxtLink to="/"><img src="~/assets/content/homepage/home_1.png" loading="lazy" alt="" class="footer_logo" /></NuxtLink>
                   <div class="footer_elm_left" style="padding-top:5px">
                     <span class="footer_subheading">Copyright © GET MEDIA 2022</span>
                   </div>
                 </div>
 
               </div>
             <!-- <div class="paperOverlay" style="opacity:.6; transform: rotate(180deg);"></div> -->
     </div>
   </footer>
 </template>
 
 <script setup>
 
 </script>
 
 <style scoped>
 
 footer{
   z-index:-1;
   bottom:0;
     margin-top:calc(-1 * (100vh - 405px));
     background-color: #fff;
 }
 .footer{
     background-color: #e8f3ff1d;
     height:400px;
     width:100%;
     z-index:1;
     border-top: 3px solid #deae00ca;
     position: fixed;
     bottom:0;
     margin-top:-100vh
 }
 
 
 
 
 
 
 
 
 
 
 .footer_logo{
 color: var(--theme-color)
 }
 
 .footer_elm_left{
 padding-bottom:10px;
 white-space: nowrap;
 color: var(--theme-color) !important;
 }
 
 .footer_elm_right{
 padding:25px;
 white-space: nowrap;
 color: var(--theme-color) !important
 }
 
 .footer_subheading{
 white-space: nowrap;
 color: var(--footer_subheading) !important;
 text-decoration: none !important;
 line-height:2.5
 }
 
 
 .footer_content {
 padding-top: 40px;
 padding-bottom: 35px;
 padding-left: 320px;
 padding-right: 50px;
 
 }
 
 
 
 
   .footer_grid_left {
 display: grid;
 grid-template-columns: repeat(1, 1fr);
 grid-template-rows: repeat(3, 1fr);
 grid-column-gap: 0px;
 grid-row-gap: 0px;
 width:50%;
 }
 
 .footer_grid_right {
 display: grid;
 grid-template-columns: repeat(3, 1fr);
 grid-template-rows: repeat(3, 1fr);
 grid-column-gap: 0px;
 grid-row-gap: 0px;
 width:40%;
 margin-left:57%;
 }
 
 
 .footer_up{
 grid-row: span 2;
 padding-left:40%;
 background-color: transparent;
 border-color: transparent;
 color: var(--theme-color) !important;
 margin-top:30px
 
 }
 
 .footer_up_text {
 margin-top: 30px;
 line-height: 36px;
 -webkit-writing-mode: vertical-rl;
 -ms-writing-mode: tb-rl;
 writing-mode: vertical-rl;
 }
 
 
 
 .footer_up_arrow{
 display: block;
 width: 36px;
 height: 36px;
 border-radius: 50%;
 border: 1px solid var(--footer_subheading);
 overflow: hidden;
 cursor: pointer;
 position: absolute;
 margin-right:-35px;
 margin-top:-50px
 }
 
 
 .footer_logo{
   width:50%
 }
 
 
 
 
 
 
 </style>