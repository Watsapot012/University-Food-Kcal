"""
Flask Application Entry Point for University Food Kcal
"""
import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Ensure root directory is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

from backend.routes.restaurant import restaurant_bp
from backend.routes.food import food_bp
from backend.models.food import FoodModel

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register Blueprints
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(food_bp)

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "online",
            "service": "University Food Kcal API",
            "version": "1.0.0"
        }), 200

    @app.route('/api/stats', methods=['GET'])
    def system_stats():
        try:
            stats = FoodModel.get_stats()
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

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
    app.run(host=host, port=port, debug=True)
