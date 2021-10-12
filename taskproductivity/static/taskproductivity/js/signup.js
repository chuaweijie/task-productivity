import { getCookie, passwordCheck, confirmationCheck, validateEmail, btnToggle } from './helpers.js';

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
            btnToggle('#signup', 4);
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
            btnToggle('#signup', 4);
        });
    }
}



function checkPassword() {
    passwordCheck('#password', '#confirmation', 8, '#signup', 4);
}

function checkConfirmation() {
    confirmationCheck('#password', '#confirmation', '#signup', 4);
}