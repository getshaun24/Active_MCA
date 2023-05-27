<template>



    <div ref="hover_el" :class="in_box" class="button_container">
    <NuxtLink :to="link_to" ref="el" class="button_el" :style="{'margin-top': button_top + 'px', 'margin-left': button_left + 'px'}">{{ button_text }}</NuxtLink>
</div>



</template>



<script setup>

import { ref } from 'vue'
import { useElementBounding, useMouseInElement, useElementHover, useWindowSize, useParallax } from '@vueuse/core'


const props = defineProps(['button_text', 'background_color', 'color', 'link_to'])


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
                button_top.value = elementY.value - 20
            }
            else{
                button_top.value = (elementY.value + height.value) / 2 
            }
            if (elementX.value < 50){
                button_left.value = elementX.value - 20
            }
            else{
            button_left.value = (elementX.value + width.value) / 6
        }

        }
        else{
            button_top.value = 5
            button_left.value = 5
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
    height:50px;
    border: #fafdff00 1px solid;
    width:100px;
    margin:auto;
    margin-top:5px;
}

.button_el {
    border:2px solid #000;
    border-radius:50px/50px;
  cursor: pointer;
  transition: all 400ms ease;
  padding:4px 25px;
  width:120px;
  margin:auto;
  margin-top:15px;
  text-align: center;
  background-color: v-bind(background_color);
  color: v-bind(color);
  font-size: 20px;
  white-space: nowrap;

}


.button_el:hover {
  transform: scale(1.1);
  color: v-bind(background_color);
  background-color:v-bind(color);
  
}


</style>