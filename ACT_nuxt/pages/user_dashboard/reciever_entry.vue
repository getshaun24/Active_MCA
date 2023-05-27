<template>


<UserDashSettlementDoneSlider :reciever_entry_done="reciever_entry_done" :receiver_name="receiver_name" :settlement_ID="settlement_ID" :lowest_value="lowest_value" :acceptable_value="acceptable_value" :ideal_value="ideal_value"/>
  <Teleport to="body">
  <div class="modal_container" :class="{modal_hide_anim: modal_exit_anim, modal_hide_disp: modal_exit_display}">
          <div class="modal_popup" :class="{modal_bix_hide_anim: modal_exit_anim}" ref="modal">
              <div @click="modal_leave" class="modal_exit">
              <div class="horizontal_line"></div>
              <div class="vertical_line"></div>
          </div>
  
          <div class="modal_info">
              <h6 class="modal_text">Settlement Request Successful</h6>
  
          </div>
  
          </div>
      </div>
  
      <div class="plaid_blur" v-if="plaid_blur"></div>
      <div class="loader_container" v-if="start_loader"></div>
  
  </Teleport>
  
  






  <ACTMainHeader/>
      <ACTGSAPScrollSmoother>
        <div style="background-color: #fff; padding-bottom:10%; border-bottom: 1px solid rgb(167, 211, 232, 0.4); padding-top:10%">



<!-- -------------------------------------------------------------------------- -->
<!-- -------------------------------------------------------------------------- -->

    <div ref="designation_box" class="designation_box" :class="{designation_show: designation_show}" @mouseleave="designation_show = false">
    <p class="designation_text desig_underline">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. </p> 
    <p class="designation_text"><span style="font-size:10px; color:#deae008c">○</span> Dignissim diam quis enim lobortis scelerisque. Dignissim cras tincidunt lobortis feugiat vivamus. Semper feugiat nibh sed pulvinar proin gravida hendrerit. Nulla facilisi cras fermentum odio eu feugiat pretium nibh. </p>
    <p class="designation_text">Quis imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper.</p> 
    <br>
    <p class="designation_text"><span style="font-size:10px; color:#deae008c">○</span>  Aliquet bibendum enim facilisis gravida neque convallis a. Id ornare arcu odio ut sem nulla pharetra diam sit. Consectetur adipiscing elit duis tristique. Elit ullamcorper dignissim cras tincidunt lobortis feugiat vivamus at augue. Odio eu feugiat pretium nibh ipsum consequat nisl. Magna fringilla urna porttitor rhoncus dolor purus non enim praesent.<br><br> Ut morbi tincidunt augue interdum velit euismod in. Lacus suspendisse faucibus interdum posuere lorem ipsum dolor sit amet. At tellus at urna condimentum mattis. Sit amet justo donec enim diam vulputate. 
</p>
<div class="paperOverlay"></div>
</div>

<!-- -------------------------------------------------------------------------- -->
<!-- -------------------------------------------------------------------------- -->




          <div class="request_grid">
  
  <div class="upper_block">

      <h6 class="page_title">New Settlement Request</h6>


    <div class="info_container">

    <div class="info_left">
    <p class="info_text_intro">Hello, {{  receiver_name  }}, welcome to
        <i>Can We Settle.</i></p>
    <p class="intro_subtext">ACT makes settling simple, fast, and fair.
        <br> Learn more about how it works <span class="designation_hover" @click="designation_show = true" @mouseover="designation_show = true">?</span>
    </p>


    <br>

    <p class="info_text"><span class="underline_it">New Request From:</span> {{  initiator_name  }}</p>
    <p class="info_text"><span class="underline_it">Firm:</span> {{  initiator_firm_name  }}</p>
    <p class="info_text"><span class="underline_it">Email:</span> {{  initiator_email  }}</p>
    <p class="info_text"><span class="underline_it">Phone:</span> {{  initiator_phone  }}</p>
    <br>
  </div>

  <div class="info_right">
    <p class="info_text_id"><span style="color:#fff">ACT Settlement ID: {{  settlement_ID  }}</span></p>
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

  





  <div class="lower_block">

      <div class="form_move">

          <div class="form_box">
      <div>
      <p class="form_text">Ideal Amount</p>
      <p class="form_subtext">This is the amount you would like to receive</p>
      </div>
      <div class="input_wrap input_wrap_edit_2">
          <input @keyup="update_ideal_val" v-model="ideal_value" type="text" class="input_white input_edit_2" placeholder=' ' required/>
          <label class="label_white label_move_2" >Ideal Amount</label>
        </div>
      </div>


        <div class="form_box">
          <div>
      <p class="form_text">Acceptable Amount</p>
      <p class="form_subtext">This is the meadian value of what you settle for</p>
      </div>
        <div class="input_wrap input_wrap_edit_2">
          <input @keyup="update_acceptable_val" v-model="acceptable_value" type="text" class="input_white input_edit_2" placeholder=' ' required/>
          <label class="label_white label_move_2" >Acceptable Amount</label>
        </div>
      </div>


        <div class="form_box">
          <div>
      <p class="form_text">Lowest Amount</p>
      <p class="form_subtext">This is the absolute lowest terms you would accept</p>
      </div>
        <div class="input_wrap input_wrap_edit_2">
          <input @keyup="update_lowest_val" v-model="lowest_value" type="text" class="input_white input_edit_2" placeholder=' ' required/>
          <label class="label_white label_move_2" >Lowest Amount</label>
        </div>
      </div>


      <div @click="send_new_request" class="submit_button">Send Request</div>


      </div>
</div>


</div>








          <div style="padding-bottom:30vh"></div>        
        </div>
          <ACTFooterMain/>  
  <div class="paperOverlay"></div>
  </ACTGSAPScrollSmoother>
  




  
    
  
  
  
  
  </template>
  
  
  
  
  
  <script setup>
  import { useFileDialog } from '@vueuse/core'
  const config = useRuntimeConfig()
  
  const route = useRoute().query
  console.log(route.receiver_name)
  console.log(route.settlement_ID)
  const cookie_options = {default:()=> '', watch:true}
  const receiver_name =  useCookie('receiver_name', cookie_options)
  const settlement_ID =  useCookie('settlement_ID', cookie_options)
  receiver_name.value = route.receiver_name
  settlement_ID.value = route.settlement_ID


  const initiator_name = ref('')
  const initiator_email = ref('')
  const initiator_phone = ref('')
  const initiator_firm_name = ref('')
  const request_date = ref('')
  const case_number = ref('')
  const filing_state = ref('')
  const brief_description = ref('')
  const additional_info = ref('')


  // const reciever_entry_done = useCookie('reciever_entry_done', cookie_options)
  const reciever_entry_done = ref(false)

// --------------------------------------------------------------------------
// Gset Settlement Info

  fetch(`${config.flask_url}/api/user_dashboard/receiver_entry/`, {
   method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    body: JSON.stringify({settlement_ID: settlement_ID.value})
}).then((response) => response.json())
    .then((data) => {
    
      initiator_name.value = data.initiator_name
         initiator_email.value = data.initiator_email
          initiator_phone.value = data.initiator_phone
         initiator_firm_name.value = data.initiator_firm_name
         request_date.value = data.request_date
         case_number.value = data.case_number
         filing_state.value = data.filing_state
         brief_description.value = data.brief_description
         additional_info.value = data.additional_info



    })
    .catch(error => {
        console.error('Error');
    });




  // --------------------------------------------------------------------------
  // --------------------------------------------------------------------------


  const designation_show = ref(false)
const designation_box = ref(null)

watch(designation_show, (new_desig) => {
        if (new_desig == true) {
            sleep(1000).then(() => {
            onClickOutside(designation_box, (event) => designation_show.value = false) 
    })
}
})




  const email = ref('')
  const ideal_value = ref('')
  const acceptable_value = ref('')
  const lowest_value = ref('')
  
  
  
  function update_ideal_val(){
      ideal_value.value  = '$' + ideal_value.value.toString().replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
  
  function update_acceptable_val(){
      acceptable_value.value  = '$' + acceptable_value.value.toString().replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
  
  function update_lowest_val(){
      lowest_value.value  = '$' + lowest_value.value.toString().replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }
  
  
  
  function send_new_request(){
  
  
    reciever_entry_done.value = 'true'

  // fetch(`${config.flask_url}/api/user_dashboard/new_request/`, {
  //     method: 'POST',
  //     headers: {
  //         'Accept': 'application/json',
  //         'Content-Type': 'application/json'
  //     },
  //     body: JSON.stringify({email: email.value, ideal_value: ideal_value.value, acceptable_value: acceptable_value.value, lowest_value: lowest_value.value})
  // })
  // .then((response) => response.json())
  // .then((data) => {
  
  
  
  // if (data.status == 'recipient_requested'){
  //     open_modal(),
  //     email.value = '',
  //     ideal_value.value = '',
  //     acceptable_value.value = '',
  //     lowest_value.value = ''
  // }
  
  
  // })
  // .catch(error => {
  //     alert('Error')
  // });



  }
  
  
  
  
  
  
  
  
  
  // ------------------------------- Modal  ---------------
  // ------------------------------- Modal  ---------------
  // ------------------------------- Modal  ---------------
  
  
  const modal_exit_anim = ref(true)
  const modal_exit_display = ref(true)
  
      
      
      // sleep time expects milliseconds
      function sleep (time) {
        return new Promise((resolve) => setTimeout(resolve, time));
      }
      
  function open_modal(){
      modal_exit_display.value = false
          sleep(100).then(() => {
          modal_exit_anim.value = false
          });
  }
  
  function modal_leave(){
          modal_exit_anim.value = true
          sleep(1100).then(() => {
          modal_exit_display.value = true
          start_loader.value = false;
          plaid_blur.value = false;
          });
      }
  
  
  
  </script>
  
  
  
  <style scoped>
  
  
  .request_grid{
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: repeat(2, 1fr);
  grid-column-gap: 0px;
  grid-row-gap: 20px;
  width:80%;
  margin-top:5%;
  margin-left:10%
  }
  
  
  .upper_block{
      height:500px;
      border-radius: 30px;
      background-color:rgb(6, 100, 162);
      border: #a7d3e8 1px solid;
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

  .info_text_case_num{
    color:#fff;
    font-size:18px;
    margin-top:10px
  }

  .form_move{
      margin-top:-10px
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

  .case_info_section_title{
    color:#fff;
      margin-left:4%;
      margin-top:40px;
      font-size:250%;
      margin-bottom:20px;
      text-decoration: underline;
      text-decoration-color:rgb(1, 84, 140);
      text-decoration-thickness: 3px;
      text-underline-offset: 3px;
  }
  
  .underline_it{
    text-decoration: underline;
      text-decoration-color:#deae00b9;
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
  }
  
  .input_wrap_edit_2{
      width:100%;
      margin:0%;
      margin-top:7px;
  
  }
  
  .label_move_2{
      color:rgba(6, 100, 162, 0.566);
      margin-top:3px;
      margin-left:1px
  }
  
  .input_edit_2{
      border-bottom: 1px solid rgb(6, 100, 162);
      color:rgb(6, 100, 162)
  }
  
  .form_text{
      color:rgb(5, 77, 124);
      margin:0%;
      font-size:200%
  }
  .form_subtext{
      font-size:80%;
      margin:0;
      color:#deae00b9;
  }
  .form_box{
      display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: 1fr;
  grid-column-gap: 0px;
  grid-row-gap: 0px;
  width:90%;
  margin-left:5%;
  margin-top:80px
      }
  
  
  
      .submit_button{
      width:50%;
      height:40px;
      background-color:rgb(6, 100, 162) ;
      margin-left: 25%;
      margin-top:75px;
      border-radius:100px;
      border:#fff solid 0px;
      cursor:pointer;
      font-size:25px;
      line-height:40px;
      color:#fff;
      box-shadow: 0px 5px 12px rgba(0, 0, 0, 0.2);
      outline: 0px solid rgba(19, 218, 218, 0.6);
      transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
      text-align: center;
  }
  
  
  .submit_button:hover{
    box-shadow: 0px 10px 15px rgb(25, 120, 237, .5);
    transform: translateY(-3px);
    outline: 3px solid rgba(19, 218, 218, 0.6);
    transition: outline 12s ease 1s;
  } 
  
  
  









.designation_box{
    width:75%;
    margin-left:7.5%;
    margin-top:30%;
    opacity:0;
    position:absolute;
    background-color:#fff;
    z-index:5;
    padding:5%;
    border-radius:10px;
    border: 4px solid rgba(25, 120, 237, 0.7);
    display: inline-block;
    transition: all .35s ease-in-out;
    visibility: hidden;
}

.designation_text{
    color:rgb(6, 100, 162);
    font-size:110% 
}
.desig_underline{
    border-bottom: 2px solid #deae008c;
    padding-bottom:10px;
    text-align:center;
    margin-top:-3%;
    width:80%;
    margin-left:10%;
    margin-bottom:5%
}

.designation_show{
    margin-top:10%;
    opacity:1;
    visibility: visible;
    transition: all .35s ease-in-out;
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



  
  /* 
  // ------------------------------- Modal  ---------------
  // ------------------------------- Modal  ---------------
  // ------------------------------- Modal  --------------- 
  */
  
  
  
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
          background-color:rgba(0, 0, 0, 0.5);
          position:fixed;
          top:0;
          left:0;
          z-index:200;
          display:flex;
          justify-content:center;
          align-items:center;
          backdrop-filter: blur(10px);
          transition: all 1s ease-in-out;
          opacity: 1;
      
      }
      .modal_popup{
          width:600px;
          height:425px;
          background-color:rgb(6, 100, 162);
          z-index:210;
          border-radius:20px;
          margin-top:0px;
          border: #fff solid 2px;
          transition: all 1s ease-in-out;
          overflow-y: scroll;
          overflow-x:hidden
      }
  
      .modal_popup::-webkit-scrollbar {
    width: 5px !important;
    border-radius: 10px !important;
  }
  
  .modal_popup::-webkit-scrollbar-thumb {
    background: rgba(0, 149, 255, 1) !important;
    border-radius: 10px !important;
  }
  
      
      .modal_info{
          font-size:30px;
          font-weight:600;
          color:#fff;
          margin-left:10%;
          margin-top:10%;
          width:80%;
          text-align:center
      }
      
      .modual_buttons{
          width:40%;
          height:35px;
          background-color:rgb(25, 120, 237) ;
          margin-left: 30%;
          margin-top:3.5%;
          border-radius:100px;
          border:#fff solid 0px;
          cursor:pointer;
          font-size:12px;
          color:#fff;
            box-shadow: 0px 7px 10px rgb(25, 120, 237, .3);
        transition: outline 12s ease 1s;
      }
      
      .modual_buttons:hover{
        box-shadow: 0px 10px 15px rgb(25, 120, 237, .5);
        transform: translateY(-3px);
        outline: 3px solid rgba(19, 218, 218, 0.6);
        transition: outline 12s ease 1s;
      } 
  
      .select_button{
          width:40%;
          height:35px;
          background-color:rgb(25, 120, 237) ;
          margin-left: 30%;
          margin-top:5%;
          margin-bottom:20%;
          border-radius:100px;
          border:#fff solid 0px;
          cursor:pointer;
          font-size:12px;
          color:#fff;
            box-shadow: 0px 7px 10px rgb(25, 120, 237, .3);
        transition: outline 12s ease 1s;
      }
  
      .select_button:hover{
        box-shadow: 0px 10px 15px rgb(25, 120, 237, .5);
        transform: translateY(-3px);
        outline: 3px solid rgba(19, 218, 218, 0.6);
        transition: outline 12s ease 1s;
      } 
  
      .back_arrow{
          font-size:50px;
          color:#fff;
          position:relative;
          top:-60px;
          left:20px;
          margin-bottom:-7%;
          cursor: pointer;
      }
      
      
      .modal_exit{
          margin-top:0px;
          margin-left:540px;
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
      
  
      .modal_text{
          font-size:140%;
          color:#fff;
          margin-left:5%;
          margin-top:20%;
          width:90%;
          text-align:center;
          line-height:1.3
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
  
  
  
  </style>