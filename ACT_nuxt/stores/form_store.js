import {ref, computed} from 'vue'
import {defineStore} from 'pinia'

export const form_store = defineStore('form_store', () => {
    
    const investment_amount = ref('')
    const update_investment_amount = (invest_am) => {
        investment_amount.value = invest_am
    }    
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
    const investor_ID = ref('')
    const fund_ID = ref('')
    const update_IDs = (flask_investor_id, invest_ID) => {
        investor_ID.value = flask_investor_id
        fund_ID.value = invest_ID
    }    
    const fund_investing_in = ref('')
    const update_fund_investing_in = (page_from) => {
        fund_investing_in.value = page_from
    }    
    const institution_ID = ref('')
    const update_institution_ID = (inst_ID) => {
        institution_ID.value = inst_ID
    }
    const account_list = ref(null)
    const update_account_list = (acc_list, meth) => {
        if (meth == 'add') {
            account_list.value = acc_list
        } else if (meth == 'remove') {
            account_list.value = null
        }
    }
    
    return {investment_amount, update_investment_amount, user_invest_info_step_1, update_info_step_1, update_IDs, investor_ID, fund_ID, update_fund_investing_in, fund_investing_in, account_list, update_account_list, institution_ID, update_institution_ID } 
    
})
