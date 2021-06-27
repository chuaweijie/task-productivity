import { getCookie } from './helpers.js';

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#username').addEventListener('blur', () => checkUsername());
    document.querySelector('#email').addEventListener('blur', () => checkEmail());
    document.querySelector('#password').addEventListener('blur', () => checkPassword());
    document.querySelector('#confirmation').addEventListener('input', () => checkConfirmation());
});

function checkUsername() {
    const username_ele = document.querySelector('#username');
    const username = username_ele.value;
    const csrftoken = getCookie('csrftoken');

    if (username.length < 1) {
        username_ele.classList.add("is-invalid");
    }
    else {
        fetch ('/username', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                username: username
            })
        })
        .then(response => response.json())
        .then(result => {
            const unique = result["unique"]
            if (unique == true) {
                username_ele.classList.remove("is-invalid");
                username_ele.classList.add("is-valid");
            }
            else if (unique == false) {
                username_ele.classList.remove("is-valid");
                username_ele.classList.add("is-invalid");
            }
            signupToggle();
        });
    }
}

function checkEmail() {
    const email_ele = document.querySelector('#email');
    const email = email_ele.value;

    if (!validateEmail(email)) {
        email_ele.classList.add("is-invalid");
    }
    else {
        const csrftoken = getCookie('csrftoken');
        fetch ('/email', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                email: email
            })
        })
        .then(response => response.json())
        .then(result => {
            const unique = result["unique"]
            if (unique == true) {
                email_ele.classList.remove("is-invalid");
                email_ele.classList.add("is-valid");
            }
            else if (unique == false) {
                email_ele.classList.remove("is-valid");
                email_ele.classList.add("is-invalid");
            }
            signupToggle();
        });
    }
}

//Code from: https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function checkPassword() {
    const password_ele = document.querySelector('#password');
    const password = password_ele.value;
    const confirmation = document.querySelector('#confirmation').value;

    if (password.length > 7) {
        password_ele.classList.remove("is-invalid");
        password_ele.classList.add("is-valid");
    }
    else {
        password_ele.classList.remove("is-valid");
        password_ele.classList.add("is-invalid");
    }
    if (confirmation.length == 0) {
        signupToggle();
    }
    else {
        checkConfirmation();
    }
    
}

function checkConfirmation() {
    const password = document.querySelector('#password').value;
    const confirmation_ele = document.querySelector('#confirmation');
    const confirmation = confirmation_ele.value;

    if (password == confirmation) {
        confirmation_ele.classList.remove("is-invalid");
        confirmation_ele.classList.add("is-valid");
    }
    else {
        confirmation_ele.classList.remove("is-valid");
        confirmation_ele.classList.add("is-invalid");
    }
    signupToggle();
}

function signupToggle(){
    const inputs = document.querySelectorAll("input");
    const signup = document.querySelector("#signup");
    let count = 0;
    inputs.forEach(element => {
        if (element.classList.contains("is-valid")) {
            count++;
            console.log("is-valid");
        }
    });

    if (count == 4) {
        signup.disabled = false;
    }
    else {
        signup.disabled = true;
    }
}