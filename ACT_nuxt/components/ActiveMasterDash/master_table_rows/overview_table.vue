<template>
    

    <span v-for="(value, index) in pagenated_table_data" :key="index">
        
    <tr  class="table_row">                        
    <!-- <td><div :class="row.status_color_class"></div><span class="status_text">{{ row.status }}</span></td> -->
    <td>{{ value.funder_dba }}</td>
    <td>{{ value.biz_email }}</td>            
    <td>{{ value.phone }}</td>        
  </tr>

</span>

</template>






<script setup>


    const props = defineProps(['col_num', 'counter_index', 'show_amount', 'button_value', 'search_query'])
    


    const table_data = inject('table_data', [])
    const table_datax = ref(table_data)
    

        const updated_button_value = ref(props.button_value)
        watch(()=>props.button_value, (newVal) => {
            updated_button_value.value = newVal

        })


watch(()=>props.counter_index, (newVal) => {
            pagenated_table_data_meth()
        })

        
function pagenated_table_data_meth() {
    const start = (props.counter_index - 1) * props.show_amount;
    const end = (props.counter_index * props.show_amount) + 1;
    return search_filtered.value.slice(start, end);
}


 const pagenated_table_data = computed(() => {
    const start = (props.counter_index - 1) * props.show_amount;
    const end = (props.counter_index * props.show_amount);
    return search_filtered.value.slice(start, end);
})



// ----------------- search --------------


watch(()=>props.search_query, (newVal) => {
            pagenated_table_data_meth()
        })




const search_filtered = computed(() => {
  if (!props.search_query) return table_datax.value;

  return table_datax.value.filter(person => {
    const queryLower = props.search_query.toLowerCase();
    
    return Object.values(person).some((value) => {
      if (value === null) return false;
      const valueString = value.toString().toLowerCase();
      return valueString.includes(queryLower);
    });
  });
});









//--------------- function ------

const format_underscore = (str) => {
  return str.split('_').map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
};


const statusColor = (status) => {
  switch (status) {
    case 'requested':
      return '#000';
    case 'incoming':
      return '#0373fc';
    case 'settlement_reached':
      return '#6e6ed3';
    case 'open':
      return 'green';
    case 'expiring_soon':
      return 'orange';
    case 'expired':
      return 'red';
    default:
      return 'inherit';
  }
};


const extractDate = (datetimeString) => {
  const date = new Date(datetimeString);
  return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;
};




// ----------------- transition --------------

const main_tansition = ref(null);
function transition_and_route(route_to) {
    navigateTo(route_to)
    // main_tansition.value.animation_and_route(route_to);
}


</script>










<style scoped>


.the_row{
    cursor: pointer !important;
}


td{
    text-align: left;
    font-size: 15px;
    line-height: 1.25;
    padding-right:10px;
    padding-left:10px;
    width:calc(100% / v-bind(col_num));
    cursor: pointer !important;
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