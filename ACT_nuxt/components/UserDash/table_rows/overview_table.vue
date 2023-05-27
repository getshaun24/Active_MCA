<template>
    

    <span v-for="(value, index) in pagenated_table_data" :key="index">
        
    <tr  class="table_row">                        
    <!-- <td><div :class="row.status_color_class"></div><span class="status_text">{{ row.status }}</span></td> -->
    <td>{{ value.recipient }}</td>
    <td>{{ value.status }}</td>            
    <td>{{ value.request_date }}</td>        
  </tr>

</span>

</template>







<script setup>


    const props = defineProps(['col_num', 'counter_index', 'show_amount'])
    


    const table_data = inject('table_data', 'no data')
    const table_datax = ref(table_data)
    


watch(()=>props.counter_index, (newVal) => {
            console.log('hello')
            pagenated_table_data_meth()

        })



function pagenated_table_data_meth() {
    console.log(props.counter_index)
    console.log(props.show_amount)
    const start = (props.counter_index - 1) * props.show_amount;
    const end = (props.counter_index * props.show_amount) + 1;
    console.log(table_datax.value.slice(start, end))
    return table_datax.value.slice(start, end);
}


 const pagenated_table_data = computed(() => {
    const start = (props.counter_index - 1) * props.show_amount;
    const end = (props.counter_index * props.show_amount);
    return table_datax.value.slice(start, end);
})












</script>










<style>





td{
    text-align: left;
    font-size: 15px;
    line-height: 1.25;
    padding-right:10px;
    padding-left:10px;
    width:calc(100% / v-bind(col_num));
}



.table_row {
    display: flex;
    padding: 12px 0px;
    overflow: visible;
    padding-left:50px;
    border-bottom: #8ccdff 1px solid;
    color: var(--theme-color);
    gap: 25px;
    align-items: left;
    flex-direction:row;
    justify-content: space-evenly;
}

.table_row:hover {
    background-color:#8ccdff0d;
    color: #215cda 
}



@media only screen and (min-width: 0px) and (max-width: 430px) {
    
    
    td{
        font-size: 2vw;
        padding-right:3px;
        padding-left:3px;
    }

    .table_row {
        gap: 5px;
        padding-left:10px;
        padding-right:10px
    }
    
   
    
  
}
@media only screen and (min-width: 430px) and (max-width: 576px) {
    
    
    td{
        font-size: 2vw;
        padding-right:3px;
        padding-left:3px;
    }

        
    .table_row {
        gap: 5px;
        padding-left:10px;
        padding-right:10px
    }
    
    
   
  
}
@media only screen and (min-width: 576px) and (max-width: 768px) {

    
    td{
        font-size: 2vw;
        padding-right:3px;
        padding-left:3px;
    }
    
    .table_row {
        gap: 5px;
        padding-left:20px;
        
    }
    
}
@media only screen and (min-width: 768px) and (max-width: 992px) {
    
    
    td{
        font-size: 1.2vw;
        padding-right:3px;
        padding-left:3px;
    }
   
}
@media only screen and (min-width: 768px) and (max-width: 900px) {
    
    .table_row {
        gap: 5px;
        padding-left:20px;
        padding-right:20px
    }
    
}
@media only screen and (min-width: 900px) and (max-width: 992px) {
    .table_row {
        gap: 5px;
        padding-left:20px;
    }
  
}

@media only screen and (min-width: 992px) and (max-width: 1100px) {
    

    
    .table_row {
        gap: 5px;
        padding-left:20px;
    }
   
    
}
@media only screen and (min-width: 1100px) and (max-width: 1200px) {
        
    .table_row {
        gap: 5px;
        padding-left:20px;
    }

}
    

@media only screen and (min-width: 992px) and (max-width: 1100px) {
    .table_row {
        gap: 5px;
        padding-left:20px;
    }
    
    
}
@media only screen and (min-width: 1100px) and (max-width: 1200px) {
    
  
    
}
@media only screen and (min-width: 1200px) and (max-width: 1400px) {
    
   
    td{
        font-size: 1vw;
    }

        
    .table_row {
        gap: 5px;
        padding-left:20px;
    }
  
}
@media only screen and (min-width: 1400px) and (max-width: 1600px) {
    

    td{
        font-size: 1vw;
    }
    
    .table_row {
        gap: 5px;
        padding-left:20px;
    }

  
    
}
@media only screen and (min-width: 1600px) and (max-width: 2300px) {

    
}
@media only screen and (min-width: 2300px) and (max-width: 5600px) {
    

    
}  












</style>