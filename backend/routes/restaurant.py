from flask import Blueprint, request, jsonify
from backend.models.restaurant import RestaurantModel

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/api/restaurants')

@restaurant_bp.route('', methods=['GET'])
def get_restaurants():
    try:
        restaurants = RestaurantModel.get_all()
        return jsonify(restaurants), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurant_bp.route('/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    try:
        restaurant = RestaurantModel.get_by_id(restaurant_id)
        if not restaurant:
            return jsonify({"error": "ไม่พบร้านอาหารที่ระบุ"}), 404
        return jsonify(restaurant), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurant_bp.route('', methods=['POST'])
def create_restaurant():
    try:
        data = request.get_json() or {}
        if not data.get('name') or not data.get('location'):
            return jsonify({"error": "กรุณากรอกชื่อร้านและตำแหน่งสถานที่ตั้ง"}), 400

        new_restaurant = RestaurantModel.create(data)
        return jsonify(new_restaurant), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurant_bp.route('/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    try:
        data = request.get_json() or {}
        existing = RestaurantModel.get_by_id(restaurant_id)
        if not existing:
            return jsonify({"error": "ไม่พบร้านอาหารที่ต้องการแก้ไข"}), 404

        updated = RestaurantModel.update(restaurant_id, data)
        return jsonify(updated), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurant_bp.route('/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    try:
        existing = RestaurantModel.get_by_id(restaurant_id)
        if not existing:
            return jsonify({"error": "ไม่พบร้านอาหารที่ต้องการลบ"}), 404

        success = RestaurantModel.delete(restaurant_id)
        return jsonify({"success": success, "message": "ลบร้านอาหารเรียบร้อยแล้ว"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
