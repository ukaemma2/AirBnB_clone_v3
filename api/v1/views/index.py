#!/usr/bin/python3
"""index.py for api status"""
from flask import jsonify
from . import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """Return API Status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Return stats"""
    classes = [Amenity, City, Place, Review, State, User]
    cls_names = ["amenities", "cities",
                 "places", "reviews",
                 "states", "users"]
    stats = {}
    for cls in range(len(classes)):
        stats[cls_names[cls]] = storage.count(classes[cls])

    return jsonify(stats)
