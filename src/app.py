import os
from flask import Flask, request, jsonify, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../dist/')
public_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')

app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False

# Database config
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

setup_admin(app)
setup_commands(app)
app.register_blueprint(api, url_prefix='/api')

# Error handling
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Serve index.html
@app.route('/')
def serve_index():
    return send_from_directory(static_file_dir, 'index.html')

# Serve Vite assets (JS, CSS, etc.)
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(os.path.join(static_file_dir, 'assets'), filename)

# Serve public files
@app.route('/public/<path:filename>')
def serve_public_files(filename):
    return send_from_directory(public_dir, filename)

# Catch all - for React Router support
@app.route('/<path:path>', methods=['GET'])
def serve_react_app(path):
    file_path = os.path.join(static_file_dir, path)
    if os.path.isfile(file_path):
        return send_from_directory(static_file_dir, path)
    else:
        return send_from_directory(static_file_dir, 'index.html')

# Run the app
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)