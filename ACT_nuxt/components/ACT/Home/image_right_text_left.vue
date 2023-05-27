<template>

<div class="grid_xxx">
<div class="text_section">
    <h6 class="title_text">Why People<br>Choose Us</h6>
    <p>Velit sed ullamcorper morbi tincidunt ornare massa eget egestas. Dictum fusce ut placerat orci nulla pellentesque. Diam sollicitudin tempor id eu nisl. Purus gravida quis blandit turpis cursus in hac habitasse platea. Laoreet non curabitur gravida arcu ac tortor. Porttitor eget dolor morbi non arcu.
<br><br>
Nulla porttitor massa id neque aliquam. Quisque sagittis purus sit amet volutpat consequat mauris. Interdum velit euismod in pellentesque.
<br><br>
Elit sed vulputate mi sit amet mauris. Nunc sed blandit libero volutpat sed cras ornare arcu dui. Velit sed ullamcorper morbi tincidunt ornare massa.</p>
</div>

<div class="image_section" data-speed="1.1"></div>
    
</div>
    </template>
    
    <script setup>

    </script>
    
    
    
    
    
    
    
    <style scoped>

    .grid_xxx{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: 1fr;
        grid-column-gap: 100px;
        grid-row-gap: 0px;
        width:85%;
        margin: 10% 7.5%;
        margin-top:10%
        }

    .text_section{
        margin-top:15%;
        z-index:6
    }

    .title_text{
        margin:30px 0
    }

    .image_section{
        background-image: url('~/assets/content/homepage/home_19.jpg');
        background-position: center; 
        background-repeat: no-repeat;
        background-size: cover;
        border-radius:25px;
        width:100%;
        align-content: center;
        min-height:800px
    }




@media only screen and (min-width: 0px) and (max-width: 576px) {
}

@media only screen and (min-width: 576px) and (max-width: 768px) {
}

@media only screen and (min-width: 768px) and (max-width: 992px) {
}

@media only screen and (min-width: 992px) and (max-width: 1200px) {
    .grid_xxx{
        margin-top:25%
        }

}

@media only screen and (min-width: 1200px) and (max-width: 1400px) {
    .grid_xxx{
        margin-top:20%
        }

}

@media only screen and (min-width: 1400px) and (max-width: 1600px) {
}

@media only screen and (min-width: 1600px) and (max-width: 5600px) {
}





    </style>