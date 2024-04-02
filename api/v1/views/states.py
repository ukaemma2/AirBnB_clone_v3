#!/usr/bin/python3
"""
6. State
  - Contains the API setup for the State object.
"""
from api.v1.views import app_views
from flask import abort
from flask import request as req
import json
from flask import jsonify as jsny
from models import storage


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def stateEdit(state_id=None):
    """
    Edit the State objects according to the specified HTTP method:
      - GET: Retrieves the list of all State objects.
             Or one object if ID is passed.
      - DELETE: Deletes object what have the passed ID.
                Or returns 404 page if no ID passed.
      - POST: Add a new state object if name provided.
              Returns error code if not.
      - PUT: Update object if name provided.
             Returns error code if not.
    """
    # Importing needed files
    from models.state import State
    # All states objects
    fullList = storage.all(State)

    # Using HTTP GET
    if req.method == "GET":
        if not state_id:
            # Getting a State at a time
            data = []
            for name in fullList.values():
                entry = name.to_dict()
                data.append(entry)
            # return (json.dumps(data, indent=2, sort_keys=True),
            #        {"Content-Type": "application/json"})
            return jsny(data)
        seek = "State." + state_id
        try:
            data = fullList[seek].to_dict()
            return jsny(data)
        except KeyError:
            abort(404)

    # Using HTTP DELETE
    elif req.method == "DELETE":
        try:
            seek = "State." + state_id
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
        if "name" in new:
            newState = State(**new)
            storage.new(newState)
            storage.save()
            data = newState.to_dict()
            return jsny(data), 201
        else:
            abort(400, "Missing name")

    # Using HTTP PUT
    elif req.method == "PUT":
        seek = "State." + state_id
        try:
            found = fullList[seek]
            if req.is_json:
                toEdit = req.get_json()
            else:
                abort(400, "Not a JSON")
            for key, valu in new.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(found, key, valu)
            storage.save()
            data = found.to_dict()
            return jsny(data), 200
        except KeyError:
            abort(404)

    else:
        abort(501)
