
    import { page_to } from "../stores/page_to.js"

export default defineNuxtRouteMiddleware((to, from) => {





  const getDepth = (path) => {
    return path.split('/').filter(seg => seg.length > 0).length;
  }

  const toDepth = getDepth(to.path);
  const fromDepth = getDepth(from.path);


    const new_page_to = page_to()

  console.log('middleware path', to.path)
  console.log('toDepth', toDepth)
  console.log('fromDepth', fromDepth)



  new_page_to.page_to_update(String(from.path), String(to.path))


  if (String(to.path).includes('fund_pages')) {
    to.meta.pageTransition = { name: 'page-scale', onAfterEnter: (el) => {
        console.log('After enter...')

      }, };
    from.meta.pageTransition = { name: 'page-scale' };
    console.log('to.meta.pageTransition', to.meta.pageTransition)
  } else {
    // to.meta.pageTransition = { name: 'page-scale' };
    // from.meta.pageTransition = { name: 'page-scale' };
  }
})