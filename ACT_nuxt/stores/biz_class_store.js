import {ref, computed} from 'vue'
import {defineStore} from 'pinia'

export const biz_class_store = defineStore('biz_class_store', () => {
    
    const sole_prop_biz_class = ref('')
    const update_sole_prop_biz_class = (sole_prop_val) => {
        sole_prop_biz_class.value = sole_prop_val
    }    

    const entity_biz_class = ref('')
    const update_entity_biz_class = (entity_val) => {
        entity_biz_class.value = entity_val
    }    
  
    
    return {entity_biz_class, sole_prop_biz_class } 
    
})
