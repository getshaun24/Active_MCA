<template>

<div class="top_text">
    <h5 class="counter_title">Chosen by a growing<br>
number of professionals.</h5>

<p>Quis ipsum suspendisse ultrices gravida dictum fusce ut. Ullamcorper malesuada proin libero nunc consequat interdum varius sit. In eu mi bibendum neque egestas. Sed viverra ipsum nunc aliquet bibendum enim facilisis gravida neque.</p>

</div>

    <div class="grid">

    <div class="grid_inner_section_1">
        <div class="section_1_image_1"></div>
        <div  class="section_1_counter">
            <p class="counter_text">Deals Closed</p>
            <h6 class="counter_nums">{{ deal_count }}</h6>
        </div>
    </div>



    <div class="section_1_image_2" style="height:520px; margin-left:-25%"></div>



    <div class="grid_inner_section_2">

        <div class="grid_inner_section_2_inner">
            <div class="section_2_counter">
                <p class="counter_text">Law Firms</p>
                    <h6 ref="target" class="counter_nums">{{ law_firm_count }}</h6>
            </div>
            <div class="section_2_image_1"></div>
       
        </div>

    <div class="section_2_image_2"></div>
        
</div>


<div class="section_3_image_1" style="height:520px"></div>


    </div>
        </template>



        
        <script setup>

import { ref } from 'vue'
import { useIntersectionObserver } from '@vueuse/core'



const target = ref(null)
const targetIsVisible = ref(false)
const disabled = ref(false)
const deal_count = ref(1750)
const law_firm_count = ref(0)

    const { stop } = useIntersectionObserver( target,
      ([{ isIntersecting }], observerElement) => {
        targetIsVisible.value = isIntersecting
        if (targetIsVisible.value == true){
          disabled.value = true

          deal_count.value = 1750
                setInterval(function(){
                    if (deal_count.value < 2567){
                    deal_count.value ++ 
                    }
                }, 1);

                law_firm_count.value = 0
                setInterval(function(){
                    if (law_firm_count.value < 224){
                        law_firm_count.value ++ 
                    }
                }, 15);
                    
     
            
        } else{
          disabled.value = false
        }
      },
    )




    
        </script>
        
        
        
        
        
        
        
        <style scoped>

.counter_title{
    margin-bottom:7%
}
        .top_text{
            width:60%;
            margin-left:20%;
            text-align: center;
        }
    
        .grid{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                grid-template-rows: repeat(1, 1fr);
                grid-column-gap: 10px;
                grid-row-gap: 10px;
                width:90%;
                margin:5%;
            }


            .grid_inner_section_1{
                display: grid;
                grid-template-columns: 1fr;
                grid-template-rows: repeat(2, 1fr);
                grid-column-gap: 10px;
                grid-row-gap: 10px;
                margin-right:25%;
            }

            .grid_inner_section_2{
                display: grid;
                grid-template-columns: 1fr;
                grid-template-rows: repeat(2, 1fr);
                grid-column-gap: 10px;
                grid-row-gap: 10px;
                margin-left:-25%
            }

            .grid_inner_section_2_inner{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                grid-template-rows: 1fr;
                grid-column-gap: 10px;
                grid-row-gap: 10px;
              
            }

    

        .section_1_image_1{
            background-image: url('~/assets/content/homepage/home_22.jpg');
            background-position: center; 
            background-repeat: no-repeat;
            background-size: cover;
            border-radius:25px;
            width:100%;
            align-content: center;
            height:250px
        }

        .section_1_image_2{
            background-image: url('~/assets/content/homepage/home_23.jpg');
            background-position: center; 
            background-repeat: no-repeat;
            background-size: cover;
            border-radius:25px;
            width:100%;
            align-content: center;
            height:250px
        }

        .section_2_image_1{
            background-image: url('~/assets/content/homepage/home_25.jpg');
            background-position: center; 
            background-repeat: no-repeat;
            background-size: cover;
            border-radius:25px;
            width:100%;
            align-content: center;
            height:250px
        }

        .section_2_image_2{
            background-image: url('~/assets/content/homepage/home_24.jpg');
            background-position: center; 
            background-repeat: no-repeat;
            background-size: cover;
            border-radius:25px;
            width:100%;
            align-content: center;
            height:250px
        }

        .section_3_image_1{
            background-image: url('~/assets/content/homepage/home_26.jpg');
            background-position: center; 
            background-repeat: no-repeat;
            background-size: cover;
            border-radius:25px;
            width:100%;
            align-content: center;
            height:250px
        }

        .section_1_counter{
            background-color:rgb(240, 224, 255);
            height:250px;
            width:100%;
            border-radius:25px
        }

        .section_2_counter{
            background-color:rgb(255, 255, 218);
            height:250px;
            width:100%;
            border-radius:25px
        }
        .counter_text{
            margin-left:20px;
            margin-bottom:145px
        }

        .counter_nums{
            margin-left:20px;
            margin-top:-20%
         
        }
    
    
        </style>