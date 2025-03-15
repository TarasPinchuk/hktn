import json
from pathlib import Path
from typing import Dict, List
from flask import Blueprint, render_template


index_bp = Blueprint('index', __name__, template_folder='templates')


def load_json_file(filepath: Path) -> dict:
    return json.loads(filepath.read_text(encoding='utf-8'))


def get_results_from_data_dir(data_dir: Path) -> List[Dict[str, str]]:
    results = []
    for filepath in data_dir.glob('*.json'):
        data = load_json_file(filepath)
        results.append({
            "id": filepath.stem,
            "original_filename": data.get("original_filename", ""),
            "processed_image": data.get("processed_image", "")
        })
    return results


@index_bp.route('/')
def index_page():
    results_dir = Path('./data')
    results = get_results_from_data_dir(results_dir)
    return render_template('index.html', results=results)
