<template>
    



    <div class="investor_footer" style="z-index:-1; width:100%; position: fixed; height:400px;">
              <div class="footer_content" style="width:90%; margin:0">
                <div class="footer_grid_left">
                  <div class="footer_elm_left">
                    <img class="dashboard_footer_logo" src="~/assets/content/homepage/ACT_logo.png" alt="">
                  
                  </div>
                  
                  <div class="footer_elm_left bottom_padding">
                    <span class="footer_subheading">Copyright © GET MEDIA 2022</span>
                  </div>
                </div>

              </div>
            </div>


</template>




<style scoped>



.investor_footer {
    position: -webkit-sticky;
    position: sticky;
    bottom: 0;
    width:calc(100vw - 250px); 
    margin-left:250px;
}

.footer_logo{
color: var(--theme-color)
}

.footer_elm_left{
padding-bottom:10px;
white-space: nowrap;
color: var(--theme-color) !important
}



.footer_subheading{
white-space: nowrap;
color: var(--footer_subheading) !important;
text-decoration: none !important;
line-height:2.5
}


.footer_content {
padding-top: 80px;
padding-bottom: 35px;
padding-left: 50px;
padding-right: 50px;
}

.bottom_padding{
  padding-top:70px
}



@media (min-width: 768px) {
.footer_content {
padding-top: 100px;
padding-bottom: 50px;
}
}
@media (min-width: 1025px) {
.footer_content {
padding-top: 120px;
padding-bottom: 50px;
}
}



  .footer_grid_left {
display: grid;
grid-template-columns: repeat(1, 1fr);
grid-template-rows: repeat(3, 1fr);
grid-column-gap: 0px;
grid-row-gap: 0px;
width:50%;
margin-top:-50px
}




.dashboard_footer_logo{
width: 200px;
}





@media only screen and (min-width: 0px) and (max-width: 576px) {


  .dashboard_footer_logo{
width: 150px;
margin-top:50px
}

.investor_footer {
    margin-left:0px;
}

.bottom_padding{
  padding-top:20px
}

}







@media only screen and (min-width: 576px) and (max-width: 768px) {

  .dashboard_footer_logo{
width: 150px;
margin-top:50px
}

.investor_footer {
    margin-left:0px;
}

.bottom_padding{
  padding-top:20px
}


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