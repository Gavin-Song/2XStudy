const errmsg = document.getElementById('error-msg');

function dispError(msg) {
    errmsg.style.opacity = '1';
    errmsg.innerHTML = msg;
}

function submitOnEnter(el) {
    if (event.key === 'Enter')
        submit();
}