const chat_root = document.getElementById('messages');
const message_text = document.getElementById('message-text');

function send_request(streamer, user) {
    fetch(`/${streamer}/chat/send`, {
        method: 'POST',
        body: JSON.stringify({
            "user": user,
            "content": message_text.value
        })
    }).then(response => {

    })
}

function update_chat(streamer) {
    fetch(`/${streamer}/chat/list?timestamp=${Math.trunc(Date.now() / 1000)}&limit=50`, {
        method: 'GET'
    }).then(response => {
        response.json().then(chat => {
            chat_root.innerHTML = '';
            chat.forEach(message => {
                const div = document.createElement("p");
                div.className = "chat__message";
                div.innerText = `${message.user}: ${message.content}`;
                chat_root.append(div);
            })
            setTimeout(update_chat, 10, streamer);
        }).catch(error => {
            // TODO: Error handling!
            alert(error);
        })
    }).catch(error => {
        // TODO: Error handling!
        alert(error);
    })
}