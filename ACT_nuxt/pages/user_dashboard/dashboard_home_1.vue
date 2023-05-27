<template>



    <div class="dashboard_body theme_colors">
      <div class="dashboard">
        <ACTHeadersDashboardOLDHeaderTopHeader/>
        <div class="body_container">
    
          <ACTDashboardOLDLeftSideBar/>
          <div class="main_container">
            <div class="page_container">
                <ACTGSAPScrollSmoother>
              <section class="dashboard_inner_section">
                <div class="inner_background">
                    <ACTDashboardOLDTopPageNavigationBar/>
                  <div class="main_content_container">
                   <ACTDashboardOLDInfoCards/>
                    <ACTDashboardOLDDataTable/>
                  </div>
                </div>
                <ACTDashboardOLDUncoverFooterAnimation/>
              </section>
            </ACTGSAPScrollSmoother>
            </div>
            <ACTDashboardOLDDashBoardFooter/>
          </div>
        </div>
    </div>
    </div>
    
    
    
    
    </template>
    
    
    
    
    <script setup>
    
    
    import { onBeforeMount, ref } from 'vue';
    
    let active_el =  ref(0)
    
    
    
    function hover_listener(el){
        active_el.value = el
    }
    
    
    
    
    </script>
    
    
    
    <style scoped>
    
    
    
    
      /*          MAIN TEMPATE CSS         */
      /*          MAIN TEMPATE CSS         */
      /*          MAIN TEMPATE CSS         */
      /*          MAIN TEMPATE CSS         */
      /*          MAIN TEMPATE CSS         */
      /*          MAIN TEMPATE CSS         */
      /*          MAIN TEMPATE CSS         */
    
    
    
    /* root and dark are the same -- root is just the default */
  


    .dashboard_body{
        background-size: cover;
    background-position: center;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 100%;
    height: 100%;
    position:fixed;
    font-family: Haffer, sans-serif!important;
    scroll-behavior: smooth;
    margin: 0;
    padding: 0;
    background-color:#fff
    }
    
    
    
    
    
    
    
    .dashboard {
    background-color: #fff;
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    width: 100%;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    font-size: 15px;
    }
    
    
    
    
    
    
    .dashboard_inner_section{
    margin-bottom: 450px; 
    width:100%; 
    border-bottom: rgba(75, 75, 75, 0.1) .5px solid;
    background-color: var(--inner_background);
    }
    
    /* .inner_background {
      background-color: rgba(183, 217, 255, 0.088);
      width: 100%;
      z-index: 10;
      -webkit-backdrop-filter: blur(30px);
      backdrop-filter: blur(30px);
    } */
    
    
    .main_content_container{
    width:85%; 
    padding-right:5%;
    margin-left: 300px;
    }
    
    
    
    
    
    
    .main_container {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    }
    
    
    
    
    
    
    .page_container {
    display: flex;
    flex-direction: column;
    color: var(--theme-color);
    height: 100%;
    overflow: auto;
    background-color:transparent;
    width:100%;
    margin:0; 
    }
    
    
    .page_container .overlay {
    pointer-events: none;
    transition: 0.3s;
    background-color: var(--overlay-bg);
    }
    
    
    </style>
    