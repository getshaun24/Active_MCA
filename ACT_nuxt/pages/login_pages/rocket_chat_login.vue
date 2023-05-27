<script setup>




const rocket_chat_auth_token = useCookie('rocket_chat_auth_token')
console.log(rocket_chat_auth_token.value)

fetch("https://get.rocket.chat/", {
    method: 'POST',
    mode: 'cors',
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({loginToken:rocket_chat_auth_token.value})
})
.then((response) => response.json())
.then((data) => {

    alert('Chat Log Success')



})
.catch(error => {
    alert('Chat Log Error')
});





</script>
