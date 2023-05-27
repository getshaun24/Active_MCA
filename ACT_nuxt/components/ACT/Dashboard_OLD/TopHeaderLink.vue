<template>

         <NuxtLink to="/" class="top_header_link" v-for="item in links" >{{ item.button_title }}</NuxtLink>


</template>



<script setup>

const props = defineProps(['links'])

</script>

<style scoped>



.top_header_link:first-child {
    margin-top: 13px;
    padding: 15px 30px;
    padding-bottom: 30px;
    text-decoration: none;
    color: var(--inactive-color);
    border-bottom: 2px solid transparent;
    transition: 0.3s;
    margin-left: -65px;
}
.top_header_link {
    padding: 15px 30px;
    padding-bottom: 30px;
    text-decoration: none;
    color: var(--inactive-color);
    border-bottom: 2px solid transparent;
    transition: 0.5s;
    margin-top: 13px;
}
.is-active {
    color: var(--header_menu_hover) !important;
    border-bottom: 3.5px solid var(--header_menu_hover) !important;
}
.top_header_link:hover {
    color: var(--header_menu_hover);
    border-bottom: 3.5px solid var(--header_menu_hover);
}
.notify {
    position: relative;
}
.notify:before {
    content: "";
    position: absolute;
    background-color: #3a6df0;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    right: 20px;
    top: 16px;
}
</style>