import os
import json
import xml.etree.ElementTree as ET
from PIL import Image
import pytesseract


def process_images_and_export_xml(image_folder, output_xml, lang='rus', file_list=None):
    root = ET.Element("metadata")

    files = file_list if file_list is not None else os.listdir(image_folder)

    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
            image_path = os.path.join(image_folder, filename)
            try:
                image = Image.open(image_path)
            except Exception as e:
                print(f"Ошибка при открытии {filename}: {e}")
                continue

            recognized_text = pytesseract.image_to_string(image, lang=lang).strip()

            base_name = os.path.splitext(filename)[0]
            json_file = os.path.join("data", base_name + ".json")
            detected_object = ""
            if os.path.exists(json_file):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                    if "objects_translated" in json_data and json_data["objects_translated"]:
                        detected_object = ", ".join(json_data["objects_translated"])
                except Exception as e:
                    print(f"Ошибка при чтении {json_file}: {e}")

            image_elem = ET.SubElement(root, "image", attrib={"name": filename})

            object_elem = ET.SubElement(image_elem, "object")
            object_elem.text = detected_object

            text_elem = ET.SubElement(image_elem, "text")
            text_elem.text = recognized_text

            print(f"Обработано изображение: {filename}")

    tree = ET.ElementTree(root)
    tree.write(output_xml, encoding="utf-8", xml_declaration=True)
    print(f"XML-файл сохранен: {output_xml}")
