"""
Flask Application Entry Point for University Food Kcal
"""
import os
import sys
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Ensure root directory and backend directory are both on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

load_dotenv()

try:
    from backend.routes.restaurant import restaurant_bp
    from backend.routes.food import food_bp
    from backend.models.food import FoodModel
    from backend.models.restaurant import get_db_connection
except ImportError:
    from routes.restaurant import restaurant_bp
    from routes.food import food_bp
    from models.food import FoodModel
    from models.restaurant import get_db_connection

def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json; charset=utf-8"
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def set_utf8_charset(response):
        if response.mimetype == 'application/json':
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    # Register Blueprints
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(food_bp)

    @app.route('/api/health', methods=['GET'])
    def health_check():
        db_status = "connected"
        try:
            conn = get_db_connection(max_retries=1, delay=0.5)
            conn.close()
        except Exception as e:
            db_status = f"database_connecting ({str(e)})"

        return jsonify({
            "status": "online",
            "service": "University Food Kcal API (Flask + MySQL)",
            "database": db_status,
            "version": "1.0.0"
        }), 200

    @app.route('/api/stats', methods=['GET'])
    def system_stats():
        try:
            stats = FoodModel.get_stats()
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Menu compatibility endpoints
    @app.route('/api/menu/<int:restaurant_id>', methods=['GET'])
    def get_menu(restaurant_id):
        try:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM restaurants WHERE id = %s", (restaurant_id,))
                    restaurant = cursor.fetchone()
                    cursor.execute("SELECT * FROM foods WHERE restaurant_id = %s", (restaurant_id,))
                    dishes = cursor.fetchall()
                    return jsonify({
                        "restaurant": restaurant,
                        "dishes": dishes
                    }), 200
            finally:
                conn.close()
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/menu/item/<int:dish_id>', methods=['GET'])
    def get_menu_item(dish_id):
        try:
            food = FoodModel.get_by_id(dish_id)
            if not food:
                return jsonify({"error": "ไม่พบเมนู"}), 404
            return jsonify(food), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Auth endpoints
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        data = request.get_json() or {}
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        if not name or not email or not password:
            return jsonify({"error": "กรุณากรอกข้อมูลให้ครบถ้วน"}), 400

        try:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id FROM users WHERE email = %s", (email.strip().lower(),))
                    if cursor.fetchone():
                        return jsonify({"error": "อีเมลนี้ถูกใช้งานแล้วในระบบ"}), 400

                    avatar = f"https://api.dicebear.com/7.x/bottts/svg?seed={email.strip().lower()}"
                    cursor.execute(
                        "INSERT INTO users (name, email, password_hash, avatar) VALUES (%s, %s, %s, %s)",
                        (name.strip(), email.strip().lower(), password, avatar)
                    )
                    user_id = cursor.lastrowid
                    cursor.execute(
                        "INSERT INTO profiles (user_id, weight, height, age, gender, activity, bmr, tdee, calories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (user_id, 60, 170, 20, 'male', 1.375, 1545, 2124, 2000)
                    )
                    return jsonify({
                        "message": "สมัครสมาชิกสำเร็จ",
                        "token": f"token-{user_id}-{int(time.time()*1000)}",
                        "user": {
                            "id": user_id,
                            "name": name.strip(),
                            "email": email.strip().lower(),
                            "avatar": avatar
                        }
                    }), 201
            finally:
                conn.close()
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        if not email or not password:
            return jsonify({"error": "กรุณากรอกอีเมลและรหัสผ่าน"}), 400

        try:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                    user = cursor.fetchone()
                    if not user or user['password_hash'] != password:
                        return jsonify({"error": "อีเมลหรือรหัสผ่านไม่ถูกต้อง"}), 401

                    return jsonify({
                        "message": "เข้าสู่ระบบสำเร็จ",
                        "token": f"token-{user['id']}-{int(time.time()*1000)}",
                        "user": {
                            "id": user['id'],
                            "name": user['name'],
                            "email": user['email'],
                            "avatar": user.get('avatar')
                        }
                    }), 200
            finally:
                conn.close()
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/auth/me', methods=['GET'])
    def auth_me():
        auth_header = request.headers.get('Authorization', '')
        user_id = 1
        if 'token-' in auth_header:
            try:
                user_id = int(auth_header.split('token-')[1].split('-')[0])
            except Exception:
                user_id = 1

        try:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, name, email, avatar FROM users WHERE id = %s", (user_id,))
                    user = cursor.fetchone()
                    if not user:
                        return jsonify({"error": "ไม่พบผู้ใช้งาน"}), 404
                    return jsonify(user), 200
            finally:
                conn.close()
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Profile endpoints
    @app.route('/api/profile', methods=['GET', 'POST'])
    def profile():
        user_id = request.args.get('userId', default=1, type=int)
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if request.method == 'POST':
                    data = request.get_json() or {}
                    u_id = data.get('userId', user_id)
                    weight = data.get('weight', 60)
                    height = data.get('height', 170)
                    age = data.get('age', 20)
                    gender = data.get('gender', 'male')
                    activity = data.get('activity', 1.2)
                    bmr = data.get('bmr', 1500)
                    tdee = data.get('tdee', 2000)
                    calories = data.get('calories', 2000)

                    cursor.execute("""
                        INSERT INTO profiles (user_id, weight, height, age, gender, activity, bmr, tdee, calories)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        weight=%s, height=%s, age=%s, gender=%s, activity=%s, bmr=%s, tdee=%s, calories=%s
                    """, (u_id, weight, height, age, gender, activity, bmr, tdee, calories,
                          weight, height, age, gender, activity, bmr, tdee, calories))
                    return jsonify({"success": True}), 200

                cursor.execute("SELECT * FROM profiles WHERE user_id = %s", (user_id,))
                p = cursor.fetchone()
                if not p:
                    p = {
                        "weight": 65, "height": 175, "age": 21,
                        "gender": "male", "activity": 1.55,
                        "bmr": 1650, "tdee": 2558, "calories": 2000
                    }
                return jsonify(p), 200
        finally:
            conn.close()

    # Meal logs endpoints
    @app.route('/api/logs', methods=['GET', 'POST'])
    def meal_logs():
        user_id = request.args.get('userId', default=1, type=int)
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if request.method == 'POST':
                    data = request.get_json() or {}
                    u_id = data.get('userId', user_id)
                    log_id = f"log-{int(time.time()*1000)}"
                    name = data.get('name')
                    calories = data.get('calories', 0)
                    meal_type = data.get('type', 'lunch')
                    timestamp = time.strftime('%H:%M น.')
                    protein = data.get('protein', 0.0)
                    carbs = data.get('carbs', 0.0)
                    fat = data.get('fat', 0.0)

                    cursor.execute("""
                        INSERT INTO meal_logs (id, user_id, name, calories, type, timestamp, protein, carbs, fat)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (log_id, u_id, name, calories, meal_type, timestamp, protein, carbs, fat))
                    return jsonify({
                        "id": log_id, "name": name, "calories": calories,
                        "type": meal_type, "timestamp": timestamp,
                        "protein": protein, "carbs": carbs, "fat": fat
                    }), 201

                cursor.execute("SELECT * FROM meal_logs WHERE user_id = %s ORDER BY created_at ASC", (user_id,))
                meals = cursor.fetchall()
                total_cal = sum(m.get('calories', 0) for m in meals)
                total_pro = sum(float(m.get('protein', 0.0)) for m in meals)
                total_car = sum(float(m.get('carbs', 0.0)) for m in meals)
                total_fat = sum(float(m.get('fat', 0.0)) for m in meals)

                return jsonify({
                    "meals": meals,
                    "totalCalories": total_cal,
                    "totalProtein": round(total_pro, 1),
                    "totalCarbs": round(total_car, 1),
                    "totalFat": round(total_fat, 1)
                }), 200
        finally:
            conn.close()

    @app.route('/api/logs/<string:log_id>', methods=['DELETE'])
    def delete_log(log_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM meal_logs WHERE id = %s", (log_id,))
                return jsonify({"success": True, "message": "ลบรายการอาหารเรียบร้อยแล้ว"}), 200
        finally:
            conn.close()

    # Reset endpoint
    @app.route('/api/reset', methods=['POST'])
    def reset_data():
        return jsonify({"message": "รีเซ็ตข้อมูลเริ่มต้นสำเร็จ"}), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5000))
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    print(f"🚀 University Food Kcal Flask server running on http://{host}:{port}")
    app.run(host=host, port=port, debug=False)
