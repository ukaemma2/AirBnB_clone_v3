#!/usr/bin/python3
"""App.py for api v1"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Teardown application context
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Error returned when page not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """Main function"""
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
