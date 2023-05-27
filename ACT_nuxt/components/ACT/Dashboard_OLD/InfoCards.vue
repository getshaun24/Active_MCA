<template>
    
    <div class="info_card_grid">
                
                <div class="info_card">
                    <h1 class="card_title">New Inquiries</h1>
                    <h1 class="card_data">5</h1>
                    <div class="card_circle"></div>
                    <h2 class="card_stats"><span class="stat_color_green">10%</span>since last month</h2>
                </div>

                <div class="info_card">
                    <h1 class="card_title">Closed Settlements</h1>
                    <h1 class="card_data">37</h1>
                    <div class="card_circle_2"></div>
                    <h2 class="card_stats"><span class="stat_color_green">32%</span>since last month</h2>
                </div>

                <div class="info_card">
                    <h1 class="card_title">Unsettled</h1>
                    <h1 class="card_data">2</h1>
                    <div class="card_circle_3"></div>
                    <h2 class="card_stats"><span class="stat_color_red">3%</span> from last month</h2>
                </div>

                <div class="info_card">
                    <h1 class="card_title">Dollars Settled</h1>
                    <h1 class="card_data">$82,357</h1>
                    <div class="card_circle_4"></div>
                    <h2 class="card_stats"><span class="stat_color_green">240%</span> from last month</h2>
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
    width: 95%;
    padding-top: 5%;
    margin-left:30px
}

.info_card {
    background-color: #fff;
    width: 100%;
    height: 145px;
    border-radius: 25px;
    filter: drop-shadow(2px 2px 4px #0018393d);
    transition: 0.3s;
}
.info_card:hover {
    margin-top: -2.5px;
}
.card_title {
    font-size: 18px;
    padding-top: 20px;
    padding-left: 25px;
    letter-spacing: normal;
    color: grey;
}
.card_data {
    font-size: 45px;
    font-weight: 700;
    padding-left: 25px;
    padding-top: 5px;
}
.card_circle {
    width: 50px;
    height: 50px;
    background-color: rgba(0, 0, 255, 0.66);
    border-radius: 100%;
    margin-left: 75%;
    margin-top: -75px;
    margin-bottom: 50px;
}
.card_circle_2 {
    width: 50px;
    height: 50px;
    background-color: #38c090;
    border-radius: 100%;
    margin-left: 75%;
    margin-top: -75px;
    margin-bottom: 50px;
}
.card_circle_3 {
    width: 50px;
    height: 50px;
    background-color: #f1a326;
    border-radius: 100%;
    margin-left: 75%;
    margin-top: -75px;
    margin-bottom: 50px;
}
.card_circle_4 {
    width: 50px;
    height: 50px;
    background-color: rgba(152, 46, 151, 0.704);
    border-radius: 100%;
    margin-left: 75%;
    margin-top: -75px;
    margin-bottom: 50px;
}
.card_stats {
    font-size: 14px;
    padding-left: 25px;
}
.stat_color_green {
    padding: 2px 8px;
    color: #fff;
    background-color: rgba(0, 128, 0, 0.7);
    border-radius: 5px;
    margin-right: 3.5%;
    border: 2px solid green;
}
.stat_color_red {
    padding: 2px 8px;
    color: #fff;
    background-color: rgba(214, 3, 3, 0.522);
    border-radius: 5px;
    margin-right: 3.5%;
    border: 2px solid rgba(255, 0, 0, 0.806);
}


</style>