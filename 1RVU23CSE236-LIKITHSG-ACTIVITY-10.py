from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('courses.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS courses
                (id INTEGER PRIMARY KEY, name TEXT NOT NULL, instructor TEXT NOT NULL, time TEXT NOT NULL, price REAL NOT NULL)''')
conn.commit()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM courses LIMIT 1")
    course = cursor.fetchone()
    return render_template('index.html', course=course)

@app.route('/courses')
def courses():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return render_template('courses.html', courses=courses)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form['course_name']
        instructor = request.form['course_instructor']
        time = request.form['course_time']
        price = request.form['course_price']
        cursor.execute("INSERT INTO courses (name, instructor, time, price) VALUES (?, ?, ?, ?)", (name, instructor, time, price))
        conn.commit()
        return redirect(url_for('courses'))
    return render_template('add_course.html')

@app.route('/update_course/<int:id>', methods=['GET', 'POST'])
def update_course(id):
    if request.method == 'POST':
        name = request.form['course_name']
        instructor = request.form['course_instructor']
        time = request.form['course_time']
        price = request.form['course_price']
        cursor.execute("UPDATE courses SET name=?, instructor=?, time=?, price=? WHERE id=?", (name, instructor, time, price, id))
        conn.commit()
        return redirect(url_for('courses'))
    cursor.execute("SELECT * FROM courses WHERE id=?", (id,))
    course = cursor.fetchone()
    return render_template('update_course.html', course=course)

@app.route('/delete_course/<int:id>', methods=['POST'])
def delete_course(id):
    cursor.execute("DELETE FROM courses WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for('courses'))

if __name__ == '__main__':
    app.run(debug=True)
