

export const phone_format = (e, phone) => {

    const phone_val = phone

    const key = e.keyCode || e.charCode;
    const len_phone = phone_val.length
    if (key !== 8 || key !==  46) {
    if(len_phone == 3 || len_phone == 7){
        phone_val = phone_val + '-'
        }
    }
  return { phone_val }
  
  }
  