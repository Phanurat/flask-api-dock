from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# ฟังก์ชันสำหรับเชื่อมต่อกับฐานข้อมูล
def get_db_connection():
    return mysql.connector.connect(
        host='db',  # หรือใช้ 'localhost' หากไม่ได้ใช้ Docker
        user='root',
        password='1111',
        database='db'
    )

@app.route('/')
def index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        return f"Connected to database: {db_name[0]}"
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/comments', methods=['GET'])
def get_comments():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM comment;")  # เรียกข้อมูลจากตาราง comment
        comments = cursor.fetchall()
        return jsonify(comments)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/cookies', methods=['GET'])
def get_cookies():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cookies;")  # เรียกข้อมูลจากตาราง comment
        cookies = cursor.fetchall()
        return jsonify(cookies)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
