import asyncio
import websockets

async def echo(websocket):
    print(f"New connection from {websocket.remote_address}")
    
    try:
        # Send a message every second
        while True:
            await websocket.send("Server message every second")
            await asyncio.sleep(1)  # Wait for 1 second before sending the next message

    except websockets.ConnectionClosed:
        print(f"Connection closed from {websocket.remote_address}")
    finally:
        await websocket.close()

async def main():
    server = await websockets.serve(echo, "localhost", 8080)
    print("WebSocket server started on ws://localhost:8080")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
