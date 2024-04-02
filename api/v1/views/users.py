#!/usr/bin/python3
'''User View'''
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def listUsers():
    """list of users"""
    objs = storage.all(User)
    return jsonify([user.to_dict() for user in objs.values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def getUSer(user_id):
    """get specefic User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteUser(user_id):
    """delete User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def newUser():
    """new User"""
    usr = request.get_json()
    if not usr:
        abort(400, "Not a JSON")
    if 'email' not in usr:
        abort(400, "Missing email")
    if 'password' not in usr:
        abort(400, 'Missing password')
    user = User(**usr)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def uodateUser(user_id):
    """update specvefic user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    reques = request.get_json()
    if not reques:
        abort(400, "Not a JSON")
    for key, value in reques.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
