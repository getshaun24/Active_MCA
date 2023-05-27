<template>
    
    <div class="light_mode" style="overflow-x:hidden">
        <UserDashDashboardHeader v-bind="active_page" />
        <UserDashLeftSidebar v-bind="active_page"/>
        <ACTGSAPScrollSmoother>
            
            <div class="navigation_header">
                <div class="nav_menu_title">Request A New Settlement </div>
                <!-- <div class="header_menu">
                    <div class="navigation_menu is-active" href="#">xxx</div>
                    <div class="navigation_menu" href="#">xxx</div>
                    <div class="navigation_menu" href="#">xxx</div>
                </div> -->
            </div>
            <div class="dashboard_inner_section" ref="el">
                <div class="main_content_container">
                  <div class="paperOverlay"></div>
  
                  

                  <UserDashNewRequest/>






                </div>
            </div>
            
            <!-- div for footer scroll over -->
            <div style="padding-bottom:1px"></div>
            <ACTFooterDash/>
        </ACTGSAPScrollSmoother>
        <!-- <UserDashDashboardFooter/> -->
  
        
    </div>
    
    
    
    
    
  </template>
  
  
  
  
  
  
  <script setup>
  import { useResizeObserver } from '@vueuse/core'
  import { useWindowSize } from '@vueuse/core'
  
  
  // onBeforeMount(() => { if (authCookieRefresh()) {ACT_investor_overview()} })
  
  const config = useRuntimeConfig()




  
        
  const cookie_options = {default:()=> '', watch:true, maxAge:1800}
  
  const notification_count = useCookie('notification_count', cookie_options)

  const active_page = {is_active: "request_settlement_active"}
  


    const el = ref()
    const inner_height = ref()

  
  const dashboard_inner_section_padding = ref('0px')

  useResizeObserver(el, (entries) => {
        const entry = entries[0]
        const { width, height } = entry.contentRect
          inner_height.value = height
          console.log('inner_height x -- ', height)
          const window_size = useWindowSize()
          console.log('window_height -- ', window_size.height.value)
          if (inner_height.value < window_size.height.value) {
          dashboard_inner_section_padding.value = (window_size.height.value - inner_height.value) - 130 + 'px'
          }
  
      })
  
  </script>
    
    
    
    
    
    
    
    
    <style scoped>
    


    
    .header_menu {
        display: flex;
        align-items: center;
    }
    
    .is-active {
        color: var(--header_menu_hover) !important;
        border-bottom: 3.5px solid var(--header_menu_hover) !important;
    }
    
    
    
    
    .navigation_menu {
        padding: 20px 30px;
        padding-bottom: 18px;
        text-decoration: none;
        color: var(--inactive-color);
        border-bottom: 2px solid transparent;
        transition: 0;
        cursor: pointer;
    }
    
    .navigation_menu:hover {
        color: var(--header_menu_hover);
        font-weight: bold;
    }
    
    
    
    
    .dashboard_inner_section{
        margin-bottom: 81px; 
        padding-bottom:v-bind(dashboard_inner_section_padding);
        width:calc(100vw - 250px); 
        margin-left:250px;
        border-bottom: 1px solid rgb(167, 211, 232, 0.4);
        /* background-color:var(--inner_background); */
          background-color:#fff;
        z-index:1
    }
    
    .main_content_container{
        width:80%; 
        margin-right:10%;
        margin-left:10%;
        z-index:1
    }
    
    
    
    
    
    
    .navigation_header {
        display: flex;
        align-items: center;
        border-bottom: 1px solid var(--border-color);
        height: 58px;
        flex-shrink: 0;
        margin-top:80px;
        width:calc(100vw - 250px); 
        margin-left: 250px;
        background-color: #ffffff;
    }
    
    
    
    .nav_menu_title {
        text-decoration: none;
        color: var(--theme-color);
        padding: 0 30px;
        margin-left:25px;
        padding-right:50px;
    }
    
    
    
    ::-webkit-scrollbar {
        width: 3px;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 149, 255, 0.676);
        border-radius: 10px;
    }
    
    
    
    
    
    
    
    
    
    
    
    
    
    @media only screen and (min-width: 0px) and (max-width: 576px) {
        .dashboard_inner_section{
            width:calc(100vw - 20px); 
            margin-left:20px;
        }
        
        .navigation_header {
            width:100vw;
            margin-left:20px;
        }
        
    }
    
    @media only screen and (min-width: 576px) and (max-width: 768px) {
        .dashboard_inner_section{
            width:calc(100vw - 20px); 
            margin-left:20px;
        }
        
        .navigation_header {
            width:100vw;
            margin-left:20px;
        }
        
    }
    
    @media only screen and (min-width: 768px) and (max-width: 992px) {
        
        .dashboard_inner_section{
            width:100vw;
            margin-left:180px;
        }
        
        .navigation_header {
            width:100vw;
            margin-left:150px;
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
  
  
  
  
  
  
  
  
  
  
  
  