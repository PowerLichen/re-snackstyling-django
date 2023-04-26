from io import BytesIO
from PIL import Image

def file_image(filename="test_image.png"):
    file = BytesIO()
    file.name = filename
    image = Image.new("RGBA", size=(100,100))
    image.save(file, "PNG")
    file.seek(0)
    return file