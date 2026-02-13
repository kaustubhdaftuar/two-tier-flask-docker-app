from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.route("/")
def home():
    return jsonify({"message": "Two-Tier Flask App Running"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (%s, %s)",
        (data["title"], data["description"])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Task created"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
