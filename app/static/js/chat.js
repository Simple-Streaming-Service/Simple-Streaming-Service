import markdownIt from 'https://cdn.jsdelivr.net/npm/markdown-it@14.1.0/+esm'

const chat_root = document.getElementById('messages');
const message_text = document.getElementById('message-text');

function send_request(streamer, user) {
    fetch(`/api/${streamer}/chat/send`, {
        method: 'POST',
        body: JSON.stringify({
            "message": message_text.value
        })
    }).then(response => {
        response.json().then(chat => {
            if (!chat.ok) handleError(chat.error);
        }).catch(handleError)
    }).catch(handleError)
}

function update_chat(streamer, configurator) {
    fetch(`/api/${streamer}/chat/list?timestamp=${Math.trunc(Date.now() / 1000)}&limit=50`, {
        method: 'GET'
    }).then(response => {
        response.json().then(chat => {
            if (chat.ok) {
                 const md = markdownIt();
                configurator(md)
                md.use();
                chat_root.innerHTML = '';
                chat.messages.forEach(message => {
                    const div = document.createElement("p");
                    div.className = "chat__message";
                    div.innerText = `${message.user}: ${md.render(markdownIt. message.content)}`;
                    chat_root.append(div);
                })
                setTimeout(update_chat, 100, streamer);
            }
            else handleError(chat.error);
        }).catch(handleError)
    }).catch(handleError)
}

function handleError(error) {
    // TODO: Error handling!
    alert(error);
    setTimeout(update_chat, 10_000, streamer);
}