#!/usr/bin/python3
'''the city'''
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getCities(state_id):
    """getListOfcityes in state"""
    sta = storage.get(State, state_id)
    if not sta:
        abort(404)
    return jsonify([c.to_dict() for c in sta.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getCity(city_id):
    """get city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteCity(city_id):
    """delet City and returb emoty"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def newCity(state_id):
    """newCity"""
    sta = storage.get(State, state_id)
    if not sta:
        abort(404)
    cityy = request.get_json()
    if not cityy:
        abort(400, "Not a JSON")
    if 'name' not in cityy:
        abort(400, "Missing name")

    c = City(**cityy)
    setattr(c, 'state_id', state_id)
    storage.new(c)
    storage.save()
    return make_response(jsonify(c.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """mettre a joure city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    reques = request.get_json()
    if not reques:
        abort(400, "Not a JSON")
    for key, value in reques.items():
        if key not in ['id', 'created_at', 'update_at', 'state_id']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
