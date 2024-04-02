#!/usr/bin/python3
"""The link between Place API and the Amenity API"""
from api.v1.views import app_views
from flask import jsonify as jsny, abort, request as req
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=["GET", "DELETE", "POST"],
                 strict_slashes=False)
def link(place_id=None, amenity_id=None):
    """
     - GET: Retrieves the list of all Amenity if place ID is passed.
            Or a specific object if it is passed.
     - DELETE: Remove an object. Or returns error code if other.
     - POST: Adds new object if a link exsists.
             Returns error code if other
    """
    editType = getenv('HBNB_TYPE_STORAGE')
    # Using HTTP GET
    if req.method == "GET":
        # Select the correct place
        seek = storage.get(Place, place_id)
        if not seek:
            # No such place
            abort(404)
        data = []
        for name in seek.amenities:
            entry = name.to_dict()
            data.append(entry)
        return jsny(data)

    # Using HTTP DELETE
    elif req.method == "DELETE":
        # Pulling objects
        seekPlac = storage.get(Place, place_id)
        seekAmen = storage.get(Amenity, amenity_id)
        # One of them is not found
        if not seekPlac or not seekPlac:
            abort(404)
        if editType == "db":
            storage.delete(seekAmen)
        seekPlac.amenity_id.remove('Amenity.' + amenity_id)
        storage.save()
        emptData = {}
        return jsny(emptData), 200

    # Using HTTP POST
    elif req.method == "POST":
        # Pulling objects
        seekPlac = storage.get(Place, place_id)
        seekAmen = storage.get(Amenity, amenity_id)
        # One of them is not found
        if not seekPlac or not seekPlac:
            abort(404)
        if seekAmen in seekPlac.amenities:
            data = seekAmen.to_dict()
            return jsonify(data), 200
        if editType != 'db':
            seekPlac.amenity_ids.append('Amenity.' + amenity_id)
        else:
            seekPlac.amenities.append(amenity)
        storage.save()
        data = seekAmen.to_dict()
        return jsny(data), 201

    else:
        abort(501)
