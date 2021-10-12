import { passwordCheck, confirmationCheck } from './helpers.js';

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#password').addEventListener('blur', () => checkPassword());
    document.querySelector('#confirmation').addEventListener('input', () => checkConfirmation());
});

function checkPassword() {
    passwordCheck('#password', '#confirmation', 8, '#btn_submit', 2);
}

function checkConfirmation() {
    confirmationCheck('#password', '#confirmation', '#btn_submit', 2);
}