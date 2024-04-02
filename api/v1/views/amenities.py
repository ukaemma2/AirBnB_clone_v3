#!/usr/bin/python3
"""API definition for the Amenity object"""
from api.v1.views import app_views
from flask import jsonify as jsny, abort, request as req
from models import storage


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def amenity_methods(amenity_id=None):
    """
    Handle requests to API for amentities
    """
    from models.amenity import Amenity
    fullList = storage.all(Amenity)

    # Using HTTP GET
    if req.method == "GET":
        if not amenity_id:
            # return jsonify([obj.to_dict() for obj in fullList.values()])
            data = []
            for name in fullList.values():
                entry = name.to_dict()
                data.append(entry)
            return jsny(data)

        seek = "Amenity." + amenity_id
        try:
            # return jsonify(fullList[seek].to_dict())
            data = fullList[seek].to_dict()
            return jsny(data)
        except KeyError:
            abort(404)

    # Using HTTP DELETE
    elif req.method == "DELETE":
        try:
            seek = "Amenity." + amenity_id
            storage.delete(fullList[seek])
            storage.save()
            emptData = {}
            return jsny(emptData), 200
        except Exception:
            abort(404)

    # Using HTTP POST
    elif req.method == "POST":
        if req.is_json:
            new = req.get_json()
        else:
            abort(400, "Not a JSON")

        # instantiate, store, and return new Amenity object
        if "name" in new:
            newAmen = Amenity(**new)
            storage.new(newAmen)
            storage.save()
            data = newAmen.to_dict()
            # return jsonify(newAmen.to_dict()), 201
            return jsny(data), 201
        else:
            abort(400, "Missing name")

    # Using HTTP PUT
    elif req.method == "PUT":
        seek = "Amenity." + amenity_id
        try:
            toEdit = fullList[seek]
            if req.is_json:
                edit = req.get_json()
            else:
                abort(400, "Not a JSON")

            for key, valu in edit.items():
                if (seek != "id" and seek != "created_at"
                   and seek != "updated_at"):
                    setattr(toEdit, key, valu)

            storage.save()
            data = toEdit.to_dict()
            return jsny(data), 200
        except KeyError:
            abort(404)

    else:
        abort(501)
