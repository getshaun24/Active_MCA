<template>
    
    <div class="navigation_header">
            <div class="nav_menu_title">Page Navigation</div>
            <div class="header-menu">
              <a class="navigation_menu is-active" href="#">xxx</a>
              <a class="navigation_menu" href="#">xxx</a>
              <a class="navigation_menu" href="#">xxx</a>
            </div>
          </div>


</template>


<style scoped>


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
.navigation_header {
    display: flex;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
    height: 58px;
    flex-shrink: 0;
    z-index: 1;
    margin-top:80px;
    background-color:#fff;
    margin-left:275px
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
    padding: 17px 24px;
}
.nav_menu_title {
    text-decoration: none;
    color: var(--theme-color);
    padding: 0 30px;
}


</style>