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
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(resp => resp.json())
        .then(data => showDataToast(data));
}

const bot_ui = (username) => {
    const item = document.createElement('li');
    item.classList.add('row');
    item.innerHTML = `
        ${username}
         <img class="img-btn" src="${window.img.token}" alt="Get Bot ${username} Token Button"
                 width="25" height="25" onclick="start_bot_verification(window.api.bot_get_token, 'POST', '${username}')">
         <img class="img-btn" src="${window.img.reload}" alt="Regenerate Bot ${username} Token Button"
                 width="25" height="25" onclick="start_bot_verification(window.api.bot_regenerate_token, 'PATCH', '${username}')">
         <img class="img-btn" src="${window.img.cross}" alt="Remove Bot ${username} Button"
                 width="25" height="25" onclick="start_bot_verification(window.api.bot_remove, 'DELETE', '${username}')">
    `;
    return item
}

window.get_bots = (uri) => {
    const bots = document.getElementById('bots');
    fetch(uri, {
        method: 'GET'
    }).then(resp => resp.json())
        .then(data => {
            if (data.ok) {
                bots.innerHTML = '';
                for (const bot of data.bots)
                    bots.appendChild(bot_ui(bot));
            }
            else showDataToast(data);
        });
}

window.start_bot_verification = (uri, method, username) => {
    document.querySelector('input[type="hidden"][name="bot_username"]').value = username;
    document.getElementById('verify-bot').open = true;
    window.bot_verification = {
        method: method,
        uri: uri
    };
}

window.add_bot = (uri, get_uri) => {
    const form = document.querySelector('form[name="add-bot"]');
    const data = serialize(new FormData(form));
    fetch(uri, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(resp => resp.json())
        .then(data => {
            showDataToast(data);
             get_bots(get_uri);
        });
}
window.verify_bot = (get_uri) => {
    const form = document.querySelector('form[name="verify-bot"]');
    const data = serialize(new FormData(form));
    fetch(window.bot_verification.uri, {
        method: window.bot_verification.method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(resp => resp.json())
        .then(data => {
            showDataToast(data);
            get_bots(get_uri);
        });
}

function showDataToast(data) {
    Toastify({
        text: data.ok ? (data.msg ?? `Token: ${data.token}`) : data.error,
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
