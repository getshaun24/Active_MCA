// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  
  
  app: {
    head: {
      meta: [
        // <meta name="viewport" content="width=device-width, initial-scale=1">
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ],
      script: [
        // {src: "https://cdn.plaid.com/link/v2/stable/link-initialize.js", body: true, async: true}
      ],
      link: [
        // <link rel="stylesheet" href="https://myawesome-lib.css">
        //     { rel: 'icon', href: '~/public/ACT_ICON.png' },
      ],
    }
  },
  
  
  
  css: [
    '~/assets/css/main.css',
  ],
  
  
  modules: [
    '@vueuse/nuxt', 
    [
      '@pinia/nuxt',
      {
        autoImports: [
          // automatically imports `defineStore`
          'defineStore', // import { defineStore } from 'pinia'
          // automatically imports `defineStore` as `definePiniaStore`
          ['defineStore', 'definePiniaStore'], // import { defineStore as definePiniaStore } from 'pinia'
        ],
      },
    ],
  ],     




  build: {
    transpile: ['gsap', 'swiper'],
  },
  
  "nitro":{
    "preset":"node-server",
  },
  
  runtimeConfig: {
    public: {
      flask_url: process.env.FLASK_URL
    },

    modules: ['@sidebase/nuxt-session'],
    
  },
  


  
});

