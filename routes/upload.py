import os
import time
import json
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for
from core import ocr, spellcheck, translate, detector, metadata
from core.metadata_export import process_images_and_export_xml


upload_bp = Blueprint('upload', __name__, template_folder='templates')


def detection_pipeline(image, processed_path):
    text = ocr.extract_text(image).strip()
    corrected_text = spellcheck.correct_text(text)
    translated_text = translate.translate_text(corrected_text, dest_lang='ru')
    detections = detector.detect_objects(image, processed_path)

    translated_objects = [translate.translate_text(det["class"], dest_lang='ru') for det in detections]
    return text, corrected_text, translated_text, detections, translated_objects


def process_file(file):
    if file.filename == '':
        return None

    filename = secure_filename(file.filename)
    base, ext = os.path.splitext(filename)
    if not ext:
        ext = ".jpg"
    timestamp = int(time.time())
    base_name = f"{base}_{timestamp}"
    processed_filename = base_name + ext
    json_filename = base_name + ".json"

    processed_path = os.path.join('static', 'processed', processed_filename)
    json_path = os.path.join('data', json_filename)

    img = Image.open(file.stream)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    text, corrected_text, translated_text, detections, translated_objects = detection_pipeline(
        img, processed_path
    )

    objects_to_save = translated_objects if translated_objects else None
    text_to_save = translated_text if translated_text.strip() else None
    metadata.add_metadata(processed_path, objects_to_save, text_to_save)

    result_data = {
        "id": base_name,
        "original_filename": filename,
        "processed_image": processed_filename,
        "objects": detections,
        "objects_translated": translated_objects,
        "text": text,
        "corrected_text": corrected_text,
        "translated_text": translated_text
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)

    return result_data, processed_filename


def process_uploaded_files(files):
    processed_results = []
    current_files = []

    for file in files:
        result = process_file(file)
        if result:
            result_data, processed_filename = result
            processed_results.append(result_data)
            current_files.append(processed_filename)

    xml_timestamp = int(time.time())
    xml_filename = f"output_{xml_timestamp}.xml"
    xml_path = os.path.join('data', xml_filename)
    process_images_and_export_xml('static/processed', xml_path, 'rus', file_list=current_files)
    for res in processed_results:
        res["xml_filename"] = xml_filename
        json_file = os.path.join('data', res["id"] + ".json")
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            existing_data["xml_filename"] = xml_filename
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)

    return processed_results, xml_filename


@upload_bp.route('/upload', methods=['POST'])
def upload_page():
    if 'images' not in request.files:
        return redirect(url_for('index'))

    files = request.files.getlist('images')
    processed_results, xml_filename = process_uploaded_files(files)
    return render_template('results.html', results=processed_results, xml_filename=xml_filename)
