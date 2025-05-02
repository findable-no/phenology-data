import io
from PIL import Image
from IPython.display import display
from typing import Optional


def plot_image(image_data):
    import io
    from PIL import Image

    # Create a BytesIO object from the binary data
    image_stream = io.BytesIO(image_data)

    # Open and show the image
    try:
        # Open the image using PIL
        img = Image.open(image_stream)

        # Save the image to a file
        img.save("output_image.png")

        # Display the image (this will open it in your default image viewer)
        img.show()
    except Exception as e:
        print(f"Error processing image: {e}")


def display_image(image_data):

    # Create BytesIO object from the binary data
    image_stream = io.BytesIO(image_data)
    img = Image.open(image_stream)

    # Display directly in the notebook
    display(img)


def display_images(image_datas, text: Optional[str] = None):
    # Display multiple images
    if not text:
        text = [""] * len(image_datas)
    for image_data, text in zip(image_datas, text):
        # Create BytesIO object from the binary data
        image_stream = io.BytesIO(image_data)
        img = Image.open(image_stream)
        # Display directly in the notebook
        print(text)
        display(img)


def get_pil_image(image_bytes):
    image_stream = io.BytesIO(image_bytes)
    return Image.open(image_stream)
