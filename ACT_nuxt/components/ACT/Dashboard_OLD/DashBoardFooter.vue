<template>
    
    <footer>
              <div class="footer_content" style="width:90%; margin:0">
                <div class="footer_grid_left">
                  <div class="footer_elm_left">
                    <h5>Footer</h5>
                    <span class="footer_subheading">In Progress.</span>
                  </div>
                  <a href="" class="footer_logo footer_elm_left" style="width:50px; padding-bottom: 0; margin-top:-15px">
                    <SvgLogo v-bind="svg_footer" />
                  </a>
                  <div class="footer_elm_left" style="padding-top:15px">
                    <span class="footer_subheading">Copyright © GET MEDIA 2022</span>
                  </div>
                </div>

              </div>
            </footer>


</template>

<script setup>


const svg_footer = {
  width: 300,  
}




</script>


<style scoped>

footer {
    display: block;
    z-index:-1;
    width:100%;
    height:400px;
    position: -webkit-sticky;
    position: sticky;
    bottom: 0;
}

.footer_logo {
    color: var(--theme-color);
}
.footer_elm_left {
    padding-bottom: 10px;
    white-space: nowrap;
    color: var(--theme-color) !important;
}
.footer_subheading {
    white-space: nowrap;
    color: var(--footer_subheading) !important;
    text-decoration: none !important;
    line-height: 2.5;
}
.footer_content {
    padding-top: 70px;
    padding-bottom: 35px;
    padding-left: 50px;
    padding-right: 50px;
}
@media (min-width: 768px) {
    .footer_content {
        padding-top: 100px;
        padding-bottom: 50px;
    }
}
@media (min-width: 1025px) {
    .footer_content {
        padding-top: 120px;
        padding-bottom: 50px;
    }
}
.footer_grid_left {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    grid-template-rows: repeat(3, 1fr);
    grid-column-gap: 0;
    grid-row-gap: 0;
    width: 50%;
    margin-top: -70px;
}


</style>