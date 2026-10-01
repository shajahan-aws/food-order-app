import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)

# Environment variables se DB details read karna
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("POSTGRES_DB", "food_db")
DB_USER = os.environ.get("POSTGRES_USER", "food_user")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "food_pass")
DB_PORT = os.environ.get("DB_PORT", "5432")

def get_db_connection():
    # Retries for DB availability on startup
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                port=DB_PORT
            )
            return conn
        except psycopg2.OperationalError as e:
            retries -= 1
            print(f"DB not ready yet, retrying... ({retries} left). Error: {e}")
            time.sleep(3)
    raise Exception("Could not connect to PostgreSQL database.")

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            item_name VARCHAR(100) NOT NULL,
            quantity INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Initialize DB table on startup
try:
    init_db()
except Exception as e:
    print(f"Initial DB migration warning: {e}")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or 'item_name' not in data or 'quantity' not in data:
        return jsonify({"error": "Invalid request payload"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO orders (item_name, quantity) VALUES (%s, %s) RETURNING id, item_name, quantity, created_at;",
        (data['item_name'], data['quantity'])
    )
    new_order = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Order created successfully", "order": new_order}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM orders;")
    orders = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({"orders": orders}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)