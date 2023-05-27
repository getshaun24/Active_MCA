<template>
    



    <div class="container_table">

{{ result }}
                  <table class="table" id="myTable">
                    <thead class="title_row" :class="{ wide: isWide }">


                        <th class="table_buttons" :class="{ hide_elm: isHiddenn }">
                            <span @click="button_filter(item.search_term)" v-for="item in table_buttons" class="navigation_menu_table">{{ item.btn }}</span>
                      </th>



                      <th class="search_container" :style="{ marginLeft: search_container_margin_left, width: search_container_width }">
                        <div class="search_bar_table" :style="{ marginLeft: search_container_margin_left, width: search_container_width,  Maxwidth: search_bar_table_max_width }">
                          <input @input="search_filter" @blur="table_search_blur" @focus="table_search_focus" type="text" placeholder="">
                        </div>
                      </th>

                      
                      <th class="pagenation_container" :class="{ hide_elm: isHiddenn }">
                        <div class="counter">{{ counter }}</div>
                        <button @click="slide(-1, 'left')" :class="{ disabled_left: isDisabledLeft }" class="pagenation_button paginate left"><i></i><i></i></button>
                        <button @click="slide(1, 'right')" :class="{ disabled_right: isDisabledRight }" class="pagenation_button paginate right"><i></i><i></i></button>
                      </th>

                    </thead>







                    <tr class="header_row">
                        <th @click="sortBy(item.col)" v-for="item in header_titles" class="header__item">{{ item.title }}</th>
                    </tr>

    
                    <template  v-for="item in table_data">
                        <template v-if="(item.isHidden == false)">
                        <tr class="table-row">                        
                        <td><img class="table_img" :src="item.user_img">
                            <span class="table_name">{{ item.user_name }}<br><span class="table_company">{{ item.user_company }}</span></span></td>
                        <td><div :class="item.status_color_class"></div><span class="status_text">{{ item.status }}</span></td>
                        <td>{{ item.date }}</td>
                        <td>{{ item.offer }}</td>            
                        <td>...</td>
                      </tr>
                    </template>
                </template>
                    

                      <tfoot style="border-radius:100px">
                        <tr>
                          <td>Showing xxx items out of {{ table_data.length }} results found</td>
                        </tr>
                      </tfoot>





                  </table>
                </div>



</template>


<script setup>

import { ref, reactive } from 'vue'
import { useDateFormat, useTimeAgo, useArrayMap } from '@vueuse/core'

import profile_image from "~/assets/content/ACT_dashboard/shaun_profile.jpg"


const isWide = ref(false)
const isHiddenn = ref(false)
const search_container_margin_left = ref('0%')
const search_container_width = ref('40%')
const search_bar_table_max_width = ref('400px')


// expand the search bar in the table and remove other elements
function table_search_focus(){
    isWide.value = true
    isHiddenn.value = true
    search_container_margin_left.value = '-70%'
    search_container_width.value = '100%'
    search_bar_table_max_width.value = '1000px'
}


function table_search_blur(){
isWide.value = false
isHiddenn.value = false
search_container_margin_left.value = '0%'
search_container_width.value = '40%'
search_bar_table_max_width.value = '400px'
}




const reverse = ref(false)



function sortBy (col) {

    if (col == 'date'){
    
    table_data.forEach((item, index) => {
    const new_date_var = String(new Date(item.date).getTime());
    //const new_date_var = useDateFormat(item.date, 'YY/M/D hhmm');
    item.date = new_date_var;
    })
    
 
    if (reverse.value == false){
        reverse.value = true
    table_data.value = table_data.sort((a, b) => a['date'].localeCompare(b['date']))
    table_data.forEach((item, index) => {
   item.date = String(useDateFormat(new Date(Number(item.date)), "M/D/YY hh:mm").value);
    //item.date = useDateFormat(item.date, "M/D/YY hh:mm").value;
    })
    } else {
        table_data.value = table_data.sort((a, b) => b['date'].localeCompare(a['date']))
        table_data.forEach((item, index) => {
        item.date = String(useDateFormat(new Date(Number(item.date)), "M/D/YY hh:mm").value);
        //item.date = useDateFormat(item.date, "M/D/YY hh:mm").value;
        reverse.value = false
    })} }
    else{
    if (reverse.value == false){
        table_data.value = table_data.sort((a, b) => a[col].localeCompare(b[col]))
        reverse.value = true
        } else {
            table_data.value = table_data.sort((a, b) => b[col].localeCompare(a[col]))
            reverse.value = false
        }
        }
    };






function search_filter(event) {
  
    const searched_term = (event.target.value).toLowerCase()
 //   const trs = document.getElementsByTagName("tr");  


    table_data.forEach((item, index) => {
      const text = item.user_name.toLowerCase()
      const text1 = item.user_company.toLowerCase()
      const text2 = item.status.toLowerCase()
      const text3 = item.date.toLowerCase()
      const text4 = item.offer.toLowerCase()


      if (text.includes(searched_term) == true || text1.includes(searched_term) == true || text2.includes(searched_term) == true || text3.includes(searched_term) == true || text4.includes(searched_term) == true){
    //    trs[index + 1].style.display = 'flex'
             item.isHidden = false



      }
      else{
   //     trs[index + 1].style.display = 'none'
            item.isHidden = true
      }
    })
      };






      function button_filter(button) {
  


  table_data.forEach((item, index) => {
    const text = item.status

    if (text.includes(button) == true){
        item.isHidden = false
    }
    else{
        item.isHidden = true
    }
  })
    };






const header_titles = ref([{title:'Name', col:'user_name'}, {title:'Status', col:'status'}, {title:'Date', col:'date'}, {title:'Offer', col:'offer'}, {title:'Actions', col:''}])

const table_buttons = ref([{btn:'All', search_term:''}, {btn:'Discordant', search_term:'No Agreement Reached'}, {btn:'Accepted', search_term:'Deal Accepted'}, {btn:'Settled', search_term:"Settled"}, {btn:'Awaiting Reply', search_term:"Waiting Reply" }])

const table_data = reactive([

    {user_img:profile_image, user_name:'Shaun Cohen', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'Heidi P', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'Johnny Depp', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Settled', status_color_class:'status_color_blue', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'Jon', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'12/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Settled', status_color_class:'status_color_blue', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'5/25/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'Naif', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'8/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Settled', status_color_class:'status_color_blue', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'Heidi', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'Shaun Cohen', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'Heidi P', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'Johnny Depp', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Settled', status_color_class:'status_color_blue', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'Jon', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'12/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Settled', status_color_class:'status_color_blue', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'5/25/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'Naif', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'8/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Settled', status_color_class:'status_color_blue', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'Heidi', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'Shaun Cohen', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'Heidi P', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'Johnny Depp', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Settled', status_color_class:'status_color_blue', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'Jon', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'12/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Settled', status_color_class:'status_color_blue', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'5/25/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'Naif', user_company:'company xyz', status:'Waiting Reply', status_color_class:'status_color_orange', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'8/24/22 12:25', offer:'$3,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Deal Accepted', status_color_class:'status_color_green', date:'11/24/22 12:23', offer:'$1,000', isHidden:false},
    {user_img:profile_image, user_name:'xxxx', user_company:'company xyz', status:'Settled', status_color_class:'status_color_blue', date:'11/24/24 12:24', offer:'$2,000', isHidden:false},
    {user_img:profile_image, user_name:'Heidi', user_company:'company xyz', status:'No Agreement Reached', status_color_class:'status_color_purple', date:'11/24/22 12:25', offer:'$3,000', isHidden:false},
  
])




// pagenation buttons

const isDisabledLeft = ref(true)
const isDisabledRight = ref(false)

const counter = ref(null)

const show_amount = 25
const index = ref(0)
 const total_pages = ref(Math.ceil(table_data.length / show_amount))
 const rowShow = ref(0)

function slide(offset, lr) {



    if (lr == 'left' && isDisabledLeft.value != true){
        rowShow.value -= show_amount
    } else if (lr == 'right' && isDisabledRight.value != true){
        rowShow.value += show_amount
    }

    index.value = Math.min(Math.max(index.value + offset, 0), total_pages.value - 1);

    counter.value = index.value + 1 + " / " + total_pages.value;

    if (index.value == 0){
        isDisabledLeft.value = true
     } else {
        isDisabledLeft.value = false
     } 
     if(index.value == total_pages.value - 1){
        isDisabledRight.value = true
    } else{
        isDisabledRight.value = false
    }

    table_data.forEach((item, index) => {
    if (index >= rowShow.value && index < rowShow.value + show_amount ){
        item.isHidden = false
    }
    else{
        item.isHidden = true
    }
  })


}

slide(0);






</script>




<style scoped>


.hide_elm{
    visibility: hidden;
}

.navigation_menu_table {
    padding: 12px 30px;
    padding-bottom: 19px;
    text-decoration: none;
    color: #deae00;
    transition: 0;
    cursor: pointer;
    font-size: 16px;
}
.navigation_menu_table:first-child {
    margin-left: 25px;
}
.navigation_menu_table:hover {
    color: var(--header_menu_hover);
    font-weight: 700;
}
.table_img {
    width: 50px;
    height: 50px;
    border-radius: 100%;
    position: relative;
}
.table_name {
    margin-left: 10px;
    position: absolute;
    max-width: 170px;
    font-size: 15px;
    word-wrap: break-word;
}
.table_company {
    margin-left: 0;
    margin-top: 4px;
    position: relative;
    max-width: 100px;
    font-size: 13px;
    color: rgba(128, 128, 128, 0.683);
    line-height: 1;
}
.status_color_orange {
    width: 10px;
    height: 10px;
    background-color: orange;
    border-radius: 100%;
}
.status_color_green {
    width: 10px;
    height: 10px;
    background-color: green;
    border-radius: 100%;
}
.status_color_purple {
    width: 10px;
    height: 10px;
    background-color: purple;
    border-radius: 100%;
}

.status_color_blue {
    width: 10px;
    height: 10px;
    background-color: blue;
    border-radius: 100%;
}
.status_text {
    margin-left: 22px;
    margin-top: -13.5px;
    position: absolute;
}
tfoot tr td {
    padding: 20px 60px;
    font-size: 15px;
    color: grey;
}
tfoot tr td {
    padding: 20px 60px;
    font-size: 15px;
    color: grey;
}

table {
    border-collapse: collapse;
    border-spacing: 0;
}
* {
    outline: 0;
    box-sizing: border-box;
    font-family: Haffer, sans-serif !important;
}
img {
    max-width: 100%;
}
.profile-img {
    border: 2px solid var(--theme-bg-color);
    border-radius: 100%;
}
.profile_menu {
    width: 100%;
    height: 100%;
    padding: 5%;
    position: relative;
    -webkit-backdrop-filter: blur(20px);
    backdrop-filter: blur(20px);
    background-color: var(--background_overlay);
    border: #deae0040 1px solid;
}
.header {
    display: flex;
    align-items: center;
    flex-shrink: 0;
    height: 80px;
    width: 100%;
    border-bottom: 1px solid var(--border-color);
    padding: 0 30px;
    white-space: nowrap;
}
@media screen and (max-width: 480px) {
    .header {
        padding: 0 16px;
    }
}
.header-menu {
    display: flex;
    align-items: center;
}
.is-active {
    color: var(--header_menu_hover) !important;
    border-bottom: 3.5px solid var(--header_menu_hover) !important;
}
.navigation_menu {
    padding: 20px 30px;
    padding-bottom: 16px;
    text-decoration: none;
    color: var(--inactive-color);
    border-bottom: 2px solid transparent;
    transition: 0;
    cursor: pointer;
}
.navigation_menu:hover {
    color: var(--header_menu_hover);
    font-weight: 700;
}
.search_bar_header {
    height: 40px;
    display: flex;
    width: 100%;
    max-width: 400px;
    padding-left: 16px;
    border-radius: 4px;
    margin-left: 5%;
}
.search_bar_header input {
    width: 100%;
    height: 100%;
    border: none;
    background-color: var(--search-bg);
    border-radius: 4px;
    font-size: 15px;
    font-weight: 500;
    padding: 0 20px 0 40px;
    box-shadow: 0 0 0 2px rgba(134, 140, 160, 0.02);
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 56.966 56.966' fill='%23717790c7'%3e%3cpath d='M55.146 51.887L41.588 37.786A22.926 22.926 0 0046.984 23c0-12.682-10.318-23-23-23s-23 10.318-23 23 10.318 23 23 23c4.761 0 9.298-1.436 13.177-4.162l13.661 14.208c.571.593 1.339.92 2.162.92.779 0 1.518-.297 2.079-.837a3.004 3.004 0 00.083-4.242zM23.984 6c9.374 0 17 7.626 17 17s-7.626 17-17 17-17-7.626-17-17 7.626-17 17-17z'/%3e%3c/svg%3e");
    background-size: 14px;
    background-repeat: no-repeat;
    background-position: 16px 48%;
    color: var(--theme-color);
}
.search_bar_header input::-moz-placeholder {
    color: rgba(175, 175, 175, 1);
    font-size: 15px;
    font-weight: 500;
}
.search_bar_header input:-ms-input-placeholder {
    color: rgba(175, 175, 175, 1);
    font-size: 15px;
    font-weight: 500;
}
.search_bar_header input::placeholder {
    color: rgba(175, 175, 175, 1);
    font-size: 15px;
    font-weight: 500;
}
.header-profile {
    display: flex;
    align-items: center;
    padding: 0 16px 0 40px;
    margin-left: auto;
    flex-shrink: 0;
    margin-right: 2.5%;
}
.profile-img {
    width: 32px;
    height: 32px;
    -o-object-fit: cover;
    object-fit: cover;
    border: 2px solid #198de6;
    margin-left: 22px;
    border-radius: 100%;
}
.body_container {
    display: flex;
    flex-grow: 1;
    overflow: hidden;
}
.navigation_header {
    display: flex;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
    height: 58px;
    flex-shrink: 0;
}
.navigation_header .header-menu {
    margin-left: 150px;
}
@media screen and (max-width: 1055px) {
    .navigation_header .header-menu {
        margin: auto;
    }
}
.navigation_header .header-menu a {
    padding: 20px 24px;
}

#myInput,
#myInput_1 {
    background-color: #ddf0ff;
    color: #000;
}
input:focus {
    outline: 0;
}
.container_table {
    margin-right: auto;
    margin-left: auto;
    overflow: visible;
    padding-top: 5%;
    padding-bottom: 15vh;
}
table {
    width: 95%;
    overflow: visible;
    min-width: 600px;
    background-color: #fff;
    margin-right: auto;
    margin-left: auto;
    border-bottom-left-radius: 30px;
    border-bottom-right-radius: 30px;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
    filter: drop-shadow(2px 2px 2.5px #00183927);
}
.title_row {
    border: #8ccdff 1px solid;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
    width: 100%;
    padding: 15px 17px;
    white-space: nowrap;
    line-height: 1;
    text-decoration: none;
    cursor: pointer;
    display: inline-block;
    margin-bottom: -3px;
    color: var(--theme-color) !important;
    font-weight: 100;
}

.header_row {
    display: flex;
    width: 100%;
    padding: 18px 25px;
    padding-left: 60px;
    overflow: visible;
    border-bottom: none;
    margin-bottom: 0;
    background-color: #ddf0ff !important;
    margin-top: 0;
    gap: 25px;
    align-items: center;
    flex-direction: row;
    justify-content: space-evenly;
}
.table-row {
    display: flex;
    width: 100%;
    padding: 20px 25px;
    padding-left: 60px;
    overflow: visible;
    border-bottom: #8ccdff 1px solid;
    color: var(--theme-color);
    justify-content: space-evenly;
    gap: 25px;
    align-items: center;
    flex-direction: row;
}
.table-row:hover {
    background-color: #f5faff;
    color: var(--hover_text_color) !important;
}
td {
    text-align: left;
    font-size: 15px;
    line-height: 1.25;
    padding-right: 10px;
    padding-left: 10px;
    min-width: 150px;
}
.header__item {
    text-align: left;
    font-size: 15px;
    line-height: 1.25;
    color: #000;
    text-decoration: none;
    cursor: pointer;
    padding-right: 10px;
    padding-left: 10px;
    min-width: 150px;
}
table tr td:nth-child(1) {
    min-width: 225px;
    flex-grow: 1.5;
    flex-shrink: 0;
}
table tr td:nth-child(2) {
    min-width: 225px;
    flex-grow: 1.5;
    flex-shrink: 0;
}
table tr td:nth-child(3) {
    flex-grow: 1;
    flex-shrink: 3;
}
table tr td:nth-child(4) {
    flex-grow: 1;
    flex-shrink: 3;
}
table tr td:nth-child(5) {
    min-width: 50px;
    flex-grow: 0;
    flex-shrink: 10;
}
.header__item:nth-child(1) {
    min-width: 225px;
    flex-grow: 1.5;
    flex-shrink: 0;
}
.header__item:nth-child(2) {
    min-width: 225px;
    flex-grow: 1.5;
    flex-shrink: 0;
}
.header__item:nth-child(3) {
    flex-grow: 1;
    flex-shrink: 3;
}
.header__item:nth-child(4) {
    flex-grow: 1;
    flex-shrink: 3;
}
.header__item:nth-child(5) {
    min-width: 50px;
    flex-grow: 0;
    flex-shrink: 10;
}
.pagenation_button {
    -webkit-appearance: none;
    background: 0 0;
    border: 0;
    outline: 0;
}
.paginate i {
    position: absolute;
    width: 25px;
    height: 5px;
    border-radius: 2.5px;
    background: #ddf0ff;
    transition: all 0.15s ease;
    margin-top: -7.5px;
    cursor: pointer;
    transform: translate3d(0, 0, 0);
    -webkit-filter: drop-shadow(0 2px 0 rgba(0, 0, 0, 0.2));
}
.paginate.left {
    right: 58%;
}
.paginate.left i {
    transform-origin: 0 50%;
    margin-left: -130px;
}
.paginate.left i:first-child {
    transform: translate(0, -1px) rotate(40deg);
}
.paginate.left i:last-child {
    transform: translate(0, 1px) rotate(-40deg);
}
.paginate.left:hover i:first-child {
    transform: translate(0, -1px) rotate(30deg);
}
.paginate.left:hover i:last-child {
    transform: translate(0, 1px) rotate(-30deg);
}
.paginate.left:active i:first-child {
    transform: translate(1px, -1px) rotate(25deg);
}
.paginate.left:active i:last-child {
    transform: translate(1px, 1px) rotate(-25deg);
}
.disabled_left i:first-child {
    transform: translate(-5px, 0) rotate(0) !important;
}
.disabled_left i:last-child {
    transform: translate(-5px, 0) rotate(0) !important;
}
.disabled_left:hover i:first-child {
    transform: translate(-5px, 0) rotate(0) !important;
}
.disabled_left:hover i:last-child {
    transform: translate(-5px, 0) rotate(0) !important;
}
.paginate.right {
    left: 58%;
}
.paginate.right i {
    transform-origin: 100% 50%;
    margin-left: -50px;
}
.paginate.right i:first-child {
    transform: translate(0, 1px) rotate(40deg);
}
.paginate.right i:last-child {
    transform: translate(0, -1px) rotate(-40deg);
}
.paginate.right:hover i:first-child {
    transform: translate(0, 1px) rotate(30deg);
}
.paginate.right:hover i:last-child {
    transform: translate(0, -1px) rotate(-30deg);
}
.paginate.right:active i:first-child {
    transform: translate(1px, 1px) rotate(25deg);
}
.paginate.right:active i:last-child {
    transform: translate(1px, -1px) rotate(-25deg);
}
.disabled_right i:first-child {
    transform: translate(5px, 0) rotate(0) !important;
}
 .disabled_right i:last-child {
    transform: translate(5px, 0) rotate(0) !important;
}
.disabled_right:hover i:first-child {
    transform: translate(5px, 0) rotate(0) !important;
}
.disabled_right:hover i:last-child {
    transform: translate(5px, 0) rotate(0) !important;
}
.disabled_right {
    opacity: 0.3 !important;
    cursor: default !important;
}
.counter {
    text-align: center;
    position: absolute;
    width: 100%;
    top: 11px;
    font-size: 15px;
    color: var(--theme-color);
    margin-left: -81px;
}
.pagenation_container {
    width: 100%;
    position: relative;
    z-index: 100;
}
.table_buttons {
    font-size: 20px;
    padding-left: 1px;
    width: 60%;
    text-align: left;
    position: relative;
    line-height: 1;
}
.search_container {
    width: 40%;
    position: relative;
    margin-right: 50%;
    transition: all 1s ease;
}
.search_bar_table {
    height: 30px;
    display: flex;
    width: 50%;
    max-width: 400px;
    padding-left: 16px;
    border-radius: 4px;
    margin-left: 5%;
    transition: all 1s ease;
}
.search_bar_table input {
    width: 100%;
    height: 100%;
    border: none;
    background-color: var(--search-bg);
    border-radius: 4px;
    font-size: 15px;
    font-weight: 500;
    padding: 0 20px 0 40px;
    box-shadow: 0 0 0 2px rgba(134, 140, 160, 0.02);
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 56.966 56.966' fill='%23717790c7'%3e%3cpath d='M55.146 51.887L41.588 37.786A22.926 22.926 0 0046.984 23c0-12.682-10.318-23-23-23s-23 10.318-23 23 10.318 23 23 23c4.761 0 9.298-1.436 13.177-4.162l13.661 14.208c.571.593 1.339.92 2.162.92.779 0 1.518-.297 2.079-.837a3.004 3.004 0 00.083-4.242zM23.984 6c9.374 0 17 7.626 17 17s-7.626 17-17 17-17-7.626-17-17 7.626-17 17-17z'/%3e%3c/svg%3e");
    background-size: 14px;
    background-repeat: no-repeat;
    background-position: 16px 48%;
    color: var(--theme-color);
    transition: all 1s ease;
}
.search_bar_table input::-moz-placeholder {
    color: var(--inactive-color);
    font-size: 15px;
    font-weight: 500;
}
.search_bar_table input:-ms-input-placeholder {
    color: var(--inactive-color);
    font-size: 15px;
    font-weight: 500;
}
.search_bar_table input::placeholder {
    color: var(--inactive-color);
    font-size: 15px;
    font-weight: 500;
}




</style>