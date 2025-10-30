from PIL import Image
import io

class ModuleImage:
    def decode(self, image: bytes) -> Image.Image:
        return Image.open(io.BytesIO(image))
