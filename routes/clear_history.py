from pathlib import Path
from flask import Blueprint, redirect, url_for


clear_bp = Blueprint('clear', __name__)


def clear_files_in_directory(directory: Path, pattern: str = '*'):
    for file in directory.glob(pattern):
        if file.is_file():
            file.unlink()


def clear_history_files():
    data_dir = Path('data')
    processed_dir = Path('static') / 'processed'
    clear_files_in_directory(data_dir, '*.json')
    clear_files_in_directory(data_dir, '*.xml')
    clear_files_in_directory(processed_dir)


@clear_bp.route('/clear_history', methods=['POST'])
def clear_history():
    clear_history_files()
    return redirect(url_for('index.index_page'))
