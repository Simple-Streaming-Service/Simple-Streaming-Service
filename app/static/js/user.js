window.username_change = (uri) => {
    const input = document.querySelector(`input[name='username']`);
    if (input.readOnly)
        input.readOnly = false;
    else {
        input.readOnly = true;
        fetch(uri, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: `{"username":"${input.value}"}`
        }).then(resp => resp.json())
            .then(data => showDataToast(data));
    }
}
window.log_out = (uri, redirect_uri, token) => {
    const input = document.querySelector(`input[name='username']`);
    if (input.readOnly)
        input.readOnly = false;
    else {
        input.readOnly = true;
        fetch(uri, {
            method: 'POST',
            headers: {
                'X-CSRFToken': token
            },
        }).then(resp => resp.json())
            .then(data => location.href = redirect_uri);
    }
}

window.email_change = (uri) => {
    const input = document.querySelector(`input[name='email']`);
    if (input.readOnly)
        input.readOnly = false;
    else {
        input.readOnly = true;
        fetch(uri, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: `{"email":"${input.value}"}`
        }).then(resp => resp.json())
            .then(data => showDataToast(data));
    }
}

window.change_password = (uri) => {
    console.log("change_password");
}

function showDataToast(data) {
    Toastify({
        text: data.ok ? data.msg : data.error,
        duration: 3000,
        close: true,
        gravity: "top",
        position: "right",
        style: data.ok ?
            {
                background: "linear-gradient(90deg, rgba(57,255,213,1) 0%, rgba(0,251,72,1) 100%)",
            } :
            {
                background: "linear-gradient(90deg, rgba(255,133,57,1) 0%, rgba(251,0,115,1) 100%)",
            }
    }).showToast();
}
