import os
from PIL import Image, PngImagePlugin

try:
    import piexif
except ImportError:
    piexif = None


def add_metadata(image_path, objects, text):
    metadata_fields = []
    if objects:
        metadata_fields.append("объекты: " + ", ".join(objects))
    if text:
        metadata_fields.append("текст: " + text)

    if not metadata_fields:
        return

    metadata_str = "; ".join(metadata_fields)
    ext = os.path.splitext(image_path)[1].lower()

    if ext in ['.jpg', '.jpeg']:
        if piexif is None:
            print("Библиотека piexif не установлена – невозможно добавить EXIF для JPEG.")
            return
        try:
            exif_dict = piexif.load(image_path)
        except Exception:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = metadata_str.encode('utf-8')
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)
    elif ext == '.png':
        image = Image.open(image_path)
        meta = PngImagePlugin.PngInfo()
        meta.add_text("Description", metadata_str)
        image.save(image_path, "PNG", pnginfo=meta)
    else:
        print("Формат изображения не поддерживается для записи метаданных:", ext)
