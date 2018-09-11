from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from channels import Group
# from channels.auth import channel_session_user, channel_session_user_from_http


# @channel_session_user_from_http
# async def ws_connect(message):
#     Group('users').add(message.reply_channel)
#     Group('users').send({
#         'text': json.dumps({
#             'username': message.user.username,
#             'is_logged_in': True
#         })
#     })


# @channel_session_user
# async def ws_disconnect(message):
#     Group('users').send({
#         'text': json.dumps({
#             'username': message.user.username,
#             'is_logged_in': False
#         })
#     })
#     Group('users').discard(message.reply_channel)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))





