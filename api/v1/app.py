#!/usr/bin/python3
"""
3. Status of your API
The first endpoint that returns the status of your API
"""
from os import getenv
from flask import Flask as fl
from flask import jsonify as jsny
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

# App name and start
app = fl(__name__)
# Blueprint
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def pageNotFound(error):
    """Handels the 404 page"""
    badStat = {"error": "Not found"}
    return jsny(badStat), 404


@app.teardown_appcontext
def sessEnd(error):
    """Closes session to free up resources"""
    storage.close()


if __name__ == "__main__":
    if getenv("HBNB_API_HOST") and getenv("HBNB_API_PORT"):
        app.run(host=getenv("HBNB_API_HOST"),
                port=int(getenv("HBNB_API_PORT")), threaded=True)
    app.run(host="0.0.0.0", port=5000, threaded=True)
