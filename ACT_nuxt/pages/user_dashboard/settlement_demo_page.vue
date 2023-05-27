<template>
    
    <div class="light_mode" style="overflow-x:hidden">
        <UserDashDashboardHeader v-bind="active_page" />
        <UserDashLeftSidebar v-bind="active_page"/>
        <ACTGSAPScrollSmoother>
            
            <div class="navigation_header">
                <div class="nav_menu_title">Demo Settlement Page</div>
                <!-- <div class="header_menu">
                    <div class="navigation_menu is-active" href="#">xxx</div>
                    <div class="navigation_menu" href="#">xxx</div>
                    <div class="navigation_menu" href="#">xxx</div>
                </div> -->
            </div>
            <div class="dashboard_inner_section" ref="el">
                <div class="main_content_container">
                  <div class="paperOverlay"></div>
  
                  

                  <div class="upper_block">

                    <h6 class="page_title">Settlement Info</h6>


                    <div class="info_container">

                    <div class="info_left">
                    <p class="info_text_intro">This is a settlement between you and xxxx</p>
                    <p class="intro_subtext">Based on our mathcing algorithm, we believe that you have a XX % probability in coming to a mutally beneficial agreement. 
                    </p>


                    <br>

                    <p class="info_text"><span class="underline_it">New Request From:</span> {{  sender_name  }}</p>
                    <p class="info_text"><span class="underline_it">Company:</span> {{  sender_company  }}</p>
                    <p class="info_text"><span class="underline_it">Email:</span> {{  sender_email  }}</p>
                    <br>
                    </div>

                    <div class="info_right">
                    <p class="info_text_id"><span style="color:#fff">ACT Settlement ID: {{  settlement_id  }}</span></p>
                    <p class="info_text"><span class="underline_it">Request Datetime:</span> <span style="font-size: 14px; line-height: 0;"> {{  request_date  }}</span></p>
                    <p class="info_text"><span class="underline_it">Case Number:</span> {{  case_number  }}</p>
                    <p class="info_text"><span class="underline_it">Filing State:</span> {{  filing_state  }}</p>
                    <p class="info_text"><span style="line-height: 0;" class="underline_it">Brief Description:</span> {{  brief_description  }}</p>
                    <p class="info_text"><span class="underline_it">Additional Info:</span></p>
                    <div class="add_info">{{  additional_info  }}</div>

                    <div class="attatched_docs">Attateched Documents</div>
                    </div>


                    </div>

                    </div>




                  <iframe src="https://get.rocket.chat/channel/signup_user_name%2520shaun%2520%252B%252032323%2520%257C%25203?layout=embedded"></iframe>
     







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

  const rocket_chat_auth_token = useCookie('rocket_chat_auth_token')
  const user_ID = useCookie('user_ID')

//   onMounted(() => {

//   document.querySelector('iframe').contentWindow.postMessage({
//   externalCommand: 'go',
//   path: 'https://get.rocket.chat/channel/signup_user_name%2520shaun%2520%252B%252032323%2520%257C%25203?layout=embedded'
// }, '*')
//   })


// //   onMounted(() => {
//     function iframe_load(rocket_auth) {
//     window.onload = function () {
// window.parent.postMessage({
// event: 'login-with-token',
//  loginToken: rocket_auth
// }, 'https://get.rocket.chat/');
//  }
//   }
// // })


// fetch(`${config.flask_url}/api/rocket_chat/rocket_chat_login/`, {
//       method: 'POST',
//       headers: {
//           'Accept': 'application/json',
//           'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({user_ID:user_ID.value})})
//   .then((response) => response.json())
//   .then((data) => {
//     rocket_chat_auth_token.value = data.rocket_chat_auth_token
//     iframe_load(data.rocket_chat_auth_token)
//   })
//   .catch(error => {
//       alert('Error')
//   });
  
  
    
  
        
  const cookie_options = {default:()=> '', watch:true, maxAge:1800}
  
  const notification_count = useCookie('notification_count', cookie_options)

  const active_page = {is_active: "demo"}
  


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
    


    iframe {
  border: 1px solid #f2f9ff;
  border-top:1px solid #fff;
  border-radius:20px;
  width:100%;
    height:70vh;
    margin-bottom:20%
}


iframe::-webkit-scrollbar {
      width: 3px;
      border-radius: 10px;
  }
  
  iframe::-webkit-scrollbar-thumb {
      background: rgba(0, 149, 255, 0.676);
      border-radius: 10px;
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
    
    
    
    



  
  .upper_block{
      height:500px;
      border-radius: 30px;
      background-color:rgb(6, 100, 162);
      border: #a7d3e8 1px solid;
      margin-bottom: 100px;
      margin-top:100px
  }
  
  /* .middle_block{
      height:500px;
      border-radius: 30px;
      background-color:rgba(0, 89, 178, 0.75);
      border: rgb(6, 100, 162) 1px solid;
  } */

  .lower_block{
      height:600px;
      border-radius: 30px;
      background-color: #a7d3e861;
      border: #a7d3e8 1px solid;
      margin-top:-50px
  }


  .info_container{
    width:90%;
    margin-left:5%;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: 1fr;
    grid-column-gap: 50px;
    grid-row-gap: 0px;
  }

  .info_right{
    margin-left:5%;
    margin-top:-70px;
    padding:20px;
    border-radius: 30px;
    border:#a7d3e861 solid 1px;
    height:400px;
  }

  .add_info{
    height:100px;
    overflow: hidden;
    overflow-y: scroll;
    color: #fff;
    font-size: 14px;
    margin-bottom: 20px;
  }

  .add_info::-webkit-scrollbar {
        width: 3px !important;
        border-radius: 10px !important;
    }
    
    .add_info::-webkit-scrollbar-thumb {
        background: rgba(0, 149, 255, 0.8) !important;
        border-radius: 10px !important;
    }
    

.attatched_docs{
    padding:8px;
    border-radius: 30px;
    border:#a7d3e861 solid 1px;
    color:#fff;
    font-size:12px;
    width:160px;
    text-align: center;
    cursor: pointer;
    transition: all 0.5s ease-in-out;
}

.attatched_docs:hover{
    background-color:#a7d3e861;
}

  .info_text_intro{
    color:#fff;
    margin:10px 0px;
    font-size:25px
  }

  .intro_subtext{
    color:#deae00;
    margin:10px 0px;
    font-size:15px
  }
  .info_text{
    color:#fff;
    margin:10px 0px;
    font-size:20px;
  }
  
  .info_text_id{
    color:#deae00;
    font-size:9px;
    margin-bottom:0
  }

  
  .page_title{
      color:#fff;
      margin-left:4%;
      margin-top:40px;
      font-size:250%;
      margin-bottom:20px;
      text-decoration: underline;
      text-decoration-color:#deae00b9;
      text-decoration-thickness: 3px;
      text-underline-offset: 3px;
  }


  
  .underline_it{
    text-decoration: underline;
      text-decoration-color:#deae00b9;
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
  }
  

.designation_hover{
    font-size:10px;
    padding:2px 5px;
    border: 1px solid #ffffff80;
    color: #fff;
    border-radius:100%;
    cursor:pointer;
    transition: all .35s ease-in-out;
}

.designation_hover:hover{
    background-color:#deae00b9;
    color:#fff;
    transition: all .35s ease-in-out;
}

    
    
  </style>
  
  
  
  
  
  
  
  
  
  
  
  