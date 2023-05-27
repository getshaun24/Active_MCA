<template>

    <div class="grid_xxx">

        <div class="image_section_container">
        <div class="image_section" data-speed="auto"></div>
    </div>

    <div class="text_section">

        <h6 class="title_text">Time-Savings</h6>
        <p>Settling a legal dispute can be a time-consuming and costly process. ACT's platform simplifies the settlement process and reduces the time required to negotiate a settlement. This can be especially helpful for busy individuals and businesses who want to resolve their legal disputes quickly and efficiently.</p>
        <br><br>
        <h6 class="title_text">Cost-Effective</h6>
        <p>Traditional legal settlements can be expensive, with high legal fees and other costs associated with the process. ACT's platform offers a more cost-effective solution, with lower fees and reduced overhead costs. This can help users save money while still achieving a fair settlement outcome.</p>
    </div>
    

        
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
            margin: 0% 7.5%;
            margin-bottom:10%
            }
    
        .text_section{
            margin-top:10%;
        }
    
        .title_text{
            margin:30px 0;
            font-size:250%
        }
    
        .image_section_container{
            overflow:hidden;
            min-height:800px;
            height:100%;
            border-radius:25px;
        }
        .image_section{
            background-image: url('~/assets/content/services/services_9.jpg');
            background-position: center; 
            background-repeat: no-repeat;
            background-size: cover;
            width:100%;
            align-content: center;
            min-height:850px;
            height:120%
        }
    
    
        </style>