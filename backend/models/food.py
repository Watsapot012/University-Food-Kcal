"""
Food model and database access functions.
Supports nutrition information and filtering.
"""
from backend.models.restaurant import get_db_connection

class FoodModel:
    @staticmethod
    def get_all(search=None, restaurant_id=None, min_kcal=None, max_kcal=None, sort_by=None):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT f.*, r.name as restaurant_name 
                    FROM foods f 
                    LEFT JOIN restaurants r ON f.restaurant_id = r.id 
                    WHERE 1=1
                """
                params = []

                if search:
                    query += " AND (f.name LIKE %s OR r.name LIKE %s OR f.description LIKE %s)"
                    wildcard = f"%{search}%"
                    params.extend([wildcard, wildcard, wildcard])

                if restaurant_id:
                    query += " AND f.restaurant_id = %s"
                    params.append(restaurant_id)

                if min_kcal is not None:
                    query += " AND f.kcal >= %s"
                    params.append(min_kcal)

                if max_kcal is not None:
                    query += " AND f.kcal <= %s"
                    params.append(max_kcal)

                if sort_by == 'kcal_asc':
                    query += " ORDER BY f.kcal ASC"
                elif sort_by == 'kcal_desc':
                    query += " ORDER BY f.kcal DESC"
                elif sort_by == 'price_asc':
                    query += " ORDER BY f.price ASC"
                elif sort_by == 'price_desc':
                    query += " ORDER BY f.price DESC"
                else:
                    query += " ORDER BY f.id ASC"

                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_by_id(food_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT f.*, r.name as restaurant_name 
                    FROM foods f 
                    LEFT JOIN restaurants r ON f.restaurant_id = r.id 
                    WHERE f.id = %s
                """
                cursor.execute(query, (food_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_by_restaurant_id(restaurant_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT f.*, r.name as restaurant_name 
                    FROM foods f 
                    LEFT JOIN restaurants r ON f.restaurant_id = r.id 
                    WHERE f.restaurant_id = %s
                    ORDER BY f.id ASC
                """
                cursor.execute(query, (restaurant_id,))
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def create(data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO foods (name, restaurant_id, price, kcal, protein, carbohydrate, fat, image, description, category, is_popular)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    data.get('name'),
                    data.get('restaurant_id'),
                    data.get('price', 0),
                    data.get('kcal', 0),
                    data.get('protein', 0.0),
                    data.get('carbohydrate', 0.0),
                    data.get('fat', 0.0),
                    data.get('image', ''),
                    data.get('description', ''),
                    data.get('category', 'อาหารจานเดียว'),
                    data.get('is_popular', False)
                ))
                new_id = cursor.lastrowid
                return FoodModel.get_by_id(new_id)
        finally:
            conn.close()

    @staticmethod
    def update(food_id, data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE foods 
                    SET name = %s, restaurant_id = %s, price = %s, kcal = %s, 
                        protein = %s, carbohydrate = %s, fat = %s, image = %s, 
                        description = %s, category = %s, is_popular = %s
                    WHERE id = %s
                """
                cursor.execute(sql, (
                    data.get('name'),
                    data.get('restaurant_id'),
                    data.get('price', 0),
                    data.get('kcal', 0),
                    data.get('protein', 0.0),
                    data.get('carbohydrate', 0.0),
                    data.get('fat', 0.0),
                    data.get('image', ''),
                    data.get('description', ''),
                    data.get('category', 'อาหารจานเดียว'),
                    data.get('is_popular', False),
                    food_id
                ))
                return FoodModel.get_by_id(food_id)
        finally:
            conn.close()

    @staticmethod
    def delete(food_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM foods WHERE id = %s", (food_id,))
                return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def get_stats():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as total_restaurants FROM restaurants")
                total_restaurants = cursor.fetchone()['total_restaurants']

                cursor.execute("SELECT COUNT(*) as total_foods, AVG(kcal) as avg_kcal FROM foods")
                foods_summary = cursor.fetchone()

                cursor.execute("SELECT * FROM foods ORDER BY kcal DESC LIMIT 1")
                max_food = cursor.fetchone()

                cursor.execute("SELECT * FROM foods WHERE kcal > 0 ORDER BY kcal ASC LIMIT 1")
                min_food = cursor.fetchone()

                return {
                    "total_restaurants": total_restaurants,
                    "total_foods": foods_summary['total_foods'] if foods_summary else 0,
                    "avg_kcal": round(float(foods_summary['avg_kcal'] or 0), 1) if foods_summary else 0,
                    "max_kcal_food": max_food,
                    "min_kcal_food": min_food
                }
        finally:
            conn.close()
