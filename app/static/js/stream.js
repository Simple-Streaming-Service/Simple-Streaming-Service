import markdownIt from 'https://cdn.jsdelivr.net/npm/markdown-it@14.1.0/+esm'

const md = markdownIt();
const chat_root = document.getElementById('messages');
const message_text = document.getElementById('message-text');

window.init_chat = (initializer) => {
    initializer(md);
}

window.send_request = (streamer) => {
    fetch(`/api/v1/stream/${streamer}/chat/send`, {
        method: 'POST',
        body: JSON.stringify({
            "user": "Anonym",
            "message": message_text.value
        })
    }).then(response => {
        response.json().then(chat => {
            if (!chat.ok) handleError(chat.error);
        }).catch(handleError)
    }).catch(handleError)
}

const startStamp = Math.trunc(Date.now() / 1000);
window.update_chat = (streamer) => {
    fetch(`/api/v1/stream/${streamer}/chat/list?start_timestamp=${startStamp}&end_timestamp=${Math.trunc(Date.now() / 1000)}&limit=50`, {
        method: 'GET'
    }).then(response => {
        response.json().then(chat => {
            if (chat.ok) {
                chat_root.innerHTML = '';
                chat.messages.forEach(message => {
                    const div = document.createElement("p");
                    div.className = "chat__message";
                    div.innerHTML = `${message.user}: ${md.render(message.content)}`;
                    chat_root.append(div);
                })
                setTimeout(update_chat, 100, streamer);
            }
            else handleError(chat.error, streamer);
        }).catch(error => handleError(error, streamer));
    }).catch(error => handleError(error, streamer))
}

function handleError(error, streamer) {
    // TODO: Error handling!
    showDataToast(error)
    if (streamer) setTimeout(update_chat, 10_000, streamer);
}

function showDataToast(data) {
    Toastify({
        text: data,
        duration: 3000,
        close: true,
        gravity: "top",
        position: "right",
        style: {
            background: "linear-gradient(90deg, rgba(255,133,57,1) 0%, rgba(251,0,115,1) 100%)",
        }
    }).showToast();
}