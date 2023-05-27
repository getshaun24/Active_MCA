import type { NavigationGuard } from 'vue-router'
export type MiddlewareKey = string
declare module "/Users/shauncohen/Documents/BAT_CAVE/ACTIVE_MCA/act_nuxt/node_modules/nuxt/dist/pages/runtime/composables" {
  interface PageMeta {
    middleware?: MiddlewareKey | NavigationGuard | Array<MiddlewareKey | NavigationGuard>
  }
}