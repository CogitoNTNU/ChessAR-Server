import asyncio
from frame_ble import FrameBle

class Write():
    async def write_to_frame(self, bestmove: str):
        frame = FrameBle()

        try:
            try:
                await frame.disconnect()
            except Exception:
                pass 

            print("Connecting to Frame...")
            await frame.connect()

            print(f"Sending move: {bestmove}")
            await frame.send_lua(f"frame.display.text('{bestmove}', 1, 1);frame.display.show();print(nil)", await_print=True)

        except Exception as e:
            print(f"Error during communication with Frame: {e}")

        finally:
            print("Disconnecting...")
            try:
                await frame.disconnect()
            except Exception as e:
                print(f"Error during disconnect: {e}")


write = Write()
asyncio.run(write.write_to_frame("Nc3"))
