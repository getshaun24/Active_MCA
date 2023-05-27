<template>
    

<div class="menu_grid">

<div class="menu_item">Home</div>
<div class="menu_item">Active Advances</div>
<div class="menu_item">All Advances</div>
<div class="menu_item">Merchants</div>
<div class="menu_item">Syndicators</div>
<div class="menu_item">ISOs</div>
<div class="menu_item">Team</div>
<div class="menu_item">Settings</div>

</div>

</template>


<style scoped>

.menu_grid{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(4, 1fr);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    width:80%;
    margin-left:10%;
    margin-top:10%;
    z-index:1000;

}
.menu_item{
    color:var(--theme-txt-color);
    font-size:50px;
    cursor: pointer;
}

.menu_item:hover{
    text-decoration: underline;
    text-decoration-color:var(--header_menu_hover);
    text-decoration-thickness: 3px;
    text-underline-offset: 4px;
    transition: all .8s ease-in-out;


}


</style>