

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()
from django.conf import settings
import redis
from utils.control.interface import Message
from channels.layers import get_channel_layer
import asyncio


r = redis.Redis(host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_CONTROLER_DB)
channel_layer = get_channel_layer()

def send_message(data):
    asyncio.run(channel_layer.group_send(
        25, {
            "type": "group.message",
            "message": Message.data(data, 25)
        }
    ))

def main():
    pubsub = r.pubsub()
    pubsub.subscribe('test_channel')
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(message)
            send_message(message['data'].decode('utf-8'))

if __name__ == "__main__":
    main()
