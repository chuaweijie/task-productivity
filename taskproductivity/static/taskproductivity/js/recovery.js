import { validateEmail } from './helpers.js';

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#email').addEventListener('input', () => checkEmail());
});

function checkEmail() {
    const email_ele = document.querySelector('#email');
    const email = email_ele.value;
    const btn_submit = document.querySelector('#btn_submit');

    if (validateEmail(email)) {
        email_ele.classList.remove("is-invalid");
        email_ele.classList.add("is-valid");
        btn_submit.disabled = false;
    }
    else {
        email_ele.classList.remove("is-valid");
        email_ele.classList.add("is-invalid");
        btn_submit.disabled = true;
    }
}