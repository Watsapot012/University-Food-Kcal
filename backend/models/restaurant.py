"""
Restaurant model and database access functions.
Supports MySQL database with auto-reconnect, retry, and UTF-8 encoding support.
"""
import os
import time
import pymysql

def sanitize_data(item):
    """
    Auto-correct mojibake (e.g. à¸‚à¹‰à¸²à¸§ -> ข้าว)
    if database was populated or read with mismatched latin1 charset.
    """
    if isinstance(item, dict):
        return {k: sanitize_data(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [sanitize_data(v) for v in item]
    elif isinstance(item, str) and ('à¸' in item or 'à¹' in item):
        try:
            return item.encode('latin1').decode('utf-8')
        except Exception:
            return item
    return item

def get_db_connection(max_retries=10, delay=2):
    host = os.environ.get('MYSQL_HOST', 'localhost')
    user = os.environ.get('MYSQL_USER', 'root')
    password = os.environ.get('MYSQL_PASSWORD', 'rootpassword')
    database = os.environ.get('MYSQL_DB', 'university_food_kcal')
    port = int(os.environ.get('MYSQL_PORT', 3306))
    
    last_err = None
    for attempt in range(max_retries):
        try:
            return pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                charset='utf8mb4',
                use_unicode=True,
                init_command="SET NAMES utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
                connect_timeout=5
            )
        except Exception as e:
            last_err = e
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise last_err

class RestaurantModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM restaurants ORDER BY id ASC")
                rows = cursor.fetchall()
                return sanitize_data(rows)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(restaurant_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM restaurants WHERE id = %s", (restaurant_id,))
                row = cursor.fetchone()
                return sanitize_data(row)
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
