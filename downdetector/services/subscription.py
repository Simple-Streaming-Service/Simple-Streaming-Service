from downdetector import bot

subscribers = {}

def subscribe(channel : str, chat_id):
    if channel not in subscribers:
        subscribers[channel] = []
    subscribers[channel].append(chat_id)

def unsubscribe(channel : str, chat_id):
    subscribers[channel].remove(chat_id)
    if len(subscribers[channel]) == 0:
        del subscribers[channel]

def broadcast(channel : str, message : str) -> bool:
    if channel not in subscribers:
        return False
    for chat_id in subscribers[channel]:
        bot.send_message(chat_id, message)
    return True