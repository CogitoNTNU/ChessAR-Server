import io
from PIL import Image
from frame_ble.frame_ble import asyncio
from src.viewport.viewport import ViewPort
from frame_msg import FrameMsg, RxPhoto, TxCaptureSettings
import time

ViewPortImage = Image.Image

class Frame(ViewPort):
    """
    This class implements a frame viewport interface to be used as a base for all frame viewports.
    """
    def __init__(self) -> None:
        """
        Initializes the Frame glasses.
        """
        super().__init__()
        self.frame = FrameMsg()


    async def init_frame(self) -> None:
        try:
            await self.frame.connect()
            await self.frame.print_short_text("Loading...")
            await self.frame.upload_stdlua_libs(lib_names=['data', 'camera'])
            await self.frame.upload_frame_app(local_filename="lua/camera_frame.lua")
            self.frame.attach_print_response_handler()

            await self.frame.start_frame_app()

            rx_photo = RxPhoto()
            self.photo_queue = await rx_photo.attach(self.frame)
            print("Letting autoexposure loop run for 5 seconds to settle")
            # await asyncio.sleep(5.0)
            print("Taking snapshot")
            self.initialized = True
        except Exception as e:
            print(f"Error initializing Frame: {e}")
            await self.frame.disconnect()
            raise e

    async def write_to_frame(self, text: str) -> None:
        """
        Writes a message to the frame.
        """
        await self.frame.print_short_text(text)

    async def get_output(self) -> ViewPortImage:
        """
        Returns the current state of the chess board as a stream or image.
    """
        # await self._init_frame()

        image = await self._take_snapshot()

        if image is None:
            raise ValueError("Frame couldn't take snapshot")

        return image

    async def _take_snapshot(self) -> ViewPortImage | None:
        """
        Takes a snapshot of the camera feed.
        """
        if (self.frame is None):
            raise ValueError("Frame is not connected")

        try:
            await self.frame.send_message(0x0d, TxCaptureSettings(resolution=720).pack())
            jpeg_bytes = await asyncio.wait_for(self.photo_queue.get(), timeout=10.0)
            image = Image.open(io.BytesIO(jpeg_bytes))
            image.save(f"misc/images/frame_image_{time.time()}.png")

            return image

        except Exception as e:
            print(f"Error taking snapshot: {e}")
            return None
