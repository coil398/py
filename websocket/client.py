import asyncio
import websockets


async def chat_client():
    uri = "ws://localhost:8000/ws/chat"

    async with websockets.connect(uri) as websocket:
        print("Connected to the WebSocket server")

        async def receive_messages():
            while True:
                try:
                    message = await websocket.recv()
                    print(f"Received message: {message}")
                except websockets.ConnectionClosed:
                    print("Connection closed")
                    break
                except websockets.WebSocketException as e:
                    if e.code == 403:
                        print("Unauthorized access - 403 Forbidden")
                        break

        asyncio.create_task(receive_messages())

        while True:
            try:
                message = input("Enter your message: ")
                if message.lower() == "exit":
                    print("Exiting chat")
                    break
                await websocket.send(message)
            except websockets.ConnectionClosed:
                print("Connection closed")
                break


if __name__ == "__main__":
    asyncio.run(chat_client())
