from io import BytesIO
from PIL import Image

def file_image():
    file = BytesIO()
    file.name = "test_image.png"
    image = Image.new("RGBA", size=(100,100))
    image.save(file, "PNG")
    file.seek(0)
    return file