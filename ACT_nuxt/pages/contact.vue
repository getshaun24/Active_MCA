<template>

<div>

    <ACTMainHeader/>

<ACTGSAPScrollSmoother>


<div ref="top_line" class="top_line"></div>

    <div class="contact_img_container">
<img ref="contact_image" class="contact_img" src="~/assets/content/contact/map.jpg">
</div>


<div class="grid_container">

    <div class="col_1">
        <h4 class="content_title">Contact</h4>
    </div>
    <div class="col_2">
        <h6 class="form_title">Talk to Us. We Can Help.</h6>

        <div class="form_input_container">
        <input type="text" class="form_input" name="First Name" placeholder="xxx">
        <input type="text" class="form_input" name="Last Name" placeholder="yyy">
    </div>
    </div>
    <div class="col_3">

        <div class="form_input_container">
        <input type="text" class="form_input" name="First Name" placeholder="aaax">
        <input type="text" class="form_input" name="Last Name" placeholder="ddd">
    </div>

        <div class="left_box_line"></div>

</div>


    <div class="col_4">
        <div class="contact_info">
    <p class="contact_elm">404-513-3348</p>
    <p class="contact_elm">xxx shaun street
Charleston,<br>South Carolina 29403</p>
<p class="contact_elm">shaun@thisisget.com</p>
</div>

    </div>
</div>

<textarea class="form_input_area" placeholder="aaax" name="comment" ></textarea>

<button class="submit_button">Submit</button>






<div class="mobile_grid">

    <h3 class="content_title">Contact</h3>


        <p class="form_title">Talk to Us. We Can Help.</p>

     
    <div class="mobile_form_background">

        <div class="form_input_container">
        <input type="text" class="form_input" name="First Name" placeholder="xxx">
        <input type="text" class="form_input" name="Last Name" placeholder="yyy">
        <input type="text" class="form_input" name="First Name" placeholder="xxx">
        <input type="text" class="form_input" name="Last Name" placeholder="yyy">
        <textarea class="form_input_area" placeholder="aaax" name="comment" ></textarea>

        <button class="submit_button">Submit</button>
    </div>

    <div class="contact_info">
    <p class="contact_elm">404-513-3348</p>
    <p class="contact_elm">xxx shaun street
    Charleston, SC 29403</p>
    <p class="contact_elm">shaun@thisisget.com</p>
    </div>




    </div>


</div>







<div class="scrub_container">
<ACTContactScrubText v-bind="scrub_text_1"/>
</div>



<div ref="map_button" class="map_button"></div>

<div class="body_video">
    <h1 class="contact_message">Settlements Made Easy</h1>

            <div class="paperOverlay"></div>
</div>


<ACTFooterContact/>


</ACTGSAPScrollSmoother>


</div>

</template>


<script setup>


        
        const scrub_text_1 = {text:"Let's Talk", duration:100}







    
      

</script>




<style scoped>



.grid_container{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr 1fr;
    grid-template-areas: 
    "col_1 col_2 col_3 col_4"
    "col_1 col_2 col_3 col_4"
    "col_1 col_2 col_3 col_4"
    "col_1 col_2 col_3 col_4";
    width: 100vw;
    z-index:1;
    position:absolute;
    top:0

}

.col_1{
    grid-area: col_1;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:144vh;
}

.col_2{
    grid-area: col_2;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:120vh;
    border-right:0;
    border-left:0
}

.col_3{
    grid-area: col_3;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    border-left: 0px;
    height:132vh
}

.col_4{
    grid-area: col_4;
    background-color: #18181800;
}

.left_box_line{
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:12vh;
    border-right:rgba(255, 255, 255, 0) solid 1px;
    border-top:rgba(255, 255, 255, 0) solid 1px;
    border-bottom:rgba(255, 255, 255, 0) solid 1px;
    position:absolute;
    bottom:12vh
}

.contact_img_container{
  position: absolute;
 height: 100vh;
 width: 100%;
 object-fit: cover;
 top:0;
 z-index:-2
}
.contact_img{
  position: absolute;
  height: 90vw;
  top:0;
  left:-20%;
  object-fit: cover;
  object-position: center;
  z-index:-1
}

.top_line{
    height:120px;
    border-bottom:rgba(255, 255, 255, 0.15) solid 1px;
    z-index:10
}

.content_title{
    margin-top:12.5%;
    margin-left:2.5%;
    position:absolute;
    font-size:250%
}

.form_title{
    margin-top:22%;
    margin-left:2%;
    position:absolute;
    font-size:170%
}

.form_input{
    border-bottom:#000 solid 1px;
    margin-top:25%;
    color:#fff;
    padding:10px;
    margin-left:8%;
    background-color: #18181800;
    width:75%;
    margin-right: 25px;
}

.form_input_container{
    margin-top:95%;
    position:relative;
}

.form_input_area{
    border-bottom:#000 solid 1px;
    margin-top:27%;
    color:#fff;
    padding:10px;
    margin-left:27%;
    background-color: #18181800;
    width:45%;
    height:75px;
    position:absolute;
    border:none;
    border-bottom:#000 solid 1px;
    z-index:10
}

.submit_button{
    background-color: #fff;
    border:#000 solid 1px;
    margin-top:40%;
    color:rgb(0, 0, 0);
    padding:10px;
    margin-left:27.5%;
    font-size:25px;
    background-color: #18181800;
    width:45%;
    height:60px;
    position:absolute;
    cursor:pointer;
    z-index:10;
    border-radius:100px
}

.submit_button:hover{
    color:#000;
    border: #deae0073 solid 1px;
    background-color:#c4e7ff1e;
    transition: all 0.5s ease;
}

.body_video{
    height:50vh;
    background-color: #fff;
    margin-top:115%;
    z-index:100;
    position:relative;
    width:100%;
    overflow:hidden;

}


.map_button{
    height:80px;
    background-color: rgb(6, 100, 162);
    margin-top:-52%;
    z-index:100;
    position:absolute;
    width:80px;
    margin-left:49%;
    border-radius:100%;
    z-index:-1;
}



.contact_video{
    width:55%;
    margin-left:22.5%;
    margin-top:7.5%
}

.video_overlay{
    width:100%;
    height:100vh;
    margin-top:0%;
    background-color: rgb(0, 0, 0);
    opacity:0.85;
    position:absolute;
    z-index:10;
    top:0;
    left:0
}

.contact_message{
    margin-top:25%;
    font-size:7vw;
    position:absolute;
    color:#000;
    z-index:100;
    text-align: center;
    width:100%
}

.contact_info{
    margin-top:340px;
    width:75%;
    margin-left:15%;
    }



.scrub_container{
    margin-top:20%
}


.contact_elm{
    color:rgb(6, 100, 162)
}









@media only screen and (min-width: 0px) and (max-width: 576px) {

    .grid_container{
        display:none
    }


.contact_img{
  height: 180vw;
  left:-165%;
}

.map_button{
    height:50px;
    width:50px;
    margin-left:50%;
}

.mobile_form_background{
    background-color:#fff;
    height: 80vh;
    min-height: 510px;
    position: absolute;
    top:0;
    width:60%;
    z-index:1
}

.top_line{
    height:70px;
    background-color:#fff;
    z-index:50
}

.scrub_container{
    margin-top:40%;
    z-index:0
}

.content_title{
    margin-top:-25px;
    margin-left:30px;
    font-size:25px;
    position:absolute;
    z-index:10
}

.form_title{
    margin-top:20px;
    margin-left:30px;
    z-index:2;
    font-size:14px
}

.form_input_container{
    margin-top:195px;
    position:relative;
    z-index:2;
}


.form_input{
    margin-top:20px;
    padding:10px;
    margin-left:25px;
    font-size:10px;
    width:70%
}

.form_input_area{
    margin-top:70px;
    margin-left:-85%;
    font-size:10px;
    width:70%;
    height:20px;
}


.submit_button{
    margin-top:150px;
    margin-left:-85%;
    font-size:11px;
    width:40%;
    height:30px;
    border-radius:50px
}

.contact_info{
    margin-top:-190px;
    width:50%;
    margin-left:110%;
    }


.contact_elm{
    font-size:12px;
    color:#fff
}


.body_video{
    height:50vh;

}

.contact_video{
    margin-top:5%
}


.contact_message{
    margin-top:100px;
}



}

@media only screen and (min-width: 576px) and (max-width: 768px) {
  
    .grid_container{
        display:none
    }


.contact_img{
  height: 150vw;
  left:-125%;
}

.map_button{
    height:50px;
    width:50px;
    margin-left:57%;
}

.mobile_form_background{
    background-color:#fff;
    height: 80vh;
    min-height: 530px;
    position: absolute;
    top:0;
    width:60%;
    z-index:1
}

.top_line{
    height:70px;
    background-color:#fff;
    z-index:50
}

.scrub_container{
    margin-top:40%;
    z-index:0
}

.content_title{
    margin-top:-35px;
    margin-left:30px;
    font-size:25px;
    position:absolute;
    z-index:10
}

.form_title{
    margin-top:25px;
    margin-left:30px;
    z-index:2;
    font-size:14px
}

.form_input_container{
    margin-top:215px;
    position:relative;
    z-index:2;
}


.form_input{
    margin-top:20px;
    padding:10px;
    margin-left:30px;
    font-size:10px;
    width:70%
}

.form_input_area{
    margin-top:70px;
    margin-left:-83%;
    font-size:10px;
    width:70%;
    height:20px;
}


.submit_button{
    margin-top:140px;
    margin-left:-83%;
    font-size:11px;
    width:40%;
    height:30px;
    border-radius:50px
}

.contact_info{
    margin-top:-200px;
    width:50%;
    margin-left:110%;
    }


.contact_elm{
    font-size:20px;
    color:#fff
}


.body_video{
    height:50vh;

}

.contact_video{
    margin-top:5%
}


.contact_message{
    margin-top:100px;
}
}




@media only screen and (min-width: 768px) and (max-width: 992px) {

    .mobile_grid{
        display:none
    }

    .top_line{
    height:90px;
    border-bottom:rgba(255, 255, 255, 0.15) solid 1px;
    z-index:10
}

.content_title{
    margin-top:20%;
    margin-left:2.5%;
    position:absolute;
    font-size:250%
}

.form_title{
    margin-top:30%;
    margin-left:15px;
    position:absolute;
}


.form_input_container{
    margin-top:145%;
}

.form_input{
    border-bottom:#000 solid 1px;
    margin-top:40px;
    padding:10px;
    margin-left:10%;
    font-size:15px;
    width:70%
}



.form_input_area{
    margin-top:35%;
    padding:10px;
    margin-left:27%;
    font-size:15px;
    width:42.5%;
    height:50px;
}


.submit_button{
    margin-top:50%;
    padding:10px;
    margin-left:27.5%;
    font-size:15px;
    width:45%;
    height:50px;
}


.contact_img{
  height: 120vw;
  left:-100%;
}


.col_1{
    grid-area: col_1;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:129vh;
}

.col_2{
    grid-area: col_2;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:105vh;
    border-right:0;
    border-left:0
}

.col_3{
    grid-area: col_3;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    border-left: 0px;
    height:117vh
}

.col_4{
    grid-area: col_4;
    background-color: #18181800;
}

.contact_info{
    margin-top:120%;
    margin-left:10%;
    }

    .contact_elm{
    font-size:18px;
    color:#fff
}

.scrub_container{
    margin-top:40%;
    z-index:0
}


.map_button{
    height:80px;
    width:80px;
    margin-left:45%;
}

.contact_video{
    margin-top:5%
}


.contact_message{
    margin-top:15%;
}


.body_video{
    height:50vh;
    margin-top:100%;
}



}

@media only screen and (min-width: 992px) and (max-width: 1200px) {
    .mobile_grid{
        display:none
    }

    .form_input_area{
    margin-top:25%;
    padding:10px;
    margin-left:27%;
    width:42.5%;
    height:75px;
}

.submit_button{
    margin-top:40%;
    padding:10px;
    margin-left:27.5%;
    font-size:25px;
    background-color: #18181800;
    width:45%;
    height:80px;
    background-color: #fff;
}

.scrub_container{
    margin-top:40%;
    z-index:0
}


.contact_img{
  height: 110vw;
  left:-80%;
}

.col_1{
    grid-area: col_1;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:129vh;
}

.col_2{
    grid-area: col_2;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:105vh;
    border-right:0;
    border-left:0
}

.col_3{
    grid-area: col_3;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    border-left: 0px;
    height:117vh
}

.col_4{
    grid-area: col_4;
    background-color: #18181800;
}



}

@media only screen and (min-width: 1200px) and (max-width: 1400px) {
    .mobile_grid{
        display:none
    }


.col_1{
    grid-area: col_1;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:134vh;
}

.col_2{
    grid-area: col_2;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:110vh;
    border-right:0;
    border-left:0
}

.col_3{
    grid-area: col_3;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    border-left: 0px;
    height:122vh
}

.form_input_area{
    margin-top:27%;
    padding:10px;
    margin-left:27%;
    width:42.5%;
    height:75px;
}

.submit_button{
    margin-top:42.5%;
    padding:10px;
    margin-left:27.5%;
    font-size:25px;
    background-color: #18181800;
    width:45%;
    height:80px;
    background-color: #fff;
}


.contact_video{
    width:55%;
    margin-left:22.5%;
    margin-top:0%
}

.contact_message{
    margin-top:15%;
}



}

@media only screen and (min-width: 1400px) and (max-width: 1600px) {
    .mobile_grid{
        display:none
    }

    .col_1{
    grid-area: col_1;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:139vh;
}

.col_2{
    grid-area: col_2;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:115vh;
    border-right:0;
    border-left:0
}

.col_3{
    grid-area: col_3;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    border-left: 0px;
    height:127vh
}

.contact_message{
    margin-top:15%;
}


}

@media only screen and (min-width: 1600px) and (max-width: 5600px) {
    .mobile_grid{
        display:none
    }

    .col_1{
    grid-area: col_1;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:149vh;
}

.col_2{
    grid-area: col_2;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    height:125vh;
    border-right:0;
    border-left:0
}

.col_3{
    grid-area: col_3;
    background-color:#fff;
    border:rgba(0, 0, 0, 0.15) solid 1px;
    border-left: 0px;
    height:137vh
}

.form_input_area{
    margin-top:29.5%;
    padding:10px;
    margin-left:27%;
    width:42.5%;
    height:75px;
}


.contact_video{
    width:45%;
    margin-left:27.5%;
    margin-top:0%
}

.contact_message{
    margin-top:15%;
}


}













</style>
