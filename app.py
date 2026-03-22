from flask import Flask, render_template,request,redirect
import mysql.connector as connector
import db_config
db = connector.connect(
    host=db_config.HOST,
    user=db_config.USER,
    password=db_config.PASSWORD,
    database=db_config.DATABASE
)
cursor = db.cursor()
app = Flask(__name__,template_folder='frontend/templates',static_folder='frontend/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/students')
def students():
    cursor.execute("SELECT * FROM Student")
    data = cursor.fetchall()
    return render_template('students.html',students=data)

@app.route('/courses')
def courses():
    cursor.execute("SELECT * FROM Course")
    data = cursor.fetchall()
    return render_template('courses.html', courses=data)

@app.route('/marks')
def marks():
    cursor.execute("SELECT * FROM Marks")
    data = cursor.fetchall()
    return render_template('marks.html', marks=data)

@app.route('/attendance')
def attendance():
    cursor.execute("SELECT * FROM Attendance")
    data = cursor.fetchall()
    return render_template('attendance.html', attendance=data)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    studentID = request.form['studentID']
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']
    deptID = request.form['deptID']

    query = """
    INSERT INTO Student (StudentID, Name, Age, Phone, DeptID)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (studentID, name, age, phone, deptID)

    cursor.execute(query, values)
    db.commit()

    return redirect('/students')

@app.route('/add_course', methods=['POST'])
def add_course():
    courseID = request.form['courseID']
    courseName = request.form['courseName']
    deptID = request.form['deptID']

    query = "INSERT INTO Course (CourseID, CourseName, DeptID) VALUES (%s, %s, %s)"
    values = (courseID, courseName, deptID)

    cursor.execute(query, values)
    db.commit()

    return redirect('/courses')

@app.route('/add_marks', methods=['POST'])
def add_marks():
    studentID = request.form['studentID']
    courseID = request.form['courseID']
    marks = request.form['marks']

    cursor.execute("SELECT * FROM Student WHERE StudentID = %s", (studentID,))
    student = cursor.fetchone()

    if not student:
        cursor.execute("SELECT * FROM Marks")
        data = cursor.fetchall()
        return render_template('marks.html', marks=data, error="Invalid Student ID!")

    cursor.execute("SELECT * FROM Course WHERE CourseID = %s", (courseID,))
    course = cursor.fetchone()

    if not course:
        cursor.execute("SELECT * FROM Marks")
        data = cursor.fetchall()
        return render_template('marks.html', marks=data, error="Invalid Course ID!")

    query = "INSERT INTO Marks (StudentID, CourseID, Marks) VALUES (%s, %s, %s)"
    values = (studentID, courseID, marks)

    cursor.execute(query, values)
    db.commit()

    return redirect('/marks')

@app.route('/add_attendance', methods=['POST'])
def add_attendance():
    studentID = request.form['studentID']
    date = request.form['date']
    status = request.form['status']

    query = "INSERT INTO Attendance (StudentID, Date, Status) VALUES (%s, %s, %s)"
    values = (studentID, date, status)

    cursor.execute(query, values)
    db.commit()

    return redirect('/attendance')

@app.route('/search_results', methods=['POST'])
def search_results():
    name = request.form.get('name')
    studentID = request.form.get('studentID')
    deptID = request.form.get('deptID')
    marks = request.form.get('marks')

    # Main query with attendance subquery
    query = """
    SELECT 
        s.StudentID,
        s.Name,
        s.Age,
        s.Phone,
        d.DeptName,
        c.CourseName,
        m.Marks,
        IFNULL(a.AttendancePercent, 0) AS AttendancePercent
    FROM Student s
    JOIN Department d ON s.DeptID = d.DeptID
    LEFT JOIN Marks m ON s.StudentID = m.StudentID
    LEFT JOIN Course c ON m.CourseID = c.CourseID
    LEFT JOIN (
        SELECT StudentID,
               ROUND(SUM(CASE WHEN Status='Present' THEN 1 ELSE 0 END) 
                     / COUNT(AttendID) * 100, 2) AS AttendancePercent
        FROM Attendance
        GROUP BY StudentID
    ) a ON s.StudentID = a.StudentID
    WHERE 1=1
    """

    values = []

    if name:
        query += " AND s.Name LIKE %s"
        values.append(f"%{name}%")
    if studentID:
        query += " AND s.StudentID = %s"
        values.append(studentID)
    if deptID:
        query += " AND s.DeptID = %s"
        values.append(deptID)
    if marks:
        query += " AND m.Marks >= %s"
        values.append(marks)

    cursor.execute(query, tuple(values))
    data = cursor.fetchall()

    return render_template('search.html', results=data)
@app.route('/edit_student/<int:id>')
def edit_student(id):
    cursor.execute("SELECT * FROM Student WHERE StudentID = %s", (id,))
    student = cursor.fetchone()
    return render_template('edit_student.html', student=student)

@app.route('/update_student', methods=['POST'])
def update_student():
    studentID = request.form['studentID']
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']
    deptID = request.form['deptID']

    query = """
    UPDATE Student 
    SET Name=%s, Age=%s, Phone=%s, DeptID=%s
    WHERE StudentID=%s
    """

    values = (name, age, phone, deptID, studentID)

    cursor.execute(query, values)
    db.commit()

    return redirect('/students')

@app.route('/delete_mark/<int:id>')
def delete_mark(id):
    cursor.execute("DELETE FROM Marks WHERE MarkID = %s", (id,))
    db.commit()
    return redirect('/marks')

if __name__ == '__main__':
    app.run(debug=True)
