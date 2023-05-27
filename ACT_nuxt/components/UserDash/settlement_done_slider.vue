<template>
    

    <Teleport to="body">
<div class="modal_container" :class="{modal_hide_anim: modal_exit_anim, modal_hide_disp: modal_exit_display}">
        <div class="modal_popup" :class="{modal_box_hide_anim: modal_exit_anim_container}" ref="modal">
            <!-- <div @click="modal_leave" class="modal_exit">
            <div class="horizontal_line"></div>
            <div class="vertical_line"></div>
        </div> -->

        <div class="modal_info">
            <h6 class="modal_text"><img src="~/assets/content/homepage/home_1.png" loading="lazy" alt="" class="menu_logo" />
                <br>Settlement Consensus Reached</h6>

                <p class="signup_text">In order to see the results please signup now</p>

            <div class="form_grid">


                <div class="input_wrap input_wrap_edit_1">
            <input v-model="email" type="text" class="input_white input_edit_1" placeholder=' ' required/>
            <label class="label_white label_move_1" >Email</label>
          </div>

          <div class="input_wrap input_wrap_edit_1">
            <input v-model="password_1" type="password" class="input_white input_edit_1" placeholder=' ' required/>
            <label class="label_white label_move_1" >Password</label>
          </div>

          <div class="input_wrap input_wrap_edit_1">
            <input v-model="password_2" type="password" class="input_white input_edit_1" placeholder=' ' required/>
            <label class="label_white label_move_1" >Verify Password</label>
          </div>


            <div class="input_wrap input_wrap_edit_1">
            <input v-model="first_name" type="text" class="input_white input_edit_1" placeholder=' ' required/>
            <label class="label_white label_move_1" >First Name</label>
          </div>

            <div class="input_wrap input_wrap_edit_1">
            <input v-model="last_name" type="text" class="input_white input_edit_1" placeholder=' ' required/>
            <label class="label_white label_move_1" >Last Name</label>
          </div>

          <div class="input_wrap input_wrap_edit_1">
            <input v-model="company_name" type="text" class="input_white input_edit_1" placeholder=' ' required/>
            <label class="label_white label_move_1" >Company Name<span style="font-size:9px"> (Optional)</span></label>
          </div>


          <div class="input_wrap input_wrap_edit_1">
            <input v-model="job_title" type="text" class="input_white input_edit_1" placeholder=' ' required/>
            <label class="label_white label_move_1" >Job Title<span style="font-size:9px"> (Optional)</span></label>
          </div>


          <div class="input_wrap input_wrap_edit_1">
            <input @keyup="remove_chrs_phone" @keypress="onPhoneKeyPress" maxlength="12" v-model="phone_number" type="text" class="input_white input_edit_1" placeholder=' ' required/>
            <label class="label_white label_move_1" >Phone Number<span style="font-size:9px"> (Optional)</span></label>
          </div>

          <div class="input_wrap input_wrap_edit_1">
            <input @keyup="remove_chrs_num_open" v-model="number_of_open" type="text" class="input_white input_edit_1" placeholder=' ' required/>
            <label class="label_white label_move_long" >Current Number of Open Settlements on Your Desk Right Now <span style="font-size:9px"> (Optional)</span></label>
          </div>



        </div>

        <div @click="send_more_signup_info" class="submit_button">Submit</div>

        </div>
      <div style="padding-bottom:8vw"></div>
      <div class="modal_paper"></div>
        </div>
</div>


</Teleport>




</template>


<script setup>

const props = defineProps(['reciever_entry_done', 'receiver_name', 'settlement_ID', 'lowest_value', 'acceptable_value', 'ideal_value'])

const config = useRuntimeConfig()
const cookie_options = {default:()=> '', watch:true, maxAge:1800}
const user_ID = useCookie('user_ID', cookie_options)
const email = ref('')
const password_1 = ref('')
const password_2 = ref('')
const first_name = useCookie('first_name', cookie_options)
const last_name = ref('')
const company_name = ref('')
const job_title = ref('')
const phone_number = ref('')
const number_of_open = ref('')





function send_more_signup_info(){

    if (password_1.value != password_2.value || password_1.value == '' || password_2.value == '') {
        alert("Passwords do not match. Please try again.")
        password_1.value = ''
        password_2.value = ''
    } else if (password_1.value.length < 6) {
        alert("Your password is too short. Minimum length is 8 characters")
    } else {


  fetch(`${config.flask_url}/api/login/sign_up/`, {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({extra_info_included:'true', receiver_name:props.receiver_name, settlement_ID:props.settlement_ID, email:email.value, password:password_1.value, first_name: first_name.value, last_name: last_name.value, company_name: company_name.value, job_title: job_title.value, phone_number: phone_number.value, number_of_open: number_of_open.value, lowest_value: props.lowest_value, acceptable_value: props.acceptable_value, ideal_value: props.ideal_value})
  })
  .then((response) => response.json())
  .then((data) => {
  
    user_ID.value = data.user_ID
  if (data.status == 'created_user_success'){
    navigateTo('/user_dashboard/dashboard_home')
  } else{
    alert('Error Creating User')
  }
  
  
  })
  .catch(error => {
      alert('Error')
  });
}
  }
  
  



  function remove_chrs_phone() {
    phone_number.value = phone_number.value.toString().replace(/[^0-9-()-+ ]/g, '');
}

function remove_chrs_num_open() {
    number_of_open.value = number_of_open.value.toString().replace(/[^0-9-()-+ ]/g, '');
}


function onPhoneKeyPress(e) {
    const key = e.keyCode || e.charCode;
    const len_phone = phone_number.value.length

    if (key !== 8 || key !==  46) {
    if(len_phone == 3 || len_phone == 7){
        phone_number.value = phone_number.value + '-'
        }
    }
}




// ------------------------------- Modal  ---------------
// ------------------------------- Modal  ---------------
// ------------------------------- Modal  ---------------


const modal_exit_anim = ref(true)
const modal_exit_display = ref(true)
const modal_exit_anim_container = ref(true)
    
const more_info = useCookie('more_info')



watch(()=>props.reciever_entry_done, (newVal) => {


modal_exit_display.value = false
    sleep(100).then(() => {
    modal_exit_anim.value = false
    sleep(800).then(() => {modal_exit_anim_container.value = false})});



     })

    



    
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
        modal_exit_anim_container.value = true
        sleep(400).then(() => {
        modal_exit_anim.value = false
        });
        sleep(1100).then(() => {
        modal_exit_display.value = true
        });
    }




</script>



<style scoped>

.menu_logo{
    width: 120px;
}

.form_grid{
    display: grid;
grid-template-columns: repeat(2, 1fr);
grid-template-rows: repeat(3, 1fr);
grid-column-gap: 20px;
grid-row-gap: 40px;
}

.signup_text{
    font-size: 20px;
    color: rgb(6, 100, 162);
    margin-top: -75px;
    margin-bottom: 75px;
    text-decoration: underline;
      text-decoration-color:#deae00b9;
      text-decoration-thickness: 2px;
      text-underline-offset: 3px;
}

.input_wrap_edit_1{
    width:100%;
    margin:0%;
    margin-top:10px;

}

.label_move_1{
    color:rgba(6, 100, 162, 0.566);
    margin-top:3px;
    margin-left:-15px
}

.label_move_long{
    color:rgba(6, 100, 162, 0.566);
    margin-top:-8px;
    margin-left:-24px;
    width:85%;
    font-size:12.5px
}



.input_edit_1{
    border-bottom: 1px solid rgb(6, 100, 162);
    color:rgb(6, 100, 162)
}


.submit_button{
    width:70%;
    height:40px;
    background-color:rgb(6, 100, 162) ;
    margin-left: 15%;
    margin-top:75px;
    border-radius:100px;
    border:#fff solid 0px;
    cursor:pointer;
    font-size:20px;
    font-weight: 100;
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








/* 
// ------------------------------- Modal  ---------------
// ------------------------------- Modal  ---------------
// ------------------------------- Modal  --------------- 
*/







.modal_hide_anim{
        transition: all 1s ease-in-out !important;
        opacity: 0 !important;
    }
    
    .modal_box_hide_anim{
        transition: all .6s ease-in-out !important;
        transform: translateX(100%) !important;
    }
    
    .modal_hide_disp{
        display:none !important;
    }
    
    
    
    
    
    
    
    .modal_container{
        width:100vw;
        height:100vh;
        background-color:rgba(255, 255, 255, 0.1);
        position:fixed;
        top:0;
        left:0;
        z-index:200;
        display:flex;
        justify-content:right;
        align-items:center;
        backdrop-filter: blur(8px);
        transition: all 1s ease-in-out;
        opacity: 1;
    
    }
    .modal_popup{
        width:75vw;
        height:100vh;
        background-color:#fff;
        z-index:210;
        margin-top:0px;
        border: 1px solid rgb(6, 100, 162);
        transition: all 1s ease-in-out;
        overflow-y: scroll;
        overflow-x:hidden;
        border-top-left-radius:20px;
    border-bottom-left-radius:20px;
    }

    .modal_paper{
        height:100vh;
        width:75vw;
        top:0;
        position: absolute;
        background-size: 50%;
    opacity:.5;
  background-repeat: repeat;
  background-image: url("~/assets/content/paper/paper_overlay_3.jpg");
  mix-blend-mode: multiply;
  z-index:-1;
  border-top-left-radius:20px;
    border-bottom-left-radius:20px;
    border: 1px solid rgb(6, 100, 162);
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
        margin-top:-3%;
        width:80%;
        text-align:center;
        z-index: 10;
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
        color:rgb(6, 100, 162);
        margin-left:5%;
        margin-top:10%;
        width:90%;
        text-align:center;
        line-height:1.3;
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
    .label_move_long{
    margin-top:-25px;
    margin-left:-24px;
    width:90%;
    font-size:12.5px
}

.input_wrap .input_white:focus~ .label_move_long,
.input_wrap .input_white:valid ~ .label_move_long{
    top: -0.5vw;
}


}

@media only screen and (min-width: 992px) and (max-width: 1100px) {

    .label_move_long{
    margin-top:-20px;
    margin-left:-24px;
    width:90%;
    font-size:12.5px
}

.input_wrap .input_white:focus~ .label_move_long,
.input_wrap .input_white:valid ~ .label_move_long{
top: -0.5vw;
}

    
}

@media only screen and (min-width: 1100px) and (max-width: 1200px) {

}

@media only screen and (min-width: 992px) and (max-width: 1200px) {
    .modal_text{
        font-size:120%;
    }

    
}

@media only screen and (min-width: 1200px) and (max-width: 1400px) {
}

@media only screen and (min-width: 1400px) and (max-width: 1600px) {
}

@media only screen and (min-width: 1600px) and (max-width: 5600px) {
}







</style>