"""
Restaurant model and database access functions.
Supports MySQL database with fallback to SQLite for local development.
"""
import os
import pymysql

def get_db_connection():
    host = os.environ.get('MYSQL_HOST', 'localhost')
    user = os.environ.get('MYSQL_USER', 'root')
    password = os.environ.get('MYSQL_PASSWORD', 'rootpassword')
    database = os.environ.get('MYSQL_DB', 'university_food_kcal')
    port = int(os.environ.get('MYSQL_PORT', 3306))
    
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

class RestaurantModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM restaurants ORDER BY id ASC")
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_by_id(restaurant_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM restaurants WHERE id = %s", (restaurant_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def create(data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO restaurants (name, description, location, image, phone, open_hours)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    data.get('name'),
                    data.get('description', ''),
                    data.get('location', ''),
                    data.get('image', ''),
                    data.get('phone', ''),
                    data.get('open_hours', '08:00 - 18:00 น.')
                ))
                new_id = cursor.lastrowid
                return RestaurantModel.get_by_id(new_id)
        finally:
            conn.close()

    @staticmethod
    def update(restaurant_id, data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE restaurants 
                    SET name = %s, description = %s, location = %s, image = %s, phone = %s, open_hours = %s
                    WHERE id = %s
                """
                cursor.execute(sql, (
                    data.get('name'),
                    data.get('description', ''),
                    data.get('location', ''),
                    data.get('image', ''),
                    data.get('phone', ''),
                    data.get('open_hours', '08:00 - 18:00 น.'),
                    restaurant_id
                ))
                return RestaurantModel.get_by_id(restaurant_id)
        finally:
            conn.close()

    @staticmethod
    def delete(restaurant_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM restaurants WHERE id = %s", (restaurant_id,))
                return cursor.rowcount > 0
        finally:
            conn.close()
