
<template>
    
    <div class="landing_container">
    <div class="landing_left_blur">
                            <div class="landing_left">
                              <div style="margin-top:5%">
                            <h5 class="landing_title">MCA Software<br>Active & Responsive</h5>
        
        
                            <ACTButtonsSlideButton button_text="Sign Up"/>
        
                            <p class="landing_text">
                              Active MCA is a premium Merchant Cash Advance (MCA) management software that is ACTIVE and responsive to your daily funding system. We help you digitize your MCA processes and automate the manual steps from intake steps, auto-decisioning with artificial intelligence, functional due-diligence, integrated e-sign documentation, automated scheduled transactions, and intuitive payment tracking.
                            </p>
                              </div>
                            </div>
                            </div>

  <video poster="~/assets/content/homepage/home_1.jpg" class="landing_vid" playsinline autoplay muted loop>
  <source src="~/assets/content/homepage/active/active_ball.mp4" type="video/mp4">
</video>
</div>

</template>



<script setup>





</script>





        <style scoped>

        .landing_container{
          height:100vh
        }
        
        .landing_vid{
          width:70%;
          margin-left:15%;
          margin-top:15%
        }
        .landing_title{
          margin-bottom:10%
        }
      .image_text_1{
        margin-top:112px;
        margin-left:150px;
        position:absolute;
        z-index:10;
        background-color:#fff;
        padding:10px;
        width:160px;
        border-radius:15px;
        opacity:0
      }

      .image_text_2{
        margin-top:356px;
        margin-left:13px;
        position:absolute;
        z-index:10;
        background-color:#fff;
        padding:10px;
        width:92px;
        border-radius:15px;
        opacity:0
      }


      .image_text_3{
        margin-top:-50px;
        margin-left:235px;
        position:absolute;
        z-index:10;
        background-color:#fff;
        padding:10px;
        width:140px;
        border-radius:15px;
        opacity:0
      }

      .image_text_1_anim{
        opacity:1;
        transition: all 500ms ease 300ms;
      }
      .image_text_2_anim{
        opacity:1;
        transition: all 500ms ease 300ms;
      }
      .image_text_3_anim{
        opacity:1;
        transition: all 500ms ease 300ms;
      }





      .landing_image_1{
        width:200px;
        height:255px;
        border-radius: 25px;
        margin-top:-60%;
        margin-left:62%;
        z-index:3;
        object-fit: cover;
        position: absolute;
        opacity:.8;
        -webkit-transform: scale(1.15);
    -moz-transform: scale(1.15);
    -o-transform: scale(1.15);
    -ms-transform: scale(1.15);
    transform: scale(1.15);
      }

      .landing_image_2{
        width:200px;
        height:300px;
        border-radius: 25px;
        margin-top:30%;
        margin-left:-35%;
        z-index:3;
        object-fit: cover;
        position: absolute;
        opacity:.8;
        -webkit-transform: scale(1.15);
    -moz-transform: scale(1.15);
    -o-transform: scale(1.15);
    -ms-transform: scale(1.15);
    transform: scale(1.15);
      }

      .landing_image_3{
        width:250px;
        height:350px;
        border-radius: 25px;
        margin-top:105%;
        margin-left:80%;
        z-index:3;
        object-fit: cover;
        position: relative;
        opacity:.8;
        -webkit-transform: scale(1.15);
    -moz-transform: scale(1.15);
    -o-transform: scale(1.15);
    -ms-transform: scale(1.15);
    transform: scale(1.15);
      }

      .landing_image_1_anim{
        transition: all 700ms ease;
        margin-top:-40%;
        margin-left:60%;
        opacity:1;
        -webkit-transform: scale(1);
    -moz-transform: scale(1);
    -o-transform: scale(1);
    -ms-transform: scale(1);
    transform: scale(1);
      }

      .landing_image_2_anim{
        transition: all 800ms ease;
        margin-top:40%;
        margin-left:-30%;
        opacity:1;
        -webkit-transform: scale(1);
    -moz-transform: scale(1);
    -o-transform: scale(1);
    -ms-transform: scale(1);
    transform: scale(1);
      }

      .landing_image_3_anim{
        transition: all 900ms ease;
        margin-top:85%;
        margin-left:95%;
        opacity:1;
        -webkit-transform: scale(1);
    -moz-transform: scale(1);
    -o-transform: scale(1);
    -ms-transform: scale(1);
    transform: scale(1);
      }


        .btn-arrow span {
          display: inline-block;
          position: relative;
          transition: all 300ms ease-out;
          will-change: transform;
        }
        .btn-arrow:hover span {
          transform: translate3d(-1rem, 0, 0);
        }
        .btn-arrow svg {
          position: absolute;
          width: 1.1em;
          right: 0px;
          right: 0rem;
          opacity: 0;
          top: 50%;
          transform: translateY(-50%);
          transition: all 300ms ease-out;
          will-change: right, opacity;
        }
        .btn-arrow svg * {
          stroke-width: 5;
          stroke-color: transparent;
        }
        .btn-arrow:hover svg {
          opacity: 1;
          right: -2rem;
        }
        
        
        
        
        
        
        .landing_left_blur{
            width:50%;
            height:100vh;
            backdrop-filter: blur(20px);
            background-color:rgba(71, 71, 71, 0.25);
            top:0;
            left:0;
            position: absolute;
        }
        
        .landing_left{
            padding-top:15vh;
            width:100%;
            margin-left:5%
        }
        .landing_right{
            margin-top:15vh;
            width:80%;
            margin-left:5%;
        }
        
        
     
        
        .landing_text{
        margin-top:30px;
        width:80%;
        font-size:110%
        }
        
        
        .landing_image_background_1{
            width: 60%;
            z-index:1;
            position: relative;
            transform: rotate(15deg);
            margin-left:-3px;
            margin-top:-12px;
            opacity:1;
            max-height:500px;
            max-width:500px
        }
        .landing_image_background_2{
            width:100%;
            margin-top:-40%;
            margin-left:-15px;
            z-index:0;
            position: relative;
            opacity:1;
            max-height:500px;
            max-width:500px
        }
        .landing_image_background_3{
            width:90%;
            margin-top:-60%;
            margin-left:77%;
            z-index:3;
            position: relative;
            width:60%;
            opacity:1;
            max-height:500px;
            max-width:500px
        }



        .landing_image_background_1_anim {
          transition: all 800ms ease;
          margin-top:12px;
          opacity:.7;
          -webkit-transform: scale(1.15);
    -moz-transform: scale(1.15);
    -o-transform: scale(1.15);
    -ms-transform: scale(1.15);
    transform: scale(1.15);
}

.landing_image_background_2_anim {
          transition: all 800ms ease;
          margin-top:-50%;
          margin-left:0px;
          opacity:.3;
          -webkit-transform: scale(1.15);
    -moz-transform: scale(1.15);
    -o-transform: scale(1.15);
    -ms-transform: scale(1.15);
    transform: scale(1.15);
}

.landing_image_background_3_anim {
          transition: all 800ms ease;
          margin-top:-50%;
            margin-left:67%;
            opacity:.3;
            -webkit-transform: scale(1.15);
    -moz-transform: scale(1.15);
    -o-transform: scale(1.15);
    -ms-transform: scale(1.15);
    transform: scale(1.15);
}

                    </style>
                    
                    
                    
                    

        