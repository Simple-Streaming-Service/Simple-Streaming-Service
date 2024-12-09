function update_chat(streamer, chat_limit) {
    const chat_root = document.getElementById('chat');
    chat_root.innerHTML = '';

    fetch(`http://localhost:8088/${streamer}/chat/list?timestamp=${Date.now()}&limit=${chat_limit}`, {
        method: 'GET'
    }).then(response => {
        response.json().then(chat => {
            chat.forEach(message => {
                chat_root.append(`
                    <div class="chat-msg">
                        <h3 class="chat-username">${message.user.username}</h3>
                        <p class="chat-message">${message.content}</p>
                    </div>
                `);
            })
        }).catch(error => {
            // TODO: Error handling!
            console.error(error);
        })
    }).catch(error => {
        // TODO: Error handling!
        console.error(error);
    })
}

