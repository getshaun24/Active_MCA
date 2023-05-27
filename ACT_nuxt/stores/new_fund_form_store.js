import {ref, computed} from 'vue'
import {defineStore} from 'pinia'

export const form_store = defineStore('form_store', () => {
    
    const user_invest_info_step_1 = ref({
        first_name: '',
        last_name: '',
        email: '',
        phone: ''
    })
    const update_info_step_1 = (first_name, last_name, email, phone) => {   
        user_invest_info_step_1.value.first_name = first_name
        user_invest_info_step_1.value.last_name = last_name
        user_invest_info_step_1.value.email = email
        user_invest_info_step_1.value.phone = phone
    }
    const fund_ID = ref('')
    const update_IDs = (flask_fund_id, invest_ID) => {
        fund_ID.value = flask_fund_id
    }    
    const account_list = ref(null)
    const update_account_list = (acc_list, meth) => {
        if (meth == 'add') {
            account_list.value = acc_list
        } else if (meth == 'remove') {
            account_list.value = null
        }
    }
        
    return {user_invest_info_step_1, update_info_step_1, update_IDs, fund_ID, account_list, update_account_list }
      
})
