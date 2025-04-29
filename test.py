from src.representation.wishbone import WishBone
from PIL import Image
import base64

def test_wishbone():

    # Create a mock environment
    environment = None  # Replace with actual environment initialization

    # Initialize the WishBone representation
    wishbone = WishBone(environment)

    # Create a mock input image
    input_image = "./image3.jpg"  # Replace with actual image loading

    # Call the compute method
    chessboard = wishbone.YOLO_detect_pieces(input_image)
    chessboard2 = wishbone.YOLO_detect_corners(input_image)

    # Check the output
    assert chessboard is not None, "Chessboard should not be None"
    print("Test passed: Chessboard computed successfully.")
    print(chessboard)
    print(chessboard2)

if __name__ == "__main__":
    test_wishbone()
