<template>
    <div style="margin-top:10%">
        <p class="button_text">Start Closing Deals Now</p>
    <div class="middle_line"></div>
    <div ref="hover_el" :class="in_box" class="button_container">
    <div ref="el" class="button_el" :style="{'margin-top': button_top + 'px', 'margin-left': button_left + 'px'}">Settle Now</div>
</div>
</div>


</template>



<script setup>

import { ref } from 'vue'
import { useElementBounding, useMouseInElement, useElementHover, useWindowSize, useParallax } from '@vueuse/core'

const button_top = ref(0)
const button_left = ref(0)

const hover_el = ref(null)
const isHovered = useElementHover(hover_el)
const mouse_height = ref(null)


const el = ref(null)
const { x1, y1, top, right, bottom, left, width, height } = useElementBounding(hover_el)

const { elementX, elementY, isOutside } = useMouseInElement(el)




const in_box = computed(() => {


        if (isHovered.value == true){
            if (elementY.value < 50){
                button_top.value = elementY.value - 10
            }
            else{
                button_top.value = (elementY.value + height.value) / 2 
            }
            if (elementX.value < 50){
                button_left.value = elementX.value - 20
            }
            else{
            button_left.value = (elementX.value + width.value) / 2
        }

        }
        else{
            button_top.value = 20
            button_left.value = 20
        }
})




</script>




<style scoped>


.button_text{
    text-align: center;
    margin-bottom:40px;
    z-index:100

}

.middle_line{
    border-top:solid 1px rgba(103, 103, 103, 0.349);
    
}
.button_container{
    height:75px;
    position: relative;
    border: #fff 1px solid;
    width:150px;
    margin:auto;
    margin-top:-42px;
    background-color: #fff;
}

.button_el {
    border:2px solid #000;
    border-radius:50px/50px;
  cursor: pointer;
  transition: all 400ms ease;
  padding:3px;
  width:100px;
  margin:auto;
  margin-top:25px;
  text-align: center;
  background-color: #fff;

}




.button_el:hover {
  transform: scale(1.1);
  color: #fff;
  background-color:#000
}


</style>