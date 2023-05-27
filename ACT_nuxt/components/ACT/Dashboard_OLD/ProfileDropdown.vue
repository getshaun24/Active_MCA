<template>

<div class="profile_dropdown" :class="{ active : isactive == true }">
      <div class="profile_menu">
        <div class="side-menu">
          <img class="profile_img_dropdown" src="~/assets/content/ACT_dashboard/shaun_profile.jpg" alt="">
          <a class="side_menu_link" href="#">
           
            Profile
          </a>
          <a class="side_menu_link" href="#">
           
            Settings
          </a>
          <a class="side_menu_link" href="#">
            
            Security
          </a>
          <a class="side_menu_link" href="#" style="font-size:25px; padding:20px; margin-top:10px">
            <div class="logout_circle"></div>
            Log Out
          </a>
          <div class="background_profile"></div>
        </div>
      </div>
    </div>

</template>


<script setup>

const props = defineProps(['isactive'])
const emit = defineEmits(['isactive'])





function OpenMenu(val){


    emit('isactive', val)


}

function CloseMenu(val){

    emit('isactive', val)

}


</script>



<style scoped>

.active{
    display: block;
   } 
    

img {
    max-width: 100%;
}
.profile-img {
    border: 2px solid var(--theme-bg-color);
    border-radius: 100%;
}
.profile_dropdown {
    width: 300px;
    height: 370px;
    position: absolute;
    margin-top: 58px;
    z-index: 3;
    right: 0;
    margin-right: 10px;
    background-size: cover;
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
.logout_circle {
    width: 25px;
    height: 25px;
    background-color: #cf560b;
    border-radius: 100%;
    margin-right: 5%;
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
.profile_img_dropdown {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    -o-object-fit: cover;
    object-fit: cover;
    border: 2px solid var(--header_menu_hover);
    margin-left: 85px;
    margin-bottom: 15px;
    object-position: top;
}
.side-menu {
    display: flex;
    flex-direction: column;
    white-space: nowrap;
}
.side_menu_link {
    text-decoration: none;
    color: var(--theme-color);
    display: flex;
    align-items: center;
    font-weight: 400;
    padding: 10px;
    font-size: 18px;
    border-radius: 6px;
    transition: 0.3s;
    cursor: pointer;
    margin-top: 10px;
}
.side_menu_link:hover {
    background-color: var(--hover-menu-bg);
}


</style>