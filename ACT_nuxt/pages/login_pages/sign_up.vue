<template>
  
    <div>
  
  
  
      
  
      <div class="modal_container" :class="{modal_hide_anim: modal_exit_anim, modal_hide_disp: modal_exit_display}">
        <div class="modal_popup" :class="{modal_bix_hide_anim: modal_exit_anim}" ref="modal">
          <div @click="modal_leave" class="modal_exit">
            <div class="horizontal_line"></div>
            <div class="vertical_line"></div>
          </div>
          
  
          <!--  ----------   Inner Modal   --------------------------  -->
          
          <!--  ----------   TWO FACTOR    --------------------------  -->
          
          <div :class="{ is_hidden:forgot_password}">
            <p class="two_factor_text">Please check your email for your two factor code</p>
            <div class="two_factor_container">
              <div class="input_wrap input_wrap_two_factor">
                <input v-model="two_factor_value" type="text" class="input_white" placeholder=' ' required/>
                <label class="label_white label_move_two_factor" >Two Factor Code</label>
                <label class="label_white label_move_two_factor" :class="{is_hidden:two_factor_message_hidden}">{{two_factor_message}}</label>
  
              </div>          
              <button class="two_factor_submit"  @click="two_factor_api">Submit Two Factor</button>
            </div>
          </div>
          
  
          <!--  ----------   Forgot PW   --------------------------  -->
          
          <div :class="{ is_hidden:!forgot_password}">
            <p class="two_factor_text">Please check your email for your link to create a new password.</p>
  
            <div class="two_factor_container">
              <div class="input_wrap input_wrap_two_factor">
                <input v-model="forgot_password_email_value" type="email" class="input_white" placeholder=' ' required/>
                <label class="label_white label_move_two_factor" >Email</label>
              </div>          
              <button class="two_factor_submit"  @click="forgot_password_submit">Submit Email</button>
            </div>
  
          </div>
        </div>
      </div>
      
      <!--  ----------   Inner Modal   --------------------------  -->
      
      <ACTMainHeader/>
      <ACTGSAPScrollSmoother>
        <div style="background-color: #fff; padding-bottom:10%; border-bottom: 1px solid rgb(167, 211, 232, 0.4); padding-top:10%">
          <h4 class="login_title">Sign Up</h4>      
        <div class="login_container">      
          <div class="form_container"> 
            <div class="label_move" :class="{is_hidden:message_hidden}">
              <p>{{ login_content }}</p>
            </div>
            <div class="input_wrap">
              <input v-model="email" type="text" name="email" class="input_white" placeholder=' ' required/>
              <label class="label_white label_move" >Email</label>
            </div>          
            <div class="input_wrap">
              <input v-model="login_pass_1_value" type="password" class="input_white" placeholder=' ' required/>
              <label class="label_white label_move" >Password</label>
            </div>
            <div class="input_wrap">
              <input v-model="login_pass_2_value" type="password" class="input_white" placeholder=' ' required/>
              <label class="label_white label_move" >Verify Password</label>
            </div>
            <div class="button_container">
              <button class="submit_form" type="submit" @click="user_signup">Login</button>   
              <div @click="forgot_the_ps" class="forgot_password">Forgot Password</div>
            </div>
  
            <!-- 
              <button class="submit_form" type="submit" @click="api_data">Get Restricted Data</button>
              <p class="api_response">Restricted Data: {{ data_content }}</p>
              <button class="submit_form" type="submit" @click="api_logout">Logout</button>
              <p class="api_response">Logout: {{ logout_content }}</p> -->
              
  
            </div>
          </div>
          <div style="padding-bottom:30vh"></div>        
        </div>
          <ACTFooterMain/>  
  <div class="paperOverlay"></div>
  </ACTGSAPScrollSmoother>
  
  
      </div> 
    </template>
    
    
    
    
    
    <script setup>
    
    const cookie_options = {default:()=> '', watch:true}
    const email = useCookie('email', cookie_options)
    const more_info = useCookie('more_info', cookie_options)
    const user_ID = useCookie('user_ID', cookie_options)
    const login_pass_1_value = ref('')
    const login_pass_2_value = ref('')
    const errorMessage = ref('')
    const login_content = ref('') 
    const logout_content = ref(null)
    const data_content = ref(null)
    const two_factor_content = ref(null)
    const forgot_password = ref(false)
  
    const message_hidden = ref(true)
    const config = useRuntimeConfig()
    const modal = ref(null)
    const two_factor_message = ref('')
    const two_factor_message_hidden = ref(true)
  
    
    const modal_exit_anim = ref(true)
    const modal_exit_display = ref(true)
    
    // forgot password email
    const email_value = ref(null)
    const two_factor_value = ref(null)

    // const csrf_cookie = useCookie('csrf_access_token', {default: () => 'nothing'})
    // alert(csrf_cookie.value)
  
    // sleep time expects milliseconds
    function sleep (time) {
      return new Promise((resolve) => setTimeout(resolve, time));
    }
  




    const csrf_cookie = useCookie('csrf_access_token', {default: () => 'nothing'})

    function user_signup() {

        if (login_pass_1_value.value != login_pass_2_value.value || login_pass_1_value.value == '' || login_pass_2_value.value == '') {
        alert("Passwords do not match. Please try again.")
        login_pass_1_value.value = ''
        login_pass_2_value.value = ''
    } else if (login_pass_1_value.value.length < 6) {
        alert("Your password is too short. Minimum length is 8 characters")
    } else {




fetch(`${config.flask_url}/api/login/sign_up/`, {
method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({email: email.value, password: login_pass_1_value.value})
}).then((response) => response.json())
.then((data) => {


    if(data.status == 'email_error'){

        if (data.msg == 'User already exists'){
            // navigateTo('../../login_pages/login')
            alert('User already exists')
        }
    } else {
        const cookie = useCookie('auth_cookie')
        cookie.value = new Date().getTime()+30*60*1000
        more_info.value = true
        user_ID.value = data.user_ID

        navigateTo('/user_dashboard/dashboard_home')

    }
})
.catch(error => {
    console.error('Token Error');
    // navigateTo('/investor_dashboard/investor_expire')
});

}
}
































































// ------ already commented ----------


    // function api_data() {
      //   fetch('http://127.0.0.1:5000/api/v1/who_am_i', {
        //     method: 'GET',
        //     mode: 'cors',
        //     headers: {
          //       'Accept': 'application/json',
          //       'Content-Type': 'application/json',
          //       'X-CSRF-TOKEN': getCookie('csrf_access_token')
          //     }
          //   })
          //   .then(async response => {
            //     const data = await response.json();
            //     if (!response.ok) {
              //       const error = (data && data.message) || response.status
              //       return Promise.reject(error)
              //     }
              //     data_content.value = data.msg
              //   })
              //   .catch(error => {
                //     errorMessage.value = error;
                //     console.error('There was an error!', error);
                //   });
                // }
                
                // function api_login(){ (async () => {
                  //   const rawResponse = await fetch('http://127.0.0.1:5000/api/v1/login', {
                    //     method: 'POST',
                    //     mode: 'cors',
                    //     headers: {
                      //       'Accept': 'application/json',
                      //       'Content-Type': 'application/json'
                      //     },
                      //     body: JSON.stringify({email: email.value, password: login_pass_value.value})
                      //   });
                      //   api_content.value = await rawResponse.json()['access_token'];
                      
                      //   console.log(api_content.value);
                      // })();
                      // }
                      
                      
                      
                      
                      
                      // const { session, refresh, update, reset } = await useSession()
                      
                      
                      
                      
                      
                      
                      
                      // Reactive session object that updates after methods calls below
                      // session.value
                      
                      // Refresh the session
                      // await refresh()
                      
                      // // Update the session with arbitrary data
                      // await update({ shaun: 'thisisshaun' })
                      
                      // // // Get a new session, all data will be lost, the session id and creation time will change
                      // // await reset()
                      
                      
                      // const sesh = session.value
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      function forgot_the_ps() {
                        
                        forgot_password.value = true
                        modal_exit_display.value = false
                        sleep(100).then(() => {
                          modal_exit_anim.value = false
                        });
                        
                        
                      }
                      
                      
                      
                      function open_modal(){
                        modal_exit_display.value = false
                        sleep(100).then(() => {
                          modal_exit_anim.value = false
                        });
                        
                      }
                      
                      
                      
                      
                      function modal_leave(){
                        forgot_password.value = false
                        modal_exit_anim.value = true
                        sleep(1100).then(() => {
                          modal_exit_display.value = true
                        });
                      }
                      
                      
                      
                      
                      // open modal on load
                      
                      
                      
                    </script>
                    
                    
                    
                    <style scoped>
                    
                    
                    .is_hidden{
                      display:none;
                    }
                    
                    
                    .hide_modal{
                      display:none !important
                    }
                    .login_container{
                      width:100%;
                      display:flex;
                      justify-content: center;
                    }
                    
                    .form_container{
                      width:60%;
                      margin-left:10%;
                    }
                    
                    .input_wrap{
                      margin-top:10%;
                      width:80%
                    }
                    
                    .label_move{
                      margin-left:3%
                    }
                    
                    
                    .label_move_two_factor{
                      margin-left:-5%
                    }
                    
                    
                    .two_factor_modal{
                      background-color: rgba(255, 255, 255, 0.349);
                      z-index:10;
                      width:100vw;
                      height:100vh;
                      position:fixed;
                      top:0;
                      backdrop-filter: blur(50px);
                    }
                    
                    .login_title{
                      margin-top:5%;
                      margin-left:5%;
                      margin-bottom:0%
                    }
          
                    .submit_form{
                      background-color:#a7d3e8;
                      border:1px solid #a7d3e8;
                      width:30%;
                      margin-left:12%;
                      padding:10px;
                      border-radius:100px;
                      color:#fff;
                      margin-top:5%;
                      cursor: pointer;
                      transition: all 1s ease;
                    }
                    
                    .submit_form:hover{
                      background-color: #fff;
                      transition: all 1s ease;
                      border:1px solid #a7d3e8;
                      color:#a7d3e8;
                    }
                    
                    .two_factor_container{
                      display: flex;
                      align-items: center;
                      justify-content: center;
                      margin-left:-5%
                      
                    }
                    
                    .api_response{
                      margin-top: 10%;
                    }
                    
                    
                    
                    
                    
                    
                    .two_factor_text{
                      margin-top: 5%;
                      margin-left: 20%;
                      width:60%;
                      text-align:center
                    }
                    
                    
                    .two_factor_submit{
                      background-color:rgb(85, 210, 241);
                      width:30%;
                      margin-left:5%;
                      padding:10px;
                      border:0px;
                      border-radius:100px;
                      color:#fff;
                      margin-top:10%;
                      cursor: pointer;
                      transition: all 1s ease;
                      height:35px
                    }
                    
                    
                    
                    
                    .two_factor_submit:hover{
                      background-color: blue;
                      transition: all 1s ease;
                    }
                    
                    
                    
                    .input_wrap_two_factor{
                      width:50%
                    }
                    
                    
                    
                    .button_container{
                      display:flex;
                      justify-content: space-between;
                      align-items: center;
                      width:70%;
                      margin-top:3%
                    }
                    
                    .forgot_password{
                      color:#fff;
                      cursor: pointer;
                      margin-top:4%
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
                      z-index:10;
                      display:flex;
                      justify-content:center;
                      align-items:center;
                      backdrop-filter: blur(20px);
                      transition: all 1s ease-in-out;
                      
                    }
                    .modal_popup{
                      width:600px;
                      height:375px;
                      background-color:rgb(0, 0, 0);
                      z-index:10;
                      border-radius:20px;
                      margin-top:-100px;
                      border: #fff solid 2px;
                      transition: all 1s ease-in-out;
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
                      color:#fff
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
                      
                      .label_move_two_factor{
                        margin-left:-1%
                      }
                      
                      
                      
                    }
                    
                    @media only screen and (min-width: 576px) and (max-width: 768px) {
                      
                      .label_move_two_factor{
                        margin-left:2%
                      }
                      
                      
                    }
                    
                    @media only screen and (min-width: 768px) and (max-width: 992px) {
                      
                      .label_move_two_factor{
                        margin-left:0%
                      }
                      
                      
                    }
                    
                    @media only screen and (min-width: 992px) and (max-width: 1200px) {
                    }
                    
                    @media only screen and (min-width: 1200px) and (max-width: 1400px) {
                      
                    }
                    
                    @media only screen and (min-width: 1400px) and (max-width: 1600px) {
                      
                      
                      .label_move_two_factor{
                        margin-left:-7%
                      }
                      
                    }
                    
                    @media only screen and (min-width: 1600px) and (max-width: 5600px) {
                      
                      
                      .label_move_two_factor{
                        margin-left:-13%
                      }
                      
                      
                    }
                    
                    
                    
                  </style>