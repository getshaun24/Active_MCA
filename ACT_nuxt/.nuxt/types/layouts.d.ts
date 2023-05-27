import { ComputedRef, Ref } from 'vue'
export type LayoutKey = "default"
declare module "/Users/shauncohen/Documents/BAT_CAVE/ACTIVE_MCA/act_nuxt/node_modules/nuxt/dist/pages/runtime/composables" {
  interface PageMeta {
    layout?: false | LayoutKey | Ref<LayoutKey> | ComputedRef<LayoutKey>
  }
}