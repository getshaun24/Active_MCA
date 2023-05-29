<template>


    <MainTransition ref="main_tansition"/>
    
    <div class="modal_container" :class="{modal_hide_anim: modal_exit_anim, modal_hide_disp: modal_exit_display}">
        <div class="modal_popup" :class="{modal_bix_hide_anim: modal_exit_anim}" ref="modal">
            <div @click="modal_leave" class="modal_exit">
                <div class="horizontal_line"></div>
                <div class="vertical_line"></div>
            </div>
            <p class="modal_login_info">Please select and account you wish to pay with. </p>
            <ACTButtonsAccountSelectButtons  v-model:account_selected_value="account_selected_value"/> 
            <button @click="account_select_submit" class="next_button">Submit</button>
        </div>
    </div>
    
    
    
    
    
    
        <ACTMainHeader/>
            <ACTGSAPScrollSmoother>
        <div style="background-color: #000; padding-bottom:10%; border-bottom: 1px solid rgb(167, 211, 232, 0.4);">
    
    
    
    
    
    
            <div v-if="institution_ID" class="plaid_box">
                <p class="plaid_text">Welcome, {{ first_name }} {{ last_name }}, we use Plaid to help verify your accredation status and connect your account with our payment processor partner.</p>
       <!-- <button @click="transition_and_route('step_3')" class="continue_button">Continue With Same Bank</button> -->
    <button @click="get_link_token" class="next_button">Connect A New Bank</button>
    <p class="plaid_text_1">By continuing to the next page and inputting your information into Plaid, you permit GET Resources to use your information to verify<br> you are accredited investor status</p>
    </div>
    
    
    
    
    
    
    
    
    
          
            <div v-else class="plaid_box">
       <p class="plaid_text">Welcome, {{ first_name }} {{ last_name }}, we use Plaid to help verify your accredation status and connect your account with our payment processor partner.</p>
    <button @click="get_link_token" class="next_button">Start Plaid Connect</button>
    <p class="plaid_text_1">By continuing to the next page and inputting your information into Plaid, you permit GET Resources to use your information to verify<br> you are accredited investor status</p>
    </div>
    
    
    
    
    
    
    
    
        </div>
        <ACTFooterMain/>
        </ACTGSAPScrollSmoother>
        
        
        </template>
        
        
        
    
    
    <script setup>
    
    
    
    useHead({
        script: [{ src: "https://cdn.plaid.com/link/v2/stable/link-initialize.js", body:true, async: true, preload:true, ssr: false}],
      });
      const cookie_options = {default:()=> '', watch:true, maxAge:1800}
      const start_loader = ref(false);
      const plaid_blur = ref(false);
      const blur_amount = ref('0px');
      const plaid_opacity = ref(0);
      const institution_ID = useCookie('institution_ID', cookie_options)
      const account_list = useCookie('account_list', cookie_options)
      const config = useRuntimeConfig()
      const cicle_tansition = ref('');
      const first_name = useCookie('first_name', cookie_options)
      const last_name = useCookie('last_name', cookie_options)
      const account_selected_value = useCookie('account_selected_value', cookie_options)
      const route = useRoute().query
      const secure_ID =  useCookie('secure_ID', {default:()=> route.secure_id, watch:true, maxAge:1800})
      const db =  useCookie('db', {default:()=> route.db, watch:true, maxAge:1800})
    
      // sleep time expects milliseconds
      function sleep (time) {
      return new Promise((resolve) => setTimeout(resolve, time));
      }
    
    
      const main_tansition = ref(null);
    function transition_and_route(route_to) {
        main_tansition.value.animation_and_route(route_to);
    }
    
    
    
      // ------------------------------- Plaid Fetches ---------------
      // ------------------------------- Plaid Fetches ---------------
      // ------------------------------- Plaid Fetches ---------------
        function get_link_token(){
          // ------- get link token from flask server ---------------
      fetch(`${config.flask_url}/api/plaid_connect/plaid_link_token/`, {
              method: 'POST',
              headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({'secure_ID': secure_ID.value})
          })
          .then((response) => response.json())
          .then((data) => {
              console.log('Success:', data.link_token);
              open_plaid(data.link_token)
          })
          .catch(error => {
              alert('Error')
              console.error('There was an error!', error);
          });
        }
          function open_plaid(link_token){ 
          plaid_blur.value = true;
          sleep(10).then(() => { blur_amount.value = '10px', plaid_opacity.value = 1 });
      const handler = Plaid.create({
      token: link_token,
      onSuccess: (public_token, metadata) => {
          if (metadata['institution']['institution_id'] != institution_ID.value){
              send_plaid_public(public_token, metadata)
          } else {
              alert('You entered the same institution, Please try again with a different institution')
              plaid_blur.value = false;
          }
      },
      onLoad: () => {},
      onExit: (err, metadata) => {
          blur_amount.value = '0px',
          plaid_opacity.value = 0
          plaid_blur.value = false;
      },
      onEvent: (eventName, metadata) => {},
      //required for OAuth; if not using OAuth, set to null or omit:
      //   receivedRedirectUri: window.location.href,
      });
      handler.open();
          }
      // ------------------------------- Plaid Public Token ---------------
      // ------------------------------- Plaid Public Token ---------------
      // ------------------------------- Plaid Public Token ---------------
      function send_plaid_public(public_token, metadata){
          start_loader.value = true;
          fetch(`${config.flask_url}/api/plaid_connect/plaid_public_token/`, {
              method: 'POST',
              headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({'public_token': public_token, 'metadata': metadata, 'secure_ID': secure_ID.value, 'db': db.value})
          })
          .then((response) => response.json())
          .then((data) => {
              console.log('Success:', data.message);
              
              account_list.value = data.data
              institution_ID.value = data.institution_ID
              open_modal()
    
          })
          .catch(error => {
              start_loader.value = false;
              plaid_blur.value = false;
              console.error('There was an error! -- Public Token Error', error);
          });
      }
    
    
        // ------------------------------- Selected Account Submit ---------------
        // ------------------------------- Selected Account Submit ---------------
        // ------------------------------- Selected Account Submit ---------------
    
    
        function account_select_submit(){
          start_loader.value = true;
          fetch(`${config.flask_url}/api/master/account_connect/`, {
              method: 'POST',
              headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ 'secure_ID': secure_ID.value, 'db': db.value, institution_ID: institution_ID.value, account_selected_value: account_selected_value.value})
          })
          .then((response) => response.json())
          .then((data) => {
              console.log('Success:', data.message);
              
             
               transition_and_route('../../funder_dashboard/funder_home/');
          })
          .catch(error => {
              start_loader.value = false;
              plaid_blur.value = false;
              console.error('There was an error! -- Public Token Error', error);
          });
        }
    
    
      // ---------------------------- modal --------------------------------
    
    
    const modal_exit_anim = ref(true)
    const modal_exit_display = ref(true)
    const modal = ref(null)
    
    function modal_leave(){
        modal_exit_anim.value = true
        sleep(1100).then(() => {
        modal_exit_display.value = true
        });
    }
    
    function open_modal(){
        modal_exit_display.value = false
        sleep(100).then(() => {
        modal_exit_anim.value = false
        });
    }
    
    
    
    
      </script>
      
      
      <style scoped>
      .loader_container{
          position:fixed;
          top:0;
          left:0;
          height:100vh;
          width:100vw;
          background-color:rgba(25, 120, 237 , 0.125);
          z-index:100;
          backdrop-filter: blur(20px);
          transition:all 1s ease-in-out;
          display: flex;
          justify-content: center;
          align-items: center;
      }
      .loader {
            border: 50px solid #ffffff;
            border-top: 50px solid #3498db;
            border-radius: 50%;
            width: 240px;
            height: 240px;
            animation: spin 2s linear infinite;
          }
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
          .plaid_box{
              padding-bottom: 25%;
              padding-top:15%
          }
      .next_button{
          width:30%;
          height:40px;
          background-color:rgb(25, 120, 237) ;
          margin-left: 35%;
          margin-top:5%;
          border-radius:100px;
          border:#fff solid 0px;
          cursor:pointer;
          font-size:2vw;
          color:#fff;
          position: relative;
          margin-bottom:7%;
          box-shadow: 0px 5px 12px rgba(0, 0, 0, 0.2);
          outline: 0px solid rgba(19, 218, 218, 0.6);
          transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
      }
      .next_button:hover{
        box-shadow: 0px 10px 15px rgb(25, 120, 237, .5);
        transform: translateY(-3px);
        outline: 3px solid rgba(19, 218, 218, 0.6);
        transition: outline 12s ease 1s;
      } 
      .continue_button{
          width:30%;
          height:40px;
          background-color:rgb(11, 184, 126);
          margin-left: 35%;
          margin-top:5%;
          border-radius:100px;
          border:#fff solid 0px;
          cursor:pointer;
          font-size:2vw;
          color:#fff;
          position: relative;
          margin-bottom:1%;
          box-shadow: 0px 5px 12px rgba(0, 0, 0, 0.2);
          outline: 0px solid rgba(19, 218, 218, 0.6);
          transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
      }
      .continue_button:hover{
          box-shadow: 0px 10px 15px rgb(11, 184, 126, .5);
        transform: translateY(-3px);
        outline: 3px solid rgba(19, 218, 218, 0.6);
        transition: outline 12s ease 1s;
      } 
      .plaid_text{
          color:#fff;
          width:40%;
          margin-left:30%;
          margin-top:10%;
          text-align: center;
          font-size:20px
      }
      .plaid_text_1{
          color:#fff;
          width:40%;
          margin-left:30%;
          margin-top:0%;
          text-align: center;
          font-size:15px
      }
      .white_background{
          background-color: #fff;
          height:100vh;
          width:100vw;
          position:fixed;
          top:0;
          left:0;
          z-index:0;
      }
      .plaid_blur{
          position:fixed;
          top:0;
          left:0;
          height:100vh;
          width:100vw;
          background-color:rgba(25, 120, 237 , 0.08);
          z-index:100;
          backdrop-filter: blur(v-bind(blur_amount));
          transition:all 2s ease-in-out;
          display: flex;
          justify-content: center;
          align-items: center;
          opacity: v-bind(plaid_opacity);
      }
      @media only screen and (min-width: 0px) and (max-width: 380px) {
      .next_button{
          width:50%;
          height:30px;
          margin-top:-55%;
          font-size:3.5vw;
          margin-left: 25%;
      }
      .plaid_text{
          width:80%;
          margin-left:10%;
          margin-top:15%;
      }
      .plaid_text_1{
          width:80%;
          margin-left:10%;
          margin-top:8%;
      }
      }
      @media only screen and (min-width: 380px) and (max-width: 576px) {
      .next_button{
          width:50%;
          height:30px;
          margin-top:15%;
          font-size:3.5vw;
          margin-left: 25%;
      }
      .plaid_text{
          width:80%;
          margin-left:10%;
          margin-top:15%;
      }
      .plaid_text_1{
          width:80%;
          margin-left:10%;
          margin-top:8%;
      }
      }
    
    
    
      /* ---------------------- modal --------------------------------- */
    
    
    .modal_hide_anim{
        transition: all 1s ease-in-out !important;
        opacity: 0 !important;
    }
    .modal_bix_hide_anim{
        transition: all .6s ease-in-out !important;
        transform: scale(0) !important;
    }
    .modal_hide_disp{
        display:none !important;
    }
    .modal_container{
        width:100vw;
        height:100vh;
        background-color:rgba(255, 255, 255, 0.15);
        position:fixed;
        top:0;
        left:0;
        z-index:1;
        display:flex;
        justify-content:center;
        align-items:center;
        backdrop-filter: blur(15px);
        transition: all 1s ease-in-out;
        opacity: 1;
    }
    .modal_popup{
        width:70vw;
        height:70vh;
        background-color:rgb(0, 0, 0);
        z-index:10;
        border-radius:20px;
        border: #fff solid 2px;
        transition: all 1s ease-in-out
    }
    .modal_login_info{
        font-size:30px;
        color:#fff;
        margin-left:25%;
        margin-top:5%;
        margin-bottom:10%;
        width:50%;
        text-align:center
    }
    .login_redirect{
        width:40%;
        height:50px;
        background-color:rgb(25, 120, 237) ;
        margin-left: 30%;
        margin-top:7%;
        border-radius:100px;
        border:#fff solid 0px;
        cursor:pointer;
        font-size:20px;
        color:#fff;
          box-shadow: 0px 7px 10px rgb(25, 120, 237, .3);
      transition: outline 12s ease 1s;
    }
    .login_redirect:hover{
      box-shadow: 0px 10px 15px rgb(25, 120, 237, .5);
      transform: translateY(-3px);
      outline: 3px solid rgba(19, 218, 218, 0.6);
      transition: outline 12s ease 1s;
    } 
    .modal_exit{
        margin-top:10px;
        margin-left:92%;
        cursor:pointer;
        z-index: 10;
        position: relative;
        width:50px;
        height:50px;
    }
    .modal_exit:hover .horizontal_line{
        transform: rotate(180deg);
        transition: all 0.2s ease-in-out;
    }
    .modal_exit:hover .vertical_line{
        transform: rotate(-90deg);
        transition: all 0.5s ease-in-out;
    }
    .horizontal_line{
        height:1px;
        width:30px;
        background-color:rgb(255, 255, 255);
        top:25px;
        left:10px;
        transform: rotate(45deg);
        z-index:1000;
        position: absolute;
    }
    .vertical_line{
        width:1px;
        height:30px;
        top:11px;
        left:25px;
        background-color:#fff;
        transform: rotate(45deg);
        position: absolute;
    }
    @media only screen and (min-width: 0px) and (max-width: 576px) {
        .modal_popup{
        width:350px;
        height:400px;
    }
    .modal_exit{
        margin-top:10px;
        margin-left:290px;
        width:40px;
        height:40px;
    }
    }
    @media only screen and (min-width: 576px) and (max-width: 768px) {
    }
    @media only screen and (min-width: 768px) and (max-width: 992px) {
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