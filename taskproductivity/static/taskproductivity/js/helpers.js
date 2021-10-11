export function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//Code from: https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
export function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

export function passwordCheck(pass_id, confirmation_id, min_pass_len, btn_id, total_elements) {
    const password_ele = document.querySelector(pass_id);
    const password = password_ele.value;
    const confirmation = document.querySelector(confirmation_id).value;

    if (password.length >= min_pass_len) {
        password_ele.classList.remove("is-invalid");
        password_ele.classList.add("is-valid");
    }
    else {
        password_ele.classList.remove("is-valid");
        password_ele.classList.add("is-invalid");
    }
    if (confirmation.length == 0 || password.length != confirmation != length) {
        btnToggle(btn_id, total_elements);
    }
    else {
        confirmationCheck(pass_id, confirmation_id, btn_id, total_elements);
    }
    
}

export function confirmationCheck(pass_id, confirmation_id, btn_id, total_elements) {
    const password_ele = document.querySelector(pass_id);
    const password = password_ele.value;
    const confirmation_ele = document.querySelector(confirmation_id);
    const confirmation = confirmation_ele.value;

    if (password == confirmation && password_ele.classList == "form-control is-valid") {
        confirmation_ele.classList.remove("is-invalid");
        confirmation_ele.classList.add("is-valid");
    }
    else {
        confirmation_ele.classList.remove("is-valid");
        confirmation_ele.classList.add("is-invalid");
    }
    btnToggle(btn_id, total_elements);
}

export function btnToggle(btn_id, total_elements){
    const inputs = document.querySelectorAll("input");
    const btn = document.querySelector(btn_id);
    let count = 0;
    inputs.forEach(element => {
        if (element.classList.contains("is-valid")) {
            count++;
            console.log("is-valid");
        }
    });

    if (count == total_elements) {
        btn.disabled = false;
    }
    else {
        btn.disabled = true;
    }
}