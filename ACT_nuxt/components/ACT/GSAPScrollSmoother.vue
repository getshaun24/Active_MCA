
        <template>
        <div id="smooth-wrapper">
        <div id="smooth-content">
        <slot></slot>
        </div>
        </div>
        </template>

        <script setup>


        import { onMounted, onUnmounted, onBeforeMount, ref } from 'vue';
        import { gsap } from 'gsap'
        import { ScrollTrigger } from 'gsap/ScrollTrigger'
        import { ScrollSmoother } from 'gsap/ScrollSmoother'
        import { SplitText } from 'gsap/SplitText'
        import { useWindowSize } from '@vueuse/core'

        import { page_to } from "~/stores/page_to.js"

        // Initialize all GSAP plugins

        // gsap.registerPlugin(ScrollTrigger, ScrollSmoother, SplitText)

        if (process.client) {
  gsap.registerPlugin(ScrollTrigger, ScrollSmoother, SplitText);
}



        // sleep time expects milliseconds
        function sleep (time) {
          return new Promise((resolve) => setTimeout(resolve, time));
        }


        const current_route = useRoute()
        console.log('this_route', current_route.name)



        const smoothy = ref()





        const { width, height } = useWindowSize()


   const sleep_for = ref(100)





  const route_to = page_to()







        // Initialize the smooth scroll plugin
        onMounted(() => {





        


    sleep_for.value = 100







  // sleep for a few milli-seconds lionger then trhe page transition time
  sleep(sleep_for.value).then(() => { 




ScrollTrigger.refresh();
          

   smoothy.value =  ScrollSmoother.create({
   smooth: 2.5, 
   effects: true, 
   normalizeScroll: false,
   normalizeScroll: {
    allowNestedScroll: true
  },
  smoothTouch: 0.01,  
   })


    smoothy.value.scrollTo(0, false)

   

    // ------------------------------ Footer ------------------------------
// ------------------------------ Footer ------------------------------



    ScrollTrigger.create({
        trigger: "footer",
        start: "bottom bottom", 
        // end: "bottom 1000px",
        pin: "footer",
        pinSpacing: true,
      });




// ------------------------------ Home ------------------------------
// ------------------------------ Home ------------------------------






if (current_route.name == 'index'){

  // sleep(1000).then(() => { ScrollTrigger.refresh() })




  ScrollTrigger.create({
        trigger: ".sticky_img_1",
        start: "center center", 
        pin: ".sticky_img_1",
        endTrigger: ".end_trigger",
      });
      ScrollTrigger.create({
        trigger: ".sticky_img_2",
        start: "center center", 
        pin: ".sticky_img_2",
        endTrigger: ".end_trigger",
      });
ScrollTrigger.create({
        trigger: ".sticky_img_3",
        start: "center center", 
        pin: ".sticky_img_3",
        endTrigger: ".end_trigger",
      });
ScrollTrigger.create({
        trigger: ".sticky_img_4",
        start: "center center", 
        pin: ".sticky_img_4",
        endTrigger: ".end_trigger",
      });
      ScrollTrigger.create({
        trigger: ".white_mask",
        start: "bottom bottom", 
        pin: ".white_mask",
        endTrigger: ".end_trigger",
      });
      ScrollTrigger.create({
        trigger: ".white_mask_background",
        start: "bottom bottom", 
        pin: ".white_mask_background",
        endTrigger: ".end_trigger",
      });

    }
      

      // ------------------------------ CONTACT PAGE ------------------------------ //
      // ------------------------------ CONTACT PAGE ------------------------------ //

      if (current_route.name == 'contact'){

      ScrollTrigger.create({
        trigger: ".contact_img",
        start: "top top", 
        end: "bottom top",
        endTrigger:"html",
        pin: ".contact_img",
      });




      if(width.value < 576){

      ScrollTrigger.create({
        trigger: ".map_button",
        start: "center 71%", 
        end: "bottom top",
        endTrigger:"html",
        pin: ".map_button",
      });

      ScrollTrigger.create({
        trigger: ".top_line",
        start: "top top", 
        end: "bottom -15px",
        pin: ".top_line",
      });

    }else if(width.value < 650){
      
      ScrollTrigger.create({
        trigger: ".map_button",
        start: "center 80%", 
        end: "bottom top",
        endTrigger:"html",
        pin: ".map_button",
      });

      ScrollTrigger.create({
        trigger: ".top_line",
        start: "top top", 
        end: "bottom -15px",
        pin: ".top_line",
      });
      
    }

  else if(width.value < 768){
      
      ScrollTrigger.create({
        trigger: ".map_button",
        start: "center 90%", 
        end: "bottom top",
        endTrigger:"html",
        pin: ".map_button",
      });

      ScrollTrigger.create({
        trigger: ".top_line",
        start: "top top", 
        end: "bottom -10px",
        pin: ".top_line",
      });
      
    }

    else if(width.value < 992){
      
      ScrollTrigger.create({
        trigger: ".map_button",
        start: "center 78%", 
        end: "bottom top",
        endTrigger:"html",
        pin: ".map_button",
      });

      ScrollTrigger.create({
        trigger: ".top_line",
        start: "top top", 
        end: "bottom 8px",
        pin: ".top_line",
      });
      
    }

    else if(width.value < 1200){
      
      ScrollTrigger.create({
        trigger: ".map_button",
        start: "center 68%", 
        end: "bottom top",
        endTrigger:"html",
        pin: ".map_button",
      });

      ScrollTrigger.create({
        trigger: ".top_line",
        start: "top top", 
        end: "bottom -15px",
        pin: ".top_line",
      });
      
    }
    
    else{

      ScrollTrigger.create({
        trigger: ".map_button",
        start: "center 65%", 
        end: "bottom top",
        endTrigger:"html",
        pin: ".map_button",
      });

      ScrollTrigger.create({
        trigger: ".top_line",
        start: "top top", 
        end: "bottom -15px",
        pin: ".top_line",
      });

    }


  }


})
        })

        onUnmounted(() => {




  
          // smoothy.value.refresh(); // <- Easy Cleanup!
          // console.log('REFRESHED')

        })

        </script>

