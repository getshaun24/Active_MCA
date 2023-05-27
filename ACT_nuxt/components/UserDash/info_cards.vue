<template>
    


    <div class="info_card_grid">
                
                <div class="info_card">
                    <h1 class="card_title">Total Settlements</h1>
                    <h1 class="card_data">127</h1>
                    <div class="card_circle"></div>
                    <h2 class="card_stats"><span class="stat_color_green">10%</span>since last quarter</h2>
                </div>

                <div class="info_card">
                    <h1 class="card_title">New inquiries</h1>
                    <h1 class="card_data">2</h1>
                    <div class="card_circle_3"></div>
                    <h2 class="card_stats"><span class="stat_color_red">3%</span> from last quarter</h2>
                </div>

                <div class="info_card">
                    <h1 class="card_title">Closed</h1>
                    <h1 class="card_data">48</h1>
                    <div class="card_circle_4"></div>
                    <h2 class="card_stats"><span class="stat_color_green">240%</span> from last quarter</h2>
                </div>

                <div class="info_card">
                    <h1 class="card_title">Total Value</h1>
                    <h1 class="card_data">$820,357</h1>
                    <div class="card_circle_2"></div>
                    <h2 class="card_stats"><span class="stat_color_green">32%</span>since last quarter</h2>
                </div>

                 </div>




</template>
















<style scoped>


.info_card_grid {
display: grid;
grid-template-columns: repeat(4, 1fr);
grid-template-rows: repeat(1, 1fr);
grid-column-gap: 20px;
grid-row-gap: 20px;
width:100%;
padding-top:5%
}

.info_card{
    background-color:#fff;
    width:100%;
    height:145px;
    border-radius: 25px;
    filter: drop-shadow(2px 2px 4px #0018393d);
    transition: 0.3s;
}

/* .info_card:nth-child(1){
border:1px solid rgba(0, 0, 255, 0.25)
}

.info_card:nth-child(2){
border:1px solid rgb(56, 192, 144, 0.25)
}

.info_card:nth-child(3){
border:1px solid rgb(241, 163, 38, 0.25)
}

.info_card:nth-child(4){
border:1px solid rgba(152, 46, 151, 0.25)
} */

.info_card:hover{
    margin-top:-2.5px
}

.card_title{
    font-size:18px;
    padding-top:20px;
    padding-left:15px;
    letter-spacing: normal;
    color:grey
}

.card_data{
    font-size:2.25vw;
    font-weight: bold;
    padding-left:1.5vw;
    padding-top:1vw;
    padding-bottom:1vw
} 
/* 
.card_circle{
    width:50px;
    height:50px;
    background-color:rgba(0, 0, 255, 0.66);
    border-radius:100%;
    margin-left:70%;
    margin-top:-80px;
    margin-bottom:55px
}

.card_circle_2{
    width:50px;
    height:50px;
    background-color:rgb(56, 192, 144);
    border-radius:100%;
    margin-left:70%;
    margin-top:-80px;
    margin-bottom:55px
}

.card_circle_3{
    width:50px;
    height:50px;
    background-color:rgb(241, 163, 38);
    border-radius:100%;
    margin-left:70%;
    margin-top:-80px;
    margin-bottom:55px
}

.card_circle_4{
    width:50px;
    height:50px;
    background-color:rgba(152, 46, 151, 0.704);
    border-radius:100%;
    margin-left:70%;
    margin-top:-80px;
    margin-bottom:55px
} */

.card_stats{
    margin-top:30%;
    font-size:14px;
    padding-left:25px;
    line-height: 1.75;
}

.stat_color_green{
    padding:2px 8px;
    color:#fff;
    background-color: rgba(0, 128, 0, 0.7);
    border-radius:5px;
    margin-right:3.5%;
    border:2px solid green
}

.stat_color_red{
    padding:2px 8px;
    color:#fff;
    background-color: rgba(214, 3, 3, 0.522);
    border-radius:5px;
    margin-right:3.5%;
    border:2px solid rgba(255, 0, 0, 0.806)
}




</style>




