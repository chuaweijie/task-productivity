document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#username').addEventListener('onblur', () => check_username());
});

function check_username() {
    const username = document.querySelector('#username').value;
    fetch ('/email', {
        method: 'POST',
        body: JSON.stringify({
            username: username
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log("result!");
        console.log(result);
    });
}