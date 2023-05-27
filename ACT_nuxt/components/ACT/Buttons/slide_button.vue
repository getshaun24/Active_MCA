<template>
    
    <button ref="target" class="slide_button" :class="{ slide_anim: disabled }" >
        <div :class="{ arrow_anim: disabled }" class="arrow_svg"></div>
        <p :class="{ text_anim: disabled }" class="slide_button_text">{{ button_text }}</p>
    </button>

</template>



<script setup>
import { ref } from 'vue'
import { useIntersectionObserver } from '@vueuse/core'

const props = defineProps(['button_text'])


const target = ref(null)
const targetIsVisible = ref(false)
const disabled = ref(false)

    const { stop } = useIntersectionObserver( target,
      ([{ isIntersecting }], observerElement) => {
        targetIsVisible.value = isIntersecting
        if (targetIsVisible.value == true){
          disabled.value = true
        } else{
          disabled.value = false
        }
      },
    )




</script>




<style scoped>





.slide_button{
            background-color: #000 !important;
            border-radius:50px/50px;
            width:0px;
            height:40px;
            padding:0px;
            margin-top:15px;
            opacity:0
        }
        .arrow_svg{
            border: 1px solid #000;
            border-radius:100%;
            padding:7px;
            width:20px;
            height:20px;
            object-position:center;
            content:url('~/assets/content/icons/right_arrow.svg');
            background-color: #fff;
            margin-top:-3px;
            margin-left:50px;
            transition: all 400ms ease !important;
            opacity:0
        }
        
        .slide_button_text{
            color:rgb(255, 255, 255);
            margin-left:25px;
            margin-top: -25px;
            font-size:13px;
            transition: all 400ms ease !important;
            opacity:0
        
        }
        
        .slide_button:hover .arrow_svg{
            filter: invert(1);
            margin-left:101px;
            transition: all 400ms ease !important;
        }
        
        .slide_button:hover .slide_button_text{
            margin-left:-35px;
            transition: all 400ms ease !important;
        }

        .slide_anim {
          transition: all 600ms ease 200ms;
          width:145px;
          padding:3px;
          opacity:1
}

        .arrow_anim{
            transition: all 600ms ease 200ms;
            margin-left:-2px;
            opacity:1
        }
        .text_anim{
            opacity:1
        }

</style>