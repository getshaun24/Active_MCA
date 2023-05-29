<template>
    <div class="container_table">      
        <p style="color:#000">{{ table_name }}</p>
        <table class="table">
            <thead >

                <th class="title_row">
                    <div class="table_sorter">


                        <div class="navigation_menu_table" :class="{hide_elm:isHidden_X}">
                            <div v-for="(key,value,index) in table_buttons" 
                                :key="index" 
                                @click="button_function(key,index)" 
                                :style="[clicked_index===index ? {color:'var(--header_menu_hover)'} : {}, buttonStyles]" 
                                class="navigation_menu_table_item">{{value}}</div>
                        </div>


                        <th class="search_container" :style="{ marginLeft: search_container_margin_left, width: search_container_width }">
                        <div class="search_bar_table" :style="{ marginLeft: search_container_margin_left, width: search_container_width,  Maxwidth: search_bar_table_max_width }">
                          <input v-model="search_query" @input="search_filter" @blur="table_search_blur" @focus="table_search_focus" type="text" placeholder="">
                        </div>
                      </th>

                      
                      <th class="pagenation_container"  :class="{ hide_elm: isHidden_X }">
                        <div class="counter">{{ counter }}</div>
                        <button @click="paginate('left')" :class="{ disabled_left: isDisabledLeft }" class="pagenation_button paginate left"><i></i><i></i></button>
                        <button @click="paginate('right')" :class="{ disabled_right: isDisabledRight }" class="pagenation_button paginate right"><i></i><i></i></button>
                      </th>


                    </div>
                </th>
            </thead>
            <div class="header_row">
                <th v-for="(value, index) in table_headers" :key="index" class="header__item"> 
                        {{ value }}
                </th>
            </div>



                    <ActiveMasterDashMasterTableRowsOverviewTable v-if="table_row_style == 'overview_table'" :button_value="button_value" :col_num="col_num" :counter_index="counter_index" :show_amount="show_amount" :search_query="search_query"/>

               


                <!-- </span> -->
                <tfoot style="border-radius:100px">
                    <tr>
                        <td v-if="show_amount < record_count" class="table_footer_info">Showing {{ show_amount }} items out of {{ record_count }} results found</td>
                        <td v-else class="table_footer_info">Showing {{ record_count }} items out of {{ record_count }} results found</td>
                    </tr>
                </tfoot>
            </table>
        </div>
    </template>
    
    
    
    
    
    <script setup>



        // sleep time expects milliseconds
        function sleep (time) {
          return new Promise((resolve) => setTimeout(resolve, time));
        }



    
    const props = defineProps(['table_name', 'table_headers', 'table_buttons', 'record_count', 'table_row_style'])


    // calculate the col widths
    const col_num = ref(props.table_headers.length)


const search_query = ref('')


// pagenation buttons

const isDisabledLeft = ref(true)
const isDisabledRight = ref(false)



const show_amount = ref(25)
const total_pages = ref(Math.ceil(props.record_count / show_amount.value))
const counter_index = ref(1)
const counter = ref(1 + " / " +  total_pages.value)
 const rowShow = ref(1)


 watch(()=>props.record_count, (newVal) => {
            console.log('hello')
            total_pages.value = Math.ceil(newVal / show_amount.value)
            counter.value = counter_index.value + " / " + total_pages.value;
            console.log(total_pages.value)
        })



function paginate(direction) {

if (direction == 'left' && isDisabledLeft.value == false){
    isDisabledRight.value = false
    if (counter_index.value <= 1){
    isDisabledLeft.value = true
    } else {
        isDisabledLeft.value = false
        counter_index.value -= 1
    } 


} else if (direction == 'right' && isDisabledRight.value == false){
    isDisabledLeft.value = false
    if(counter_index.value == total_pages.value){
    isDisabledRight.value = true
    } else{
    isDisabledRight.value = false
    counter_index.value += 1
}}

counter.value = counter_index.value + " / " + total_pages.value;

}



// button click
const button_value = ref('all')
const clicked_index = ref(0)
function button_function(key, index){
    button_value.value = key
    clicked_index.value = index
}

const clickedButtons = reactive({});
function getButtonColor(index) {
    return index in clickedButtons && clickedButtons[index]
        ? 'blue'
        : 'green';
    }


    const buttonStyles = computed(() => {
        const numKeys = Object.keys(props.table_buttons).length
  return numKeys > 5 
    ? { fontSize: '13px', padding: '6px 10px' } 
    : { fontSize: '16px', padding: '15px 18px' }
});




// search
const isWide = ref(false)
const isHidden_X = ref(false)
const search_container_margin_left = ref('0%')
const search_container_width = ref('100%')
const search_bar_table_max_width = ref('1000px')


// expand the search bar in the table and remove other elements
function table_search_focus(){
    isWide.value = true
    isHidden_X.value = true
    const numKeys = Object.keys(props.table_buttons).length
    search_container_margin_left.value = numKeys === 0 ? '-20%' : String((numKeys + 1) * -4) + '%';
    search_container_width.value = '100%'
    search_bar_table_max_width.value = '1000px'
}


function table_search_blur(){
isWide.value = false
isHidden_X.value = false
search_container_margin_left.value = '0%'
search_container_width.value = '50%'
search_bar_table_max_width.value = '400px'
}



</script>











<style scoped>


.hide_elm{
    visibility: hidden;
}

.container_table {
    margin-right: auto;
    overflow:hidden;
    padding-top:10%;
    padding-bottom:15vh;
    width:100%
}
.table {
    background-color: #fff;
    table-layout: fixed;
    border-bottom-left-radius: 30px;
    border-bottom-right-radius: 30px;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
    filter: drop-shadow(2px 2px 2.5px #00183927);
    display: table;
    width:100%;
}






.navigation_menu_table {
    margin-left:8px;
    display: flex;
}
.navigation_menu_table_item {
    padding: 15px 18px;
    padding-left:0px;
    padding-bottom:12px;
    text-decoration: none;
    color: #deae00aa;
    transition: 0;
    cursor: pointer;
    font-size:16px
}
.navigation_menu_table_item:hover {
    color: var(--header_menu_hover);
}


.table_footer_info {
    padding:20px 60px;
    font-size:15px;
    color:grey
}

.pagenation_button {
    -webkit-appearance: none;
    background: transparent;
    border: 0;
    outline: 0;
}
.paginate i {
    position: absolute;
    width: 25px;
    height: 5px;
    border-radius: 2.5px;
    background:#ddf0ff;
    transition: all 0.15s ease;
    margin-top: -7.5px;
    cursor: pointer;
    transform: translate3d(0, 0, 0);
    -webkit-filter: drop-shadow(0 2px 0px rgba(0, 0, 0, 0.2));
}
.paginate.left {
    right: 58%;
}
.paginate.left i {
    transform-origin: 0% 50%;
    margin-left:-90px
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
.paginate.left[data-state="disabled"] i:first-child {
    transform: translate(-5px, 0) rotate(0deg);
}
.paginate.left[data-state="disabled"] i:last-child {
    transform: translate(-5px, 0) rotate(0deg);
}
.paginate.left[data-state="disabled"]:hover i:first-child {
    transform: translate(-5px, 0) rotate(0deg);
}
.paginate.left[data-state="disabled"]:hover i:last-child {
    transform: translate(-5px, 0) rotate(0deg);
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
    margin-left:-35px
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
.paginate.right[data-state="disabled"] i:first-child {
    transform: translate(5px, 0) rotate(0deg);
}
.paginate.right[data-state="disabled"] i:last-child {
    transform: translate(5px, 0) rotate(0deg);
}
.paginate.right[data-state="disabled"]:hover i:first-child {
    transform: translate(5px, 0) rotate(0deg);
}
.paginate.right[data-state="disabled"]:hover i:last-child {
    transform: translate(5px, 0) rotate(0deg);
}
.paginate[data-state="disabled"] {
    opacity: 0.3;
    cursor: default;
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
    margin-left: -55px;
    top: -6px;
    font-size: 11px;
    color: var(--theme-color);
}
.pagenation_container{
    width:40px;
    position:relative;
    padding-left:30%;
    display:flex;
    justify-content:space-between;
    align-content: center;
    margin-top:5px
}

.title_row{
    border: #8ccdff 2px solid;
    border-top-left-radius:15px;
    border-top-right-radius:15px;
    padding: 6px 0px;
    padding-top:8px;
    white-space: nowrap;
    line-height: 1;
    text-decoration: none;
    cursor: pointer;
    margin-bottom:-3px;
    color: var(--theme-color);
    font-weight: 100;
    box-sizing: content-box;
}
.header_row{
    display: flex;
    padding: 18px 0px;
    padding-left:50px;
    overflow: visible;
    border-bottom: none;
    margin-bottom:0%;
    background-color: rgb(0, 86, 148);
    margin-top:-1.5px;
    gap: 25px;
    align-items: left;
    flex-direction:row;
    justify-content: space-evenly;
}

.header__item {
    text-align: left;
    font-size: 15px;
    line-height: 1.25;
    color: #fff;
    cursor: pointer;
    padding-right:10px;
    padding-left:15px;
    text-decoration: none;
    width:calc(100% / v-bind(col_num))
}



.desc::after {
    content: "▽";
    font-size: 12px;
    padding-left:5px;
}
.asc::after {
    content: "△";
    font-size: 12px;
    padding-left:5px;
}
.table_sorter{
    font-size:20px;
    padding-left:1px; 
    text-align:left; 
    position:relative; 
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.search_container{
    width:100%;
    position:relative;
}
.search_bar_table {
    height: 30px;
    max-width: 500px;
    border-radius: 4px;
}
.search_bar_table input {
    margin-left:45%;
    width: 100px;
    height: 100%;
    border: none;
    background-color:#ddf0ff;
    border-radius: 4px;
    font-size: 15px;
    font-weight: 500;
    padding: 0 20px 0 40px;
    box-shadow: 0 0 0 2px rgba(134, 140, 160, 0.02);
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 56.966 56.966' fill='%23717790c7'%3e%3cpath d='M55.146 51.887L41.588 37.786A22.926 22.926 0 0046.984 23c0-12.682-10.318-23-23-23s-23 10.318-23 23 10.318 23 23 23c4.761 0 9.298-1.436 13.177-4.162l13.661 14.208c.571.593 1.339.92 2.162.92.779 0 1.518-.297 2.079-.837a3.004 3.004 0 00.083-4.242zM23.984 6c9.374 0 17 7.626 17 17s-7.626 17-17 17-17-7.626-17-17 7.626-17 17-17z'/%3e%3c/svg%3e");
    background-size: 14px;
    background-repeat: no-repeat;
    background-position: 16px 48%;
    color:#000;
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
.wide .search_bar_table {
    max-width: 1900px;
    margin-left: -100%;
    transition: 0.4s;
    box-shadow: 0 0 0 1px var(--border-color);
    padding-left: 0;
}





@media only screen and (min-width: 0px) and (max-width: 430px) {
    
    

    
    .header__item {
        font-size: 2vw;
        padding-right:3px;
        padding-left:3px;
    }
    
    .navigation_menu_table_item {
        font-size:1.75vw;
        padding: 12px 10px;
    }
    
    
    

    
    .header_row{
        gap: 5px;
        padding-left:10px;
        padding-right:10px
    }
    

    .search_container {
        display: none !important;
    }
    
    

   
    
    
    .counter {
        margin-left: -45px;
        top: -3px;
        font-size: 10px;
    }
    
    .paginate i {
        width: 20px;
        margin-top:-5px
    }
    
    .paginate.left i {
        margin-left:-70px
    }
    
    
    
    .table_footer_info {
        padding:20px 20px;
        font-size:12px;
    }
    
    .pagenation_container{
        margin-left:-15%;
    }
    .container_table {
    width:106%;
    margin-left:-2%
}
  
}
@media only screen and (min-width: 430px) and (max-width: 576px) {
    
    
    .table_data{
        font-size: 2vw;
        padding-right:3px;
        padding-left:3px;
    }
    
    .header__item {
        font-size: 2vw;
        padding-right:3px;
        padding-left:3px;
    }
    
    .navigation_menu_table_item {
        font-size:1.75vw;
        padding: 12px 10px;
    }
    
    

    
    .header_row{
        gap: 5px;
        padding-left:10px;
        padding-right:10px
    }
    

    .search_container {
        display: none !important;
    }
    

    
    
    .counter {
        margin-left: -45px;
        top: -3px;
        font-size: 10px;
    }
    
    .paginate i {
        width: 20px;
        margin-top:-5px
    }
    
    .paginate.left i {
        margin-left:-70px
    }
    
    
    
    .table_footer_info {
        padding:20px 20px;
        font-size:12px;
    }
    
    .pagenation_container{
        margin-left:-15%;
    }
    .container_table {
    width:106%
}
  
}
@media only screen and (min-width: 576px) and (max-width: 768px) {
    .table {
        width: 100%;
    }
    
    
    .header__item {
        font-size: 2vw;
        padding-right:3px;
        padding-left:3px;
    }
    
    .navigation_menu_table_item {
        font-size:1.6vw;
        padding: 12px 10px;
    }
    

    
    .table_footer_info {
        padding:20px 20px;
        font-size:15px;
    }
    
    
    .counter {
        margin-left: -45px;
        top: -3px;
        font-size: 10px;
    }
    
    .paginate i {
        width: 20px;
        margin-top:-5px
    }
    
    .paginate.left i {
        margin-left:-70px
    }
    
    .header_row{
        gap: 5px;
        padding-left:20px;
        
    }
    
  
    
    
    .search_bar_table {
        margin-left:-40%;
    }
    
    .search_bar_table input {
        width:25px;
    }
    
    
    .pagenation_container{
        margin-left:-12%;
    }
    
    
    
}
@media only screen and (min-width: 768px) and (max-width: 992px) {
    

    
    .header__item {
        font-size: 1.2vw;
        padding-right:3px;
        padding-left:3px;
    }
    
    .navigation_menu_table_item {
        font-size:1.25vw;
        padding: 12px 10px;
    }
    
    
    

    
    
    .counter {
        margin-left: -45px;
        top: -3px;
        font-size: 10px;
    }
    
    .paginate i {
        width: 20px;
        margin-top:-5px
    }
    
    .paginate.left i {
        margin-left:-70px
    }
    
    
    .search_bar_table {
        margin-left:-80%;
    }
    
    .search_bar_table input {
        width:25px;
        margin-left:65%
    }
    
    
    .pagenation_container{
        margin-left:-12%;
    }
    
    
}
@media only screen and (min-width: 768px) and (max-width: 900px) {
    
    
    .table{
        width:75%
    }
    
    .header_row{
        gap: 5px;
        padding-left:20px;
        padding-right:20px
    }
    
 
    
}
@media only screen and (min-width: 900px) and (max-width: 992px) {
    
    .table {
        width: 80%;
    }
    
    
    .header_row{
        gap: 5px;
        padding-left:20px;
    }
    

    
}
@media only screen and (min-width: 900px) and (max-width: 945px) {
    .search_bar_table {
        margin-left:5%;
        margin-right:10%
    }
}
@media only screen and (min-width: 945px) and (max-width: 992px) {
    .search_bar_table {
        margin-left:25%;
        margin-right:10%
    }
}
@media only screen and (min-width: 992px) and (max-width: 1200px) {
    
    
    
    .header__item {
        font-size: 1vw;
        padding-right:3px;
        padding-left:3px;
    }
    
    .navigation_menu_table_item {
        font-size:1.1vw;
        padding: 12px 15px;
    }
    
    
    

    
    
    
}
@media only screen and (min-width: 992px) and (max-width: 1100px) {
    
    .table{
        width:100%
    }
    .header_row{
        gap: 5px;
        padding-left:20px;
    }
    
    
    .search_bar_table {
        margin-left:20%;
    }
    
    .search_bar_table input{
        width: 50px;
    }
    
    
    
}
@media only screen and (min-width: 1100px) and (max-width: 1200px) {
    
    .table{
        width:100%
    }
    .header_row{
        gap: 5px;
        padding-left:20px;
    }
    
    
    
    .search_bar_table {
        margin-left:50%;
        width:100%;
    }
    
    
    
}
@media only screen and (min-width: 1200px) and (max-width: 1400px) {
    
    .table{
        width:100%
    }
    
    .header__item {
        font-size: 1vw;
    }
    
    .navigation_menu_table_item {
        font-size:1.1vw;
        margin-left:20px
    }
    

    .header_row{
        gap: 5px;
        padding-left:20px;
    }
    

    .search_bar_table input {
        width:70%;
    }
    
    
}
@media only screen and (min-width: 1400px) and (max-width: 1600px) {
    
    .table{
        width:100%
    }

    
    .header__item {
        font-size: 1vw;
    }
    
    .navigation_menu_table_item {
        font-size:1.1vw;
        margin-left:20px
    }
    
    
    .header_row{
        gap: 5px;
        padding-left:20px;
    }
    
    .search_bar_table input {
        width:70%;
    }
    
}
@media only screen and (min-width: 1600px) and (max-width: 2300px) {
    
    .table{
        width:100%
    }
    
    .search_bar_table input {
        width:80%;
    }
    
    
}
@media only screen and (min-width: 2300px) and (max-width: 5600px) {
    
    .table{
        width:100%
    }
    
    .search_bar_table input {
        width:80%;
    }
    
    
} 





.table {
    background-color: var(--table-background) !important;
}

.table_title{
    color:var(--theme-txt-color) !important;
}

.navigation_menu_table_item {
    color: var(--table-sorter-color) !important;
}
.navigation_menu_table_item:hover {
    color: var(--table-sorter-color-hover) !important;
}

.counter {
    color:var(--theme-txt-color) !important;
}

.title_row{
    border: var(--table-header-row-background) 2px solid !important;
    color:var(--theme-txt-color) !important;
    background-color:var(--table-header-row-background) !important;
}

.table_row {
    color: var(--theme-color) !important;
}

.search_bar_table input::-moz-placeholder {
    color: var(--inactive-color) !important;
}
.search_bar_table input:-ms-input-placeholder {
    color: var(--inactive-color) !important;
}
.search_bar_table input::placeholder {
    color: var(--inactive-color) !important;
}

.wide .search_bar_table {
    box-shadow: 0 0 0 1px var(--border-color) !important;
}

</style>





















  <!-- ---------------------- minified version ---------------------- -->



<!-- 
<template><div class="container_table"><p style="color:#000">{{table_name}}</p><table class="table"><thead><th class="title_row"><div class="table_sorter"><div class="navigation_menu_table" :class="{hide_elm:isHidden_X}"><div v-for="(key,value,index) in table_buttons" :key="index" @click="button_function(key,index)" :style="clicked_index===index?{color:'var(--header_menu_hover)'}:{}" class="navigation_menu_table_item">{{value}}</div></div><th class="search_container" :style="{marginLeft:search_container_margin_left,width:search_container_width}"><div class="search_bar_table" :style="{marginLeft:search_container_margin_left,width:search_container_width,Maxwidth:search_bar_table_max_width}"><input v-model="search_query" @input="search_filter" @blur="table_search_blur" @focus="table_search_focus" type="text" placeholder=""></div></th><th class="pagenation_container" :class="{hide_elm:isHidden_X}"><div class="counter">{{counter}}</div><button @click="paginate('left')" :class="{disabled_left:isDisabledLeft}" class="pagenation_button paginate left"><i></i><i></i></button><button @click="paginate('right')" :class="{disabled_right:isDisabledRight}" class="pagenation_button paginate right"><i></i><i></i></button></th></div></th></thead><div class="header_row"><th v-for="(value,index) in table_headers" :key="index" class="header__item">{{value}}</th></div><UserDashTableRowsOverviewTable v-if="table_row_style=='overview_table'" :button_value="button_value" :col_num="col_num" :counter_index="counter_index" :show_amount="show_amount" :search_query="search_query"/><UserDashTableRowsPaymentsTable v-if="table_row_style=='payments_table'" :button_value="button_value" :col_num="col_num" :counter_index="counter_index" :show_amount="show_amount" :search_query="search_query"/><UserDashTableRowsNotificationsTable v-if="table_row_style=='notifications_table'" :button_value="button_value" :col_num="col_num" :counter_index="counter_index" :show_amount="show_amount" :search_query="search_query"/><tfoot style="border-radius:100px"><tr><td v-if="show_amount<record_count" class="table_footer_info">Showing {{show_amount}} items out of {{record_count}} results found</td><td v-else class="table_footer_info">Showing {{record_count}} items out of {{record_count}} results found</td></tr></tfoot></table></div></template>



<script setup>
function sleep(t){return new Promise(r=>setTimeout(r,t))}
const props=defineProps(['table_name','table_headers','table_buttons','record_count','table_row_style'])
const col_num=ref(props.table_headers.length),search_query=ref(''),isDisabledLeft=ref(true),isDisabledRight=ref(false),show_amount=ref(25),total_pages=ref(Math.ceil(props.record_count/show_amount.value)),counter_index=ref(1),counter=ref(1+" / "+total_pages.value),rowShow=ref(1)
watch(()=>props.record_count,(v)=>{total_pages.value=Math.ceil(v/show_amount.value),counter.value=counter_index.value+" / "+total_pages.value})
function paginate(d){if('left'==d&&false==isDisabledLeft.value){isDisabledRight.value=false,counter_index.value<=1?isDisabledLeft.value=true:(isDisabledLeft.value=false,counter_index.value-=1)}else if('right'==d&&false==isDisabledRight.value){isDisabledLeft.value=false,counter_index.value==total_pages.value?isDisabledRight.value=true:(isDisabledRight.value=false,counter_index.value+=1)}counter.value=counter_index.value+" / "+total_pages.value}
const button_value=ref('all'),clicked_index=ref(0)
function button_function(k,i){button_value.value=k,clicked_index.value=i}
const clickedButtons=reactive({})
function getButtonColor(i){return i in clickedButtons&&clickedButtons[i]?'blue':'green'}
const isWide=ref(false),isHidden_X=ref(false),search_container_margin_left=ref('0%'),search_container_width=ref('100%'),search_bar_table_max_width=ref('400px')
function table_search_focus(){isWide.value=true,isHidden_X.value=true,search_container_margin_left.value=5===0?0:(5+1)*-4+'%',search_container_width.value='100%',search_bar_table_max_width.value='1000px'}
function table_search_blur(){isWide.value=false,isHidden_X.value=false,search_container_margin_left.value='0%',search_container_width.value='100%',search_bar_table_max_width.value='400px'}
</script>



<style scoped>



.navigation_menu_table {
    margin-left:8px;
    display: flex;
}
.navigation_menu_table_item {
    padding: 15px 18px;
    padding-left:0px;
    padding-bottom:12px;
    text-decoration: none;
    color: #deae00aa;
    transition: 0;
    cursor: pointer;
    font-size:16px
}
.navigation_menu_table_item:hover {
    color: var(--header_menu_hover);
}



</style>
 -->
