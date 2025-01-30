window.toggle_key = () => {
    const input = document.querySelector(`input[name='streaming_key']`);
    if (input.type === "password") input.type = "text";
    else input.type = "password";
}

window.regenerate_token = (uri) => {
    fetch(uri, {
        method: 'POST'
    }).then(resp => resp.json())
        .then(data => showDataToast(data));
}

window.get_token = (uri) => {
    fetch(uri, {
        method: 'GET'
    }).then(resp => resp.json())
        .then(data => {
            if (data.ok) {
                const input = document.querySelector(`input[name='streaming_key']`);
                input.value = data.token;
            }
            else showDataToast(data)
        });

}


window.changes = []
const form = document.querySelector('form[name="stream"]');
form.addEventListener('submit', async evt => {
    evt.preventDefault();
    if (window.changes.includes("name")) {
        const input = document.querySelector(`input[name='stream_name']`);
        fetch(window.stream_name_uri, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: `{"stream_name":"${input.value}"}`
        }).then(resp => resp.json())
            .then(data => showDataToast(data));
    }
    window.changes = []
});

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