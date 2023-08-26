from flask import Blueprint, jsonify, request
from models import City, Place  # Import your City and Place models
from app import app  # Import your Flask app instance

places_blueprint = Blueprint('places', __name__)


@places_blueprint.route('/api/v1/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    city = City.get(city_id)
    if city is None:
        return jsonify({'error': 'City not found'}), 404

    places = city.places
    places_json = [place.to_dict() for place in places]
    return jsonify(places_json), 200


@places_blueprint.route('/api/v1/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = Place.get(place_id)
    if place is None:
        return jsonify({'error': 'Place not found'}), 404

    return jsonify(place.to_dict()), 200


@places_blueprint.route('/api/v1/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = Place.get(place_id)
    if place is None:
        return jsonify({'error': 'Place not found'}), 404

    place.delete()  # Implement the delete method on your Place model
    return jsonify({}), 200


@places_blueprint.route('/api/v1/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    city = City.get(city_id)
    if city is None:
        return jsonify({'error': 'City not found'}), 404

    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400

    user_id = data['user_id']
    user = User.get(user_id)  # Implement the User model and get method
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    new_place = Place.create(city_id=city_id,
                             user_id=user_id, name=data['name'])
    return jsonify(new_place.to_dict()), 201


@places_blueprint.route('/api/v1/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = Place.get(place_id)
    if place is None:
        return jsonify({'error': 'Place not found'}), 404

    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)

    place.save()  # Implement the save method on your Place model
    return jsonify(place.to_dict()), 200
