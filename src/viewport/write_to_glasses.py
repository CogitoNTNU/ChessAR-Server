import asyncio
from frame_ble import FrameBle

class FrameController:
    def __init__(self):
        self.frame = FrameBle()

    async def connect(self):
        try:
            await self.frame.disconnect() 
        except Exception:
            pass

        print("Connecting to Frame...")
        await self.frame.connect()
        print("Connected.")

    async def send_text(self, text: str):
        try:
            print(f"Sending text: {text}")
            await self.frame.send_lua(
                f"frame.display.text('{text}', 1, 1);frame.display.show();print(nil)", 
                await_print=True
            )
            print("Text sent successfully.")
        except Exception as e:
            print(f"Failed to send text: {e}")
            raise e

    async def disconnect(self):
        try:
            print("Disconnecting from Frame...")
            await self.frame.disconnect()
            print("Disconnected.")
        except Exception as e:
            print(f"Error during disconnect: {e}")

    async def send_bestmove(self, bestmove: str):
        try:
            await self.connect()
            await self.send_text(bestmove)
        except Exception as e:
            print(f"Error during send_bestmove: {e}")
        finally:
            await self.disconnect()

