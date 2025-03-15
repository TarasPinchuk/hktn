import json
from pathlib import Path
from flask import Blueprint, render_template, request


search_bp = Blueprint('search', __name__, template_folder='templates')
DATA_DIR = Path('data')


def extract_text(data) -> str:
    return " ".join([
        data.get("original_filename", ""),
        data.get("text", ""),
        data.get("corrected_text", ""),
        data.get("translated_text", ""),
        " ".join(data.get("objects_translated", []))
    ])


def search_by_query(query: str):
    query = query.strip().lower()
    results = []

    if query:
        for json_file in DATA_DIR.glob('*.json'):
            with json_file.open('r', encoding='utf-8') as f:
                data = json.load(f)
            text_content = extract_text(data)
            if query in text_content.lower():
                results.append({
                    "id": json_file.stem,
                    "original_filename": data.get("original_filename", ""),
                    "processed_image": data.get("processed_image", "")
                })
    return results


@search_bp.route('/search')
def search_page():
    query = request.args.get('q', '')
    results = search_by_query(query)
    return render_template('search.html', query=query, results=results)
