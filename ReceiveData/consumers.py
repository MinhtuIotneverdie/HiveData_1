import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Kiểm tra nếu message đến từ HiveMQ và có dạng JSON
        try:
            hive_data = json.loads(message)
            humidity = hive_data.get('humidity')

            # Kiểm tra xem có dữ liệu humidity hay không
            if humidity is not None:
                self.send(text_data=json.dumps({
                    'humidity': humidity
                }))
        except json.JSONDecodeError:
            pass