<template>
    

    <Teleport to="body">
    <div class="loader_container" v-if="start_loader">
        <ACTLoadersApiLoader/>
        </div>
    </Teleport>


        <div class="form_container">
          <h6 class="section_title">Business Info</h6>
          <div class="form_grid">

          <div class="input_wrap">
                    <select v-model="business_type"   class="select_black input_theme" required>
                            <option value="" disabled selected hidden></option>
                            <option value="corporation">Corporation</option>
                            <option value="llc">LLC</option>
                            <option value="partnership">Partnership</option>
                    </select>
                        <label class="label_black label_theme">Business Type:</label>
                </div>



          <div class="input_wrap">
                  <input v-model="business_name" class="input_black input_theme" placeholder=' ' required/>
                  <label class="label_black label_theme">Business Name</label>
          </div>

          <div class="input_wrap">
                  <input v-model="business_DBA" class="input_black input_theme" placeholder=' ' required/>
                  <label class="label_black label_theme">Business DBA</label>
          </div>

          <div class="input_wrap">
                  <input v-model="business_email" class="input_black input_theme" placeholder=' ' required/>
                  <label class="label_black label_theme">Business Email</label>
          </div>

          <div class="input_wrap">
                  <input v-model="business_phone" class="input_black input_theme" placeholder=' ' required/>
                  <label class="label_black label_theme">Business Phone</label>
          </div>


          <ACTFormElementsIndustryClassification v-model:industry_classification="industry_classification"/>

          <ACTFormElementsBusinessClassification v-bind="entity_bis_class"  v-model:business_classification="business_classification"/>

          
          <div class="input_wrap">
                  <input @keypress="onEINKeyPress_business_ein" v-model="business_ein" class="input_black input_theme" placeholder=' ' type="text" maxlength="10" required />
                  <label class="label_black label_theme">Business EIN</label>
          </div>

          <div class="input_wrap">
                  <input v-model="business_address" class="input_black input_theme" placeholder=' ' required />
                  <label class="label_black label_theme">Business Address</label>
          </div>


          <div class="input_wrap">
                  <input v-model="business_city" class="input_black input_theme" placeholder=' ' required />
                  <label class="label_black label_theme">Business City</label>
          </div>

          <ACTFormElementsStateCodes v-bind="business_state_codes" v-model:state_value="business_state"/>


          <div class="input_wrap">
            <input @keypress="onKeyPress_business_zip" v-model="business_zip" class="input_black input_theme" placeholder=' '   type="text" maxlength="5" required />
            <label  class="label_black label_theme">Business Zip</label>
         </div>


          <div class="input_wrap">
                  <input v-model="business_website" class="input_black input_theme" placeholder=' ' required />
                  <label class="label_black label_theme">Business Website</label>
          </div>

          <div class="input_wrap">
                  <input v-model="business_description" class="input_black input_theme" placeholder=' ' required />
                  <label class="label_black label_theme">Business Description</label>
          </div>


        </div>
</div>




<div class="form_container">
      <h6 class="section_title">Customer Info</h6>
<div class="form_grid">

  <div class="input_wrap">
            <input v-model="customer_first_name" type="text" class="input_black input_theme" placeholder=' ' required/>
            <label class="label_black label_theme" >Customer First Name</label>
          </div>


          <div class="input_wrap">
            <input v-model="customer_last_name" type="text" class="input_black input_theme" placeholder=' ' required/>
            <label class="label_black label_theme" >Customer Last Name</label>
          </div>

          <div class="input_wrap">
            <input v-model="customer_email" type="text" class="input_black input_theme" placeholder=' ' required/>
            <label class="label_black label_theme" >Customer Email</label>
          </div>

          <div class="input_wrap">
                <input @keypress="onPhoneKeyPress" maxlength="12" v-model="customer_phone" class="input_black input_theme" placeholder=' ' required />
                <label class="label_black label_theme">Customer Phone</label>
         </div>


          <div class="input_wrap">
            <input v-model="customer_address" type="text" class="input_black input_theme" placeholder=' ' required/>
            <label class="label_black label_theme" >Customer Address</label>
          </div>

          <div class="input_wrap">
            <input v-model="customer_city" type="text" class="input_black input_theme" placeholder=' ' required/>
            <label class="label_black label_theme" >Customer City</label>
          </div>


          <ACTFormElementsStateCodes v-bind="customer_state_codes" v-model:state_value="customer_state"/>


          <div class="input_wrap">
            <input @keypress="onKeyPress_customer_zip" v-model="customer_zip" class="input_black input_theme" placeholder=' '   type="text" maxlength="5" required />
            <label  class="label_black label_theme">Customer Zip</label>
         </div>

          <ACTFormElementsCountryCodes v-bind="customer_country_codes" v-model:country_value="customer_country"/>


          </div>
        </div>




<div class="form_container">
  <h6 class="section_title">Controller Info</h6>
  <div class="same_as_button" @click="same_as_customer">Same as Customer</div>
<div class="form_grid">



<div class="input_wrap">
            <input v-model="controller_first_name" class="input_black input_theme" placeholder=' ' required/>
            <label class="label_black label_theme">Controller First Name</label>
     </div>


     <div class="input_wrap">
            <input v-model="controller_last_name" class="input_black input_theme" placeholder=' ' type="text" required/>
            <label class="label_black label_theme">Controller Last Name</label>
    </div>

    <div class="input_wrap">
            <input v-model="controller_title" class="input_black input_theme" placeholder=' ' type="text" required/>
            <label  class="label_black label_theme">Controller Title</label>
    </div>

    <div class="input_wrap">
                <input v-model="controller_dob" class="input_black input_theme input_date" placeholder=' ' type="date" maxlength="10" min="1900-01-01" max="2020-12-31" required />
                <label  class="label_black label_theme">Controller Date of Birth</label>
    </div>

    <div class="input_wrap">
            <input @keypress="onSSNKeyPress_controller" v-model="controller_ssn" class="input_black input_theme" placeholder=' ' type="text" maxlength="11" required />
            <label  class="label_black label_theme">Controller SSN</label>
    </div>


    <div class="input_wrap">
            <input v-model="controller_address" class="input_black input_theme" placeholder=' ' type="text" required/>
            <label  class="label_black label_theme">Controller Address</label>
    </div>

    <div class="input_wrap">
            <input v-model="controller_city" class="input_black input_theme" placeholder=' ' type="text" required/>
            <label  class="label_black label_theme">Controller City</label>
    </div>

    <ACTFormElementsStateCodes v-bind="controller_state_codes" v-model:state_value="controller_state"/>

    <div class="input_wrap">
            <input @keypress="onKeyPress_controller_zip" v-model="controller_zip" class="input_black input_theme" placeholder=' ' type="text"  maxlength="5"  required/>
            <label  class="label_black label_theme">Controller Zip</label>
    </div>

    <ACTFormElementsCountryCodes v-bind="controller_country_codes" v-model:country_value="controller_country"/>


</div>
</div>




<div class="form_container">
  <h6 class="section_title">Owner Info</h6>
  <div class="same_as_button" @click="same_as_controller">Same as Controller</div>
<div class="form_grid">



  <div class="input_wrap">
            <input v-model="owner_first_name" class="input_black input_theme" placeholder=' ' required />
            <label class="label_black label_theme">Owner First Name</label>
     </div>


     <div class="input_wrap">
            <input v-model="owner_last_name" class="input_black input_theme" placeholder=' ' type="text" required />
            <label class="label_black label_theme">Owner Last Name</label>
    </div>

    <div class="input_wrap">
            <input v-model="owner_title" class="input_black input_theme" placeholder=' ' type="text" required />
            <label  class="label_black label_theme">Owner Title</label>
    </div>

    <div class="input_wrap">
                <input v-model="owner_dob" class="input_black input_theme input_date" placeholder=' ' type="date" maxlength="10" min="1900-01-01" max="2020-12-31" required />
                <label  class="label_black label_theme">Controller Date of Birth</label>
    </div>

    <div class="input_wrap">
            <input @keypress="onSSNKeyPress_owner" v-model="owner_ssn" class="input_black input_theme" placeholder=' ' type="text" maxlength="11" required />
            <label  class="label_black label_theme">Owner SSN</label>
    </div>


    <div class="input_wrap">
            <input v-model="owner_address" class="input_black input_theme" placeholder=' ' type="text" required />
            <label  class="label_black label_theme">Owner Address</label>
    </div>

    <div class="input_wrap">
            <input v-model="owner_city" class="input_black input_theme" placeholder=' ' type="text" required />
            <label  class="label_black label_theme">Owner City</label>
    </div>

    <ACTFormElementsStateCodes v-bind="owner_state_codes" v-model:state_value="owner_state"/>


    <div class="input_wrap">
            <input @keypress="onKeyPress_owner_zip" v-model="owner_zip" class="input_black input_theme" placeholder=' '  type="text" maxlength="5" required />
            <label  class="label_black label_theme">Owner Zip</label>
    </div>

    <ACTFormElementsCountryCodes v-bind="owner_country_codes" v-model:country_value="owner_country"/>

</div>
</div>

            <div class="next_button"  @click="submit_validate_and_send">Submit</div>

</template>

<script setup>
    

// sleep time expects milliseconds
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

const config = useRuntimeConfig()
const csrf_cookie = useCookie('csrf_access_token')
const cookie_options = {default:()=> '', watch:true}
const start_loader = ref(false);



// ----------------------------------   format inputs  ----------------------------------


function onPhoneKeyPress(e) {
  sleep(5).then(() => { customer_phone.value = customer_phone.value.toString().replace(/[^0-9-]/g, '') })
    const key = e.keyCode || e.charCode;
    const len_phone = customer_phone.value.length
    if (key !== 8 || key !==  46) {
    if(len_phone == 3 || len_phone == 7){
      customer_phone.value = customer_phone.value + '-'
        }}
}

function onSSNKeyPress_controller(e) {
    sleep(5).then(() => { controller_ssn.value = controller_ssn.value.toString().replace(/[^0-9-]/g, '') })
    const key = e.keyCode || e.charCode;
    const input_len = controller_ssn.value.length
    if (key !== 8 || key !==  46) {
    if(input_len == 3 || input_len == 6){
        controller_ssn.value = controller_ssn.value + '-'
        }}}

        function onSSNKeyPress_owner(e) {
    sleep(5).then(() => { owner_ssn.value = owner_ssn.value.toString().replace(/[^0-9-]/g, '') })
    const key = e.keyCode || e.charCode;
    const input_len = owner_ssn.value.length
    if (key !== 8 || key !==  46) {
    if(input_len == 3 || input_len == 6){
      owner_ssn.value = owner_ssn.value + '-'
        }}}

        function onEINKeyPress_business_ein(e) {
            sleep(5).then(() => { business_ein.value = business_ein.value.toString().replace(/[^0-9-]/g, '') })
    const key = e.keyCode || e.charCode;
    const input_len = business_ein.value.length
    if (key !== 8 || key !==  46) {
        if(input_len == 2){
        business_ein.value = business_ein.value + '-'
        }}}

        function onKeyPress_individual_zip(e) {
            sleep(5).then(() => { individual_zip.value = individual_zip.value.toString().replace(/[^0-9-]/g, '') })
}
function onKeyPress_business_zip(e) {
            sleep(5).then(() => { business_zip.value = business_zip.value.toString().replace(/[^0-9-]/g, '') })
}
    
function onKeyPress_customer_zip(e) {
            sleep(5).then(() => { customer_zip.value = customer_zip.value.toString().replace(/[^0-9-]/g, '') })
}
    
function onKeyPress_controller_zip(e) {
            sleep(5).then(() => { controller_zip.value = controller_zip.value.toString().replace(/[^0-9-]/g, '') })
}
    
function onKeyPress_owner_zip(e) {
            sleep(5).then(() => { owner_zip.value = owner_zip.value.toString().replace(/[^0-9-]/g, '') })
}
// -------------------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------




const business_type =  useCookie('business_type', cookie_options)
const business_name =  useCookie('business_name', cookie_options)
const business_DBA =  useCookie('business_DBA', cookie_options)
const business_ein =  useCookie('business_ein', cookie_options)
const business_email =  useCookie('business_email', cookie_options)
const business_phone =  useCookie('business_phone', cookie_options)
const industry_classification =  useCookie('industry_classification', cookie_options)
const business_classification =  useCookie('business_classification', cookie_options)
const business_address =  useCookie('business_address', cookie_options)
const business_city =  useCookie('business_city', cookie_options)
const business_state =  useCookie('business_state', cookie_options)
const business_zip =  useCookie('business_zip', cookie_options)
const business_website =  useCookie('business_website', cookie_options)
const business_description =  useCookie('business_description', cookie_options)


const customer_first_name = useCookie('customer_first_name', cookie_options)
const customer_last_name = useCookie('customer_last_name', cookie_options)
const customer_email =  useCookie('customer_email', cookie_options)
const customer_phone =  useCookie('customer_phone', cookie_options)
const customer_address = useCookie('customer_address', cookie_options)
const customer_state =  useCookie('customer_state', cookie_options)
const customer_city =  useCookie('customer_city', cookie_options)
const customer_zip =  useCookie('customer_zip', cookie_options)
const customer_country =  useCookie('customer_country', cookie_options)



const controller_first_name = useCookie('controller_first_name', cookie_options)
const controller_last_name = useCookie('controller_last_name', cookie_options)
const controller_title =  useCookie('controller_title', cookie_options)
const controller_dob =  useCookie('controller_dob', cookie_options)
const controller_ssn =  useCookie('controller_ssn', cookie_options)
const controller_address = useCookie('controller_address', cookie_options)
const controller_state =  useCookie('controller_state', cookie_options)
const controller_city =  useCookie('controller_city', cookie_options)
const controller_zip =  useCookie('controller_zip', cookie_options)
const controller_country =  useCookie('controller_country', cookie_options)

const owner_first_name =  useCookie('owner_first_name', cookie_options)
const owner_last_name =  useCookie('owner_last_name', cookie_options)
const owner_title =  useCookie('owner_title', cookie_options)
const owner_dob =  useCookie('owner_dob', cookie_options)
const owner_ssn =  useCookie('owner_ssn', cookie_options)
const owner_address =  useCookie('owner_address', cookie_options)
const owner_state =  useCookie('owner_state', cookie_options)
const owner_city =  useCookie('owner_city', cookie_options)
const owner_zip =  useCookie('owner_zip', cookie_options)
const owner_country =  useCookie('owner_country', cookie_options)


const business_state_codes = {
    name: 'business_state',
        label: 'Business State',
    }

const customer_state_codes = {
        name: 'customer_state',
        label: 'Customer State',
    }
const customer_country_codes = {
    name: 'customer_country',
        label: 'Customer Country',
    }

    const controller_state_codes = {
        name: 'controller_state',
        label: 'Controller State',
    }
const controller_country_codes = {
    name: 'controller_country',
        label: 'Controller Country',
    }
const owner_state_codes = {
    name: 'owner_state',
        label: 'Owner State',
    }
    const owner_country_codes = {
    name: 'owner_country',
        label: 'Owner Country',
    }



const entity_bis_class = ref({
    industry_class: industry_classification.value
})

watch(industry_classification, (new_industry_classification) => {
        entity_bis_class.value = {industry_class: new_industry_classification}
    })


    const same_as_customer_var = ref(false)
function same_as_customer(){
  same_as_customer_var.value = !same_as_customer_var.value
    if(same_as_customer_var.value == true){
        sleep(200).then(() => {controller_first_name.value = customer_first_name.value })
        sleep(400).then(() => { controller_last_name.value = customer_last_name.value })
        sleep(1200).then(() => {controller_address.value = customer_address.value })
        sleep(1400).then(() => {controller_state.value = customer_state.value })
        sleep(1600).then(() => {controller_city.value = customer_city.value })
        sleep(1800).then(() => {controller_zip.value = customer_zip.value })
        sleep(2200).then(() => {controller_country.value = customer_country.value })
    }
} 




const same_as_controller_var = ref(false)
function same_as_controller(){
  same_as_controller_var.value = !same_as_controller_var.value
    if(same_as_controller_var.value == true){
        sleep(200).then(() => {owner_first_name.value = controller_first_name.value })
        sleep(400).then(() => { owner_last_name.value = controller_last_name.value })
        sleep(600).then(() => {owner_title.value = controller_title.value })
        sleep(800).then(() => {owner_dob.value = controller_dob.value })
        sleep(1000).then(() => {owner_ssn.value = controller_ssn.value })
        sleep(1200).then(() => {owner_address.value = controller_address.value })
        sleep(1400).then(() => {owner_state.value = controller_state.value })
        sleep(1600).then(() => {owner_city.value = controller_city.value })
        sleep(1800).then(() => {owner_zip.value = controller_zip.value })
        sleep(2200).then(() => {owner_country.value = controller_country.value })
    }
} 








// -------------------------------- send data to server --------------------------------
// -------------------------------- send data to server --------------------------------
// -------------------------------- send data to server --------------------------------

function submit_validate_and_send() {
  

  const data_to_send = {
  
    business_type: business_type.value,
    industry_classification: industry_classification.value ,
    business_classification:  business_classification.value,
    business_name:  business_name.value,
    business_DBA:  business_DBA.value,
    business_ein:  business_ein.value,
    business_email:  business_email.value,
    business_phone:  business_phone.value,
    business_address:  business_address.value,
    business_city:  business_city.value,
    business_state:  business_state.value,
    business_zip:  business_zip.value,
    business_website:  business_website.value,
    business_description:  business_description.value,



  customer_first_name: customer_first_name.value,
  customer_last_name: customer_last_name.value,
  customer_address: customer_address.value,
  customer_city: customer_city.value,
  customer_state: customer_state.value,
  customer_zip: customer_zip.value,
  customer_country: customer_country.value,
  customer_email: customer_email.value,
  customer_phone: customer_phone.value,


controller_first_name:  controller_first_name.value,
controller_last_name: controller_last_name.value,
controller_title: controller_title.value ,
controller_dob:  controller_dob.value,
controller_ssn:  controller_ssn.value,
controller_address: controller_address.value ,
controller_state: controller_state.value ,
controller_city: controller_city.value ,
controller_zip: controller_zip.value ,
controller_country: controller_country.value ,
//  controller_email: controller_email.value ,
owner_first_name: owner_first_name.value ,
owner_last_name:  owner_last_name.value,
owner_title: owner_title.value ,
owner_dob: owner_dob.value ,
owner_ssn: owner_ssn.value ,
owner_address: owner_address.value ,
owner_state: owner_state.value ,
owner_city: owner_city.value ,
owner_zip: owner_zip.value ,
owner_country: owner_country.value ,

}


const input_error = ref(false)
// regex to check if password has at least one number and one letter
const regex = /^(?=.*[0-9])(?=.*[a-zA-Z])(?!.*[^ a-zA-Z0-9]).*$/



for (const [key, value] of Object.entries(data_to_send)) {   
  console.log(key, value);
  if (value == ''){
      alert('Please fill out the ___ ' + key + ' ___')
      input_error.value = true
      }
      else if (key == 'business_ein' && value.length != 10){
      alert('Check EIN Number')
      input_error.value = true
      }
      else if (key == 'controller_ssn' && value.length != 11){
      alert('Check Controller SSN Number')
      input_error.value = true
      }
      else if (key == 'owner_ssn' && value.length != 11){
      alert('Check Controller SSN Number')
      input_error.value = true
      }
      else if (key == 'customer_zip' && String(value).length != 5){
      alert('Check Customerr Zip Code')
      input_error.value = true
      }
      else if (key == 'controller_zip' && String(value).length != 5){
      alert('Check Controller Zip Code')
      input_error.value = true
      }
      else if (key == 'owner_zip' && String(value).length != 5){
      alert('Check Owner Zip Code')
      input_error.value = true
      }
      else if (key == 'customer_address'){
          if (!regex.test(value)) {
      alert('Customer address must contain at least one number and letter')
      input_error.value = true
      }}
      else if (key == 'controller_address'){
          if (!regex.test(value)) {
      alert('Controller address must contain at least one number and letter')
      input_error.value = true
      }}
      else if (key == 'owner_address'){
          if (!regex.test(value)) {
      alert('Owner address must contain at least one number and letter')
      input_error.value = true
      }}
      else if( key == 'controller_dob' ){
      if( new Date(Date.parse(value.replace(/-/g, " "))) <= new Date(Date.parse('1900-01-01'.replace(/-/g, " "))) || new Date(Date.parse(value.replace(/-/g, " "))) >= new Date(Date.parse('2005-01-01'.replace(/-/g, " "))) ){
              alert('Please input a Controller valid date of birth that is after 1900 and before 2005')
              input_error.value = true
          }
      }
      else if( key == 'owner_dob' ){
      if( new Date(Date.parse(value.replace(/-/g, " "))) <= new Date(Date.parse('1900-01-01'.replace(/-/g, " "))) || new Date(Date.parse(value.replace(/-/g, " "))) >= new Date(Date.parse('2005-01-01'.replace(/-/g, " "))) ){
          alert('Please input a Owner valid date of birth that is after 1900 and before 2005')
          input_error.value = true
          }
      }
  }

if (input_error.value == false){
  start_loader.value = true;
  fetch(`${config.flask_url}/api/master/funder_sign_up/`, {
    method: 'post',
      mode: 'cors',
      credentials: 'include',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrf_cookie.value
      },
      body: JSON.stringify(data_to_send)
  })
  .then((response) => response.json())
  .then((data) => {
      alert('Success:', data.message);
      start_loader.value = false;
  })
  .catch(error => {
      start_loader.value = false;
      console.error('There was an error!', error);
  });


} else{
  input_error.value = false
  start_loader.value = false;
  console.error('There was an error no send');
}
}




</script>



<style scoped>

.form_container{
    background-color: #121212;
    margin-top:10%;
    border-radius: 20px;
    padding:40px 30px 80px 10px;
  }
.form_grid{
    display: grid;
grid-template-columns: repeat(2, 1fr);
grid-template-rows: repeat(3, 1fr);
grid-column-gap: 10px;
grid-row-gap: 10px;
}

.input_theme{
  color:var(--theme-txt-color);
  background-color:var(--form_background);
}

/* .label_theme{
  color:var(--theme-txt-color);
} */


.section_title{
    color:var(--theme-txt-color);
    font-size: 45px;
    margin-bottom: 10px;
    margin-top: 10px;
    margin-left:5%
}

.same_as_button{
    width:200px;
    padding:10px 20px;
    background-color:var(--form_background);
    color:var(--theme-txt-color);
    border:1px solid var(--theme-txt-color);
    text-align: center;
    border-radius:10px;
    cursor: pointer;
    margin-top:30px;
    margin-bottom:20px;
    margin-left:5%;
    box-shadow: 0px 5px 12px rgba(0, 0, 0, 0.2);
    outline: 0px solid rgba(19, 218, 218, 0.6);
    transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out, background-color .7s ease-in-out;
}

.same_as_button:hover{
  background-color:rgb(25, 120, 237);
  box-shadow: 0px 10px 15px rgb(25, 120, 237, .5);
  transform: translateY(-3px);
  outline: 1px solid rgba(19, 218, 218, 0.6);
  transition: outline 12s ease 1;
} 

.next_button{
    width:50%;
    padding:10px 20px;
    background-color:rgb(25, 120, 237);
    color:#fff;
    text-align: center;
    border-radius:100px;
    cursor: pointer;
    margin-top:5%;
    margin-bottom:10%;
    margin-left:25%;
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



</style>