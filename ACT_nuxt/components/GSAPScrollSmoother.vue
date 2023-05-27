
        <template>
        <div id="smooth-wrapper">
        <div id="smooth-content">
        <slot></slot>
        </div>
        </div>
        </template>

        <script setup lang="ts">


        import { onMounted, onUnmounted, ref } from 'vue';
        import { gsap } from 'gsap'
        import { ScrollTrigger } from 'gsap/ScrollTrigger'
        import { ScrollSmoother } from 'gsap/ScrollSmoother'

        // Initialize all GSAP plugins
        if (process.client) {
        gsap.registerPlugin(ScrollTrigger, ScrollSmoother)
        }


        const smoothy = ref()


        // Initialize the smooth scroll plugin
        onMounted(() => {
        smoothy.value =  ScrollSmoother.create({
        smooth: 2, // Seconds it takes to "catch up" to native scroll position
        effects: true, // Look for data-speed and data-lag attributes on elements and animate accordingly
   //     normalizeScroll: true
        })

        })


        onUnmounted(() => {
          smoothy.value.refresh(); // <- Easy Cleanup!
        })

        </script>

