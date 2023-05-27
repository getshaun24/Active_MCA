import {ref, computed} from 'vue'
import {defineStore} from 'pinia'

export const page_to = defineStore('page_to', () => {
    
    const current_page_to = ref('')
    const current_page_from = ref('')    
    const page_to_update = (old_page, new_page) => {
        current_page_from.value = old_page
        current_page_to.value = new_page
    } 
    
    return { current_page_to, current_page_from, page_to_update }
    
})
