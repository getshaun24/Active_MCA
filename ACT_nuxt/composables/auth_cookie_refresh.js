export default function () {
    
    const auth_cookie = useCookie('auth_cookie')
    console.log("Cookie refresh function")
    
    if (auth_cookie.value < new Date().getTime() || auth_cookie.value == null) {
        const config = useRuntimeConfig()
        const csrf_cookie = useCookie('csrf_access_token')
        console.log("timeout")
        auth_cookie.value = null//new Date().getTime()+5*60*1000
        fetch(`${config.flask_url}/api/logout/`, {
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'X-CSRF-TOKEN': csrf_cookie.value
            }
          })
          .then(async response => {
            const data = await response.json();
            if (!response.ok) {
              const error = (data.msg) || response.status
              return Promise.reject(error)
            }
            console.log('Logout success')
            navigateTo('/login_pages/login')
          })
          .catch(error => {
            console.log('Logout error ', error)
            navigateTo('/login_pages/login')
          });
          return false
    } else {
        auth_cookie.value = new Date().getTime()+30*60*1000
        console.log('Not timeout')
        return true
    }
}
