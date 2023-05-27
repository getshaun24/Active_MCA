

export const send_api_call = (url_endpoint, data_to_post) => {


  const config = useRuntimeConfig()
  const data = ref(null)
  const error = ref(null)


  fetch(String(config.flask_url + url_endpoint), {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
      },
      // credentials: 'include',
      body: JSON.stringify(data_to_post)
  })
  .then((response) => response.json())
  .then((data) => {

    data.value = data
    alert(data.message)
  })
  .catch(error => {
      // message.value = error;
      alert("Error")
      error.value = error
  });

  // .then((res) => res.json())
  //   .then((json) => (data.value = json))
  //   .catch((err) => (error.value = err))



  return { data, error }



}
