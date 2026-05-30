import asyncio
import websockets
import json
import random
import math
import time

COLORS = ["red", "green", "blue", "white", "yellow"]

async def handler(websocket):
    t = 0
    while True:
        data = {
            "x": round(math.sin(t * 1.3) * 4 + random.uniform(-0.3, 0.3), 3),
            "y": round(math.cos(t * 0.9) * 3 + random.uniform(-0.3, 0.3), 3),
            "color": COLORS[int(t) % len(COLORS)],
            "timestamp": round(time.time(), 3),
        }
        await websocket.send(json.dumps(data))
        await asyncio.sleep(0.5)
        t += 0.5

async def main():
    print("WebSocket server starting at ws://localhost:8765")
    print("Press Ctrl+C to stop.")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
