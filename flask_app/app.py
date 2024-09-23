from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # สำหรับ flash message

# ฟังก์ชันสำหรับเชื่อมต่อกับฐานข้อมูล
def get_db_connection():
    return mysql.connector.connect(
        host='db',  # หรือ 'localhost' ถ้าไม่ได้ใช้ Docker
        user='root',
        password='1111',
        database='db'
    )

# หน้าแรก - แสดงรายการ comment ทั้งหมด (Read)
@app.route('/')
def index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM comment;")
        comments = cursor.fetchall()
        return render_template('index.html', comments=comments)
    except Exception as e:
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# สร้าง comment ใหม่ (Create)
@app.route('/create', methods=['GET', 'POST'])
def create_comment():
    if request.method == 'POST':
        content = request.form['content']
        user_id = request.form['user_id']

        if not content or not user_id:
            flash('Content and User ID are required!')
            return redirect(url_for('create_comment'))

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO comment (content, user_id) VALUES (%s, %s)", (content, user_id))
            connection.commit()
            flash('Comment created successfully!')
            return redirect(url_for('index'))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('create_comment'))
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    return render_template('create.html')

# แก้ไข comment (Update)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_comment(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM comment WHERE id = %s", (id,))
        comment = cursor.fetchone()

        if request.method == 'POST':
            new_content = request.form['content']
            if not new_content:
                flash('Content is required!')
                return redirect(url_for('edit_comment', id=id))

            cursor.execute("UPDATE comment SET content = %s WHERE id = %s", (new_content, id))
            connection.commit()
            flash('Comment updated successfully!')
            return redirect(url_for('index'))

        return render_template('edit.html', comment=comment)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ลบ comment (Delete)
@app.route('/delete/<int:id>', methods=['POST'])
def delete_comment(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM comment WHERE id = %s", (id,))
        connection.commit()
        flash('Comment deleted successfully!')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
