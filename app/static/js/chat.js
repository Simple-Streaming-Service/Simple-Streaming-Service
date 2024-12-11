import markdownIt from 'https://cdn.jsdelivr.net/npm/markdown-it@14.1.0/+esm'

const chat_root = document.getElementById('messages');
const message_text = document.getElementById('message-text');

window.send_request = (streamer) => {
    fetch(`/api/${streamer}/chat/send`, {
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

window.update_chat = (streamer, configurator) => {
    fetch(`/api/${streamer}/chat/list?timestamp=${Math.trunc(Date.now() / 1000)}&limit=50`, {
        method: 'GET'
    }).then(response => {
        response.json().then(chat => {
            if (chat.ok) {
                 const md = markdownIt();
                configurator(md);
                chat_root.innerHTML = '';
                chat.messages.forEach(message => {
                    const div = document.createElement("p");
                    div.className = "chat__message";
                    div.innerHTML = `${message.user}: ${md.render(message.content)}`;
                    chat_root.append(div);
                })
                setTimeout(update_chat, 100, streamer, configurator);
            }
            else handleError(chat.error, streamer, configurator);
        }).catch(error => handleError(error, streamer, configurator));
    }).catch(error => handleError(error, streamer, configurator))
}

function handleError(error, streamer, configurator) {
    // TODO: Error handling!
    alert(error);
    if (streamer && configurator) setTimeout(update_chat, 10_000, streamer, configurator);
}