import json
from channels.generic.websocket import AsyncWebsocketConsumer
from llama_index.llms.gemini import Gemini
import os

# Configura la API key de Gemini
GOOGLE_API_KEY = "AIzaSyANKRunVr3c24k7LBNKhTAMuzurgEPqhK0"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
model = Gemini(model="models/gemini-1.5-flash", api_key=GOOGLE_API_KEY)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Aceptar conexión
        await self.accept()

    async def disconnect(self, close_code):
        # Limpiar al desconectar
        pass

    async def receive(self, text_data):
        # Procesar mensaje recibido
        text_data_json = json.loads(text_data)
        user_message = text_data_json['message']

        # Obtener respuesta de Gemini
        try:
            response = model.complete(prompt=user_message).text
            print(response)
        except Exception as e:
            response = f"Error al procesar la solicitud: {str(e)}"

        # Enviar respuesta al cliente
        await self.send(text_data=json.dumps({
            'message': response
        }))
