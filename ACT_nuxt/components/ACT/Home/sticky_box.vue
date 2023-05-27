<template>
    


    <div class="sticky_grid">

        <div class="left_images">

            <div class="sticky_img_1">
                <div class="stickyBoxPaperOverlay"></div>
            <img class="left_img_1" src="~/assets/content/homepage/home_10.png" alt="">
            </div>
            <div class="white_mask"></div>
            <div class="white_mask_background"></div>
            <div class="sticky_img_2">
                <div class="stickyBoxPaperOverlay"></div>
            <img class="left_img_2" src="~/assets/content/homepage/home_11.png" alt="">
            </div>
            <div class="sticky_img_3">
                <div class="stickyBoxPaperOverlay"></div>
            <img class="left_img_3" src="~/assets/content/homepage/home_12.png" alt="">
            </div>
            <div class="sticky_img_4">
                <div class="stickyBoxPaperOverlay"></div>
            <img class="left_img_4" src="~/assets/content/homepage/home_13.png" alt="">
            </div>
    </div>

        <div class="right_text">

            <div class="text_box_1">
                <div class="icon_1 icons">Fast and Fair Deals<img class="icon_img" src="~/assets/content/homepage/home_15.png"></div>
            <h3 style="font-size: 2.5rem;">Enter Your Amounts and Share With Counterparty</h3>
            <p class="body_text">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </div>
   
        <div class="text_box_2">
            <div class="icon_2 icons">Algorithmic Consensus<img class="icon_img" src="~/assets/content/homepage/home_16.png"></div>
        <h3 style="font-size: 2.5rem;">We determine if there is a match</h3>
            <p class="body_text">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </div>

    <div class="text_box_3">
        <div class="icon_3 icons">Easy Communication<img class="icon_img" src="~/assets/content/homepage/home_17.png"></div>
        <h3 style="font-size: 2.5rem;">We determine if there is a match</h3>
            <p class="body_text">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </div>
  
        <div class="end_trigger" style="margin-top:40vh"></div>
    <div class="text_box_4">
        <div class="icon_4 icons">Full Settlement Pipeline<img class="icon_img" src="~/assets/content/homepage/home_18.png"></div>
        <h3 style="font-size: 2.5rem;">We determine if there is a match</h3>
            <p class="body_text">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </div>
    </div>

    </div>
</template>




<style scoped>

.sticky_grid{
display: grid;
grid-template-columns: repeat(2, 1fr);
grid-template-rows: 1fr;
grid-column-gap: 60px;
grid-row-gap: 0px;
margin-top:10%;
margin-bottom:10%;
width:80%;
margin-left:7.5%
}

.left_images{
    display:flex;
    flex-direction:column;
    width:100%;
}
.stickyBoxPaperOverlay {
    position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  opacity:.4;
  background-size: 80%;
  background-repeat: repeat;
  background-image: url("~/assets/content/paper/paper_overlay_3.jpg");
  mix-blend-mode: multiply;
  pointer-events: none;
}


.sticky_img_1 {
    background-color: #a7d3e8;
    z-index:1;
    width:100%;
    height:80vh;
    display:flex;
    justify-content:center;
    align-items:center;
    border-radius:50px;
    opacity:.9;
    overflow:hidden;
    filter: drop-shadow(2px 2px 5px #3d3d3d34);
}

.sticky_img_2 {
    background-color: #fffeeb;
    z-index:1;
    width:100%;
    height:80vh;
    display:flex;
    justify-content:center;
    align-items:center;
    border-radius:50px;
    opacity:1;
    overflow:hidden
}
.sticky_img_3 {
    background-color: #efe2ff;
    z-index:2;
    width:100%;
    height:80vh;
    display:flex;
    justify-content:center;
    align-items:center;
    border-radius:50px;
    opacity:1;
    overflow:hidden
}
.sticky_img_4 {
    background-color: #e4fff1;
    z-index:3;
    width:100%;
    height:80vh;
    display:flex;
    justify-content:center;
    align-items:center;
    border-radius:50px;
    opacity:1;
    overflow:hidden
}

.left_img_1{
    width:70%;
    height:auto;

}

.left_img_2{
    width:80%;
    height:auto
}
.left_img_3{
    width:100%;
    height:auto
}
.left_img_4{
    width:100%;
    height:auto
}

.white_mask_background{
    background-color:#fff;
    z-index:4;
    width:100%;
    height:9.7vh;
    margin-top:-10vh
}
.white_mask{
    background-color:#d8d8d8;
    z-index:5;
    width:100%;
    height:9.8vh;
    margin-top:.1vh;
    background-size: 95%;
    opacity:.5;
  background-repeat: repeat;
  background-image: url("~/assets/content/paper/paper_overlay_3.jpg");
  mix-blend-mode: multiply;
  pointer-events: none;
}


.right_text{
    width:95%;
    margin-left:10%
}
.text_box_1{
    margin-top:15vh
}


.text_box_2{
    margin-top:40vh
}

.text_box_3{
    margin-top:30vh
}

.text_box_4{
    margin-top:40vh
}

.icons{
border-radius:15px;
width:210px;
padding:10px 20px;
}
.icon_1{
    background-color: #a7d3e8;
}

.icon_2{
    background-color: #fffeeb;
}

.icon_3{
    background-color: #efe2ff;
}

.icon_4{
    background-color: #e4fff1;
}

.icon_img{
    width:30px;
    height:auto;
    margin-left:20px;
    margin-top:-5px;
    position:absolute
}

.body_text{
    font-size:130%
}
</style>