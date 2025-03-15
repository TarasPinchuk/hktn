import json
from pathlib import Path
from flask import Blueprint, render_template, send_from_directory


result_bp = Blueprint('result', __name__, template_folder='templates')


@result_bp.route('/result/<id>')
def result_page(id):
    json_path = Path('data') / f"{id}.json"
    if not json_path.exists():
        return "Result not found", 404
    with json_path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('result.html', data=data)


@result_bp.route('/download_xml/<filename>')
def download_xml(filename):
    return send_from_directory('data', filename, as_attachment=True)
