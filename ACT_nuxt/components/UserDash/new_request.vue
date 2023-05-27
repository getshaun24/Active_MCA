<template>



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



    
<div class="request_grid">

    <div class="upper_block">

        <h6 class="email_title">Enter Settlement Case Info</h6>

        <div class="form_grid">
        <div class="input_wrap input_wrap_edit">
            <input v-model="receiver_email" type="text" class="input_white input_edit" placeholder=' ' required/>
            <label class="label_white label_move" >Opposing Council Email</label>
          </div>

          <div class="input_wrap input_wrap_edit">
            <input v-model="receiver_name" type="text" class="input_white input_edit" placeholder=' ' required/>
            <label class="label_white label_move" >Opposing Council Full Name</label>
          </div>

          <div class="input_wrap input_wrap_edit">
            <input v-model="case_number" type="text" class="input_white input_edit" placeholder=' ' required/>
            <label class="label_white label_move">Case Number</label>
          </div>

          <div class="input_wrap input_wrap_edit">
            <input v-model="filing_state" type="text" class="input_white input_edit" placeholder=' ' required/>
            <label class="label_white label_move" >Filing State</label>
          </div>

          <div class="input_wrap input_wrap_edit">
            <input v-model="brief_description" type="text" class="input_white input_edit" placeholder=' ' required/>
            <label class="label_white label_move" >Brief Description</label>
          </div>

        <div class="input_wrap input_wrap_edit_button">
            <button class="button_move" type="button" @click="open">Choose file</button>
            <label class="label_white label_move_button">Document Upload <span style="font-size:9px">(Optional)</span></label>
          </div>
        </div>

        <div class="input_wrap input_wrap_edit_additional_info">
            <textarea v-model="additional_info" type="textarea" class="input_white input_edit_additional_info" cols="50" placeholder=' ' required></textarea>
            <label class="label_white label_move_additional_info">Add Additional Relevant Info<span style="font-size:9px"> (Optional)</span></label>
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





</template>





<script setup>
import { useFileDialog } from '@vueuse/core'
const config = useRuntimeConfig()


const { files, open, reset } = useFileDialog()

const user_ID = useCookie('user_ID')
const receiver_email = ref('')
const receiver_name = ref('')
const case_number = ref('')
const filing_state = ref('')
const brief_description = ref('')
const additional_info = ref('')

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


fetch(`${config.flask_url}/api/user_dashboard/new_request/`, {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({user_ID:user_ID.value, receiver_email: receiver_email.value, receiver_name:receiver_name.value, case_number: case_number.value, filing_state: filing_state.value, brief_description: brief_description.value, additional_info: additional_info.value,
        ideal_value: ideal_value.value, acceptable_value: acceptable_value.value, lowest_value: lowest_value.value})
})
.then((response) => response.json())
.then((data) => {



if (data.status == 'recipient_requested'){
    open_modal(),

    // reset all values
    receiver_email.value = '',
    receiver_name.value = '',
    case_number.value = '',
    filing_state.value = '',
    brief_description.value = '',
    additional_info.value = '',
    ideal_value.value = '',
    acceptable_value.value = '',
    lowest_value.value = ''
}


})
.catch(error => {
    alert('Error')
});
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
width:100%;
margin-top:10%;
margin-bottom: 15%;
}


.upper_block{
    height:500px;
    border-radius: 30px;
    background-color:rgb(6, 100, 162);
    border: #a7d3e8 1px solid;
}

.lower_block{
    height:600px;
    border-radius: 30px;
    background-color: #a7d3e861;
    border: #a7d3e8 1px solid;
    margin-top:-50px
}

.form_move{
    margin-top:-10px
}

.form_grid{
    display: grid;
grid-template-columns: repeat(2, 1fr);
grid-template-rows: repeat(3, 1fr);
grid-column-gap: 0px;
grid-row-gap: 0px;
width:90%;
margin-left:3%;
}
.email_title{
    color:#fff;
    margin-left:4%;
    margin-top:40px;
    font-size:300%;
    margin-bottom:40px
}


.input_wrap_edit{
    margin-top:40px
}

.input_edit{
    border-bottom: 1px solid #fff;
    color:#fff
}

.label_move{
    margin-top:-1px;
    margin-left:-3PX;
    color:#ffffffaf
}

.label_move_button{
    margin-top:-1px;
    margin-left:-5PX;
    color:#ffffffaf
}



.input_wrap_edit .input_edit:focus~ .label_white,
  .input_wrap_edit .input_edit:valid ~ .label_white{
    top: -1.25vw;
    left: 4vw;  
    font-size: 1vw;
    color: #70c1ff;
  }


.input_wrap_edit_2{
    width:100%;
    margin:0%;
    margin-top:7px;

}

.label_move_2{
    color:rgba(6, 100, 162, 0.566);
    margin-top:3px;
    margin-left:-10px
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




.button_move{
    margin-left:70%;
    margin-top:2px;
    border: 1px solid #022181;
    display: inline-block;
    padding: 6px 12px;
    cursor: pointer;
    background-color: #fff;
    font-size:10px;
    border-radius:20px;
    transition: all 0.3s ease-in-out;
}

.button_move:hover{
 background-color:rgb(6, 100, 162);
 border: 1px solid #fff;
 color:#fff
}

.label_move_button{
    margin-top:-1px;
    margin-left:-13%;
    color:#ffffffaf
}

.input_wrap_edit_button{
    margin-top:40px;
    padding-bottom:5px;
    border-bottom: 1px solid #fff;
    width:85%;
    margin-left:10%
}


.input_wrap_edit_additional_info{
    width:100%;
    margin-left:-2%;
    margin-top:30px
}

.input_edit_additional_info{
    color:#fff;
    height:50px;
    border:1px rgb(255, 255, 255, 0) solid;
    border-bottom: 1px solid #fff;
}

.label_move_additional_info{
    margin-top:20px;
    margin-left:5%;
    color:#ffffffaf
}

.input_edit_additional_info:focus~ .label_move_additional_info,
  .input_edit_additional_info:valid ~ .label_move_additional_info{
    top: -3.25vw;
    left: 4vw;  
    font-size: 1vw;
    color: #70c1ff;
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