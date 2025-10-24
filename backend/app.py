from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database connection
db = mysql.connector.connect(
    host="mysql_db",  # Docker service name
    user="root",
    password="root",
    database="todo_db"
)
cursor = db.cursor(dictionary=True)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    cursor.execute("SELECT * FROM task ORDER BY id DESC LIMIT 5")
    return jsonify(cursor.fetchall())

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    cursor.execute("INSERT INTO task (title, description, completed) VALUES (%s, %s, %s)",
                   (data['title'], data['description'], False))
    db.commit()
    return jsonify({"message": "Task added"}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def mark_done(id):
    cursor.execute("UPDATE task SET completed = TRUE WHERE id = %s", (id,))
    db.commit()
    return jsonify({"message": "Task marked done"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
