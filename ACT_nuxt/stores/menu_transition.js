import {ref, computed} from 'vue'
import {defineStore} from 'pinia'

export const from_header_menu = defineStore('from_header_menu', () => {
    
    const from_menu = ref(false)
    const menu_clicked_open = ref(false)
    const toggle_from_menu = () => {
        from_menu.value = !from_menu.value
    } 
    const clicked_open = () => {
        menu_clicked_open.value = !menu_clicked_open.value
        
        console.log(menu_clicked_open.value)
        console.log('xssx')
    } 
    console.log(menu_clicked_open.value)
    console.log('axxxx')
    
    return { from_menu, toggle_from_menu, clicked_open, menu_clicked_open }
    
})
