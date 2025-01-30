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

 function serialize(formData) {
    const data = {};
    for (const [k, v] of formData) data[k] = v;
    return data;
}

window.change_password = (uri) => {
    const form = document.querySelector('form[name="change_password"]');
    const data = serialize(new FormData(form));
    fetch(uri, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'
        },
        body: JSON.stringify(data)
    }).then(resp => resp.json())
        .then(data => showDataToast(data));
}

function showDataToast(data) {
    Toastify({
        text: data.ok ? data.msg : data.error,
        duration: 3000,
        close: true,
        gravity: "top",
        position: "right",
        style: {
            background: data.ok
                ? "linear-gradient(90deg, rgba(57,255,213,1) 0%, rgba(0,251,72,1) 100%)"
                : "linear-gradient(90deg, rgba(255,133,57,1) 0%, rgba(251,0,115,1) 100%)",
        }
    }).showToast();
}
