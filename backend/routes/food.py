from flask import Blueprint, request, jsonify
from backend.models.food import FoodModel

food_bp = Blueprint('food', __name__, url_prefix='/api/foods')

@food_bp.route('', methods=['GET'])
def get_foods():
    try:
        search = request.args.get('search')
        restaurant_id = request.args.get('restaurant_id', type=int)
        min_kcal = request.args.get('min_kcal', type=int)
        max_kcal = request.args.get('max_kcal', type=int)
        sort_by = request.args.get('sort_by')

        foods = FoodModel.get_all(
            search=search,
            restaurant_id=restaurant_id,
            min_kcal=min_kcal,
            max_kcal=max_kcal,
            sort_by=sort_by
        )
        return jsonify(foods), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/<int:food_id>', methods=['GET'])
def get_food(food_id):
    try:
        food = FoodModel.get_by_id(food_id)
        if not food:
            return jsonify({"error": "ไม่พบรายการอาหารที่ระบุ"}), 404
        return jsonify(food), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/restaurant/<int:restaurant_id>', methods=['GET'])
def get_foods_by_restaurant(restaurant_id):
    try:
        foods = FoodModel.get_by_restaurant_id(restaurant_id)
        return jsonify(foods), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('', methods=['POST'])
def create_food():
    try:
        data = request.get_json() or {}
        if not data.get('name') or not data.get('restaurant_id'):
            return jsonify({"error": "กรุณาระบุชื่ออาหารและเลือกร้านอาหาร"}), 400

        new_food = FoodModel.create(data)
        return jsonify(new_food), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/<int:food_id>', methods=['PUT'])
def update_food(food_id):
    try:
        data = request.get_json() or {}
        existing = FoodModel.get_by_id(food_id)
        if not existing:
            return jsonify({"error": "ไม่พบรายการอาหารที่ต้องการแก้ไข"}), 404

        updated = FoodModel.update(food_id, data)
        return jsonify(updated), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    try:
        existing = FoodModel.get_by_id(food_id)
        if not existing:
            return jsonify({"error": "ไม่พบรายการอาหารที่ต้องการลบ"}), 404

        success = FoodModel.delete(food_id)
        return jsonify({"success": success, "message": "ลบรายการอาหารเรียบร้อยแล้ว"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/stats/summary', methods=['GET'])
def get_stats():
    try:
        stats = FoodModel.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
