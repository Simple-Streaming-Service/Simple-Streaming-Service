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