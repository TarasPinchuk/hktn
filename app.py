from pathlib import Path
from flask import Flask
from flasgger import Swagger
from routes.index import index_bp
from routes.upload import upload_bp
from routes.search import search_bp
from routes.result import result_bp
from routes.statistics import stats_bp
from routes.clear_history import clear_bp


def init_app():
    app = Flask(__name__)
    app.register_blueprint(index_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(result_bp)
    app.register_blueprint(clear_bp)
    app.register_blueprint(stats_bp)
    return app


if __name__ == '__main__':
    Path('static/processed').mkdir(exist_ok=True)
    Path('data').mkdir(exist_ok=True)
    app = init_app()
    swagger = Swagger(app, template_file='swagger.yaml')
    app.run(debug=True)
