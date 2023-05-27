import {ref, computed} from 'vue'
import {defineStore} from 'pinia'



export const investor_dash_store = defineStore('investor_dash_store', () => {



    const investor_info = ref({
        investor_ID: '',
        first_name: '',
        last_name: '',
        email: '',
    })


    const update_investor_info = (investor_ID, first_name, last_name, email) => {   
        investor_info.value.investor_ID = investor_ID
        investor_info.value.first_name = first_name
        investor_info.value.last_name = last_name
        investor_info.value.email = email
    }




    return {update_investor_info, investor_info } 



  })
  