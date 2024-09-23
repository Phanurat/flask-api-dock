from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # สำหรับ flash message

def get_db_connection():
    return mysql.connector.connect(
        host='db',
        user='root',
        password='1111',
        database='db'
    )

@app.route('/')
def index():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM comment;")
            comments = cursor.fetchall()
        return render_template('index.html', comments=comments)
    except Exception as e:
        return str(e)

@app.route('/api/comments', methods=['GET'])
def show_comments():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM comment;")
            comments = cursor.fetchall()
        return jsonify(comments)  # ส่งกลับข้อมูลในรูปแบบ JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create', methods=['GET', 'POST'])
def create_comment():
    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Content required!')
            return redirect(url_for('create_comment'))

        try:
            with get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO comment (content) VALUES (%s)", (content,))
                connection.commit()
            flash('Comment created successfully!')
            return redirect(url_for('index'))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('create_comment'))

    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_comment(id):
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM comment WHERE id = %s", (id,))
            comment = cursor.fetchone()

        if request.method == 'POST':
            new_content = request.form['content']
            if not new_content:
                flash('Content is required!')
                return redirect(url_for('edit_comment', id=id))

            with get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("UPDATE comment SET content = %s WHERE id = %s", (new_content, id))
                connection.commit()
            flash('Comment updated successfully!')
            return redirect(url_for('index'))

        return render_template('edit.html', comment=comment)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_comment(id):
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM comment WHERE id = %s", (id,))
            connection.commit()
        flash('Comment deleted successfully!')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
