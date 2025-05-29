import json
import os.path
import uuid
import zlib
from datetime import datetime

from app.models.account import User
from app.models.messaging import Message
from app.services.user import delete_user

msg_path = '/archive/messages/'
user_path = '/archive/users/'

os.makedirs(msg_path, exist_ok=True)
os.makedirs(user_path, exist_ok=True)

class Registry:
    def __init__(self, filepath):
        self.registry = {}
        self.__filepath = filepath

    def load_registry(self):
        if os.path.exists(self.__filepath):
            with open(self.__filepath, 'r') as reg:
                self.registry = json.loads(reg.read())


    def save_registry(self):
        with open(self.__filepath, 'w') as reg:
            reg.write(json.dumps(self.registry))
        self.registry = {}


msg_registry = Registry(msg_path + 'registry')
user_registry = Registry(user_path + 'registry')

def pack_old_messages(date: datetime, min_pack_count: int = 1000):
    nodes = Message.nodes.filter(timestamp__lte=date).all()
    if len(nodes) < min_pack_count:
        return 0
    reg_data = {}
    messages = []
    for node in nodes:
        streamer = node.streamer.single().user().single().username
        messages.append({
            "streamer": streamer,
            "author": node.author.single().username,
            "timestamp": node.timestamp.isoformat(),
            "content": node.content
        })
        if streamer not in reg_data:
            reg_data[streamer] = {
                "from": node.timestamp.isoformat(),
                "to": node.timestamp.isoformat()
            }
        else:
            if datetime.fromisoformat(reg_data[streamer]["from"]) > node.timestamp:
                reg_data[streamer]["from"] = node.timestamp.isoformat()
            if datetime.fromisoformat(reg_data[streamer]["to"]) < node.timestamp:
                reg_data[streamer]["to"] = node.timestamp.isoformat()
        node.delete()
    block_id = uuid.uuid4().hex

    msg_registry.registry[block_id] = reg_data
    pack_data(msg_path + block_id, messages)
    return len(messages)


def delete_old_messages(date: datetime):
    del_count = 0
    for block_id, reg_data in msg_registry.registry.items():
        deletable = True
        for streamer, data in reg_data.items():
            if datetime.fromisoformat(data["to"]) > date:
                deletable = False
                break
        if deletable:
            os.remove(msg_path + block_id)
            del msg_registry.registry[block_id]
            del_count += 1
    return del_count


def restore_messages(streamer: str, from_date: datetime, to_date: datetime):
    return []


def pack_old_users(date: datetime, min_pack_count: int = 100):
    nodes = User.nodes.filter(last_login__lte=date).all()
    if len(nodes) < min_pack_count:
        return 0
    reg_data = {}
    users = []
    for node in nodes:
        users.append({
            "username": node.username,
            "password": node.password,
            "email": node.email,
            "created_at": node.created_at.isoformat(),
            "revoked_at": node.revoked_at.isoformat(),
            "revoked_by": node.revoked_by,
        })
        reg_data[node.username] = node.last_login.isoformat()
        delete_user(node)
    block_id = uuid.uuid4().hex
    user_registry.registry[block_id] = reg_data
    pack_data(user_path + block_id, users)
    return len(users)


def delete_old_users(date: datetime):
    del_count = 0
    for block_id, reg_data in msg_registry.registry.items():
        deletable = True
        for user, time in reg_data.items():
            if datetime.fromisoformat(time) > date:
                deletable = False
                break
        if deletable:
            os.remove(msg_path + block_id)
            del msg_registry.registry[block_id]
            del_count += 1
    return del_count


def restore_user(mail: str, new_username: str):
    return False


def pack_data(file: str, data):
    data = json.dumps(data)
    with open(file, 'w') as f:
        f.write(zlib.compress(
            data.encode('utf8'),
            zlib.Z_BEST_COMPRESSION
        ).decode('utf8'))


def unpack_data(file: str):
    with open(file, 'r') as f:
        data = zlib.decompress(
            f.read().encode('utf8')
        ).decode('utf8')
        return json.loads(data)
