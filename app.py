from flask import Flask, render_template, request, redirect, url_for
from models import db, Student, Professor, Course
import os

app = Flask(__name__)

# Update the URI for PostgreSQL (replace with your credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pgadmin_database_user:4TBcyPjYqry6dvfQFSqbuxvDmq1bjECY@dpg-cuas0pogph6c73a1qvgg-a.oregon-postgres.render.com:5432/pgadmin_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to add student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    # Fetch all courses for the department dropdown
    courses = Course.query.all()

    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        age = int(request.form['age'])
        department = request.form['department']
        
        # Check if the student ID already exists
        existing_student = Student.query.filter_by(id=student_id).first()
        if existing_student:
            return render_template('add_student.html', error="Student ID already exists. Please choose a different ID.", courses=courses)
        
        # If the ID doesn't exist, create a new student
        new_student = Student(id=student_id, name=name, age=age, department=department)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('view_students'))

    # Render the form with available courses when the request is GET
    return render_template('add_student.html', courses=courses)

# Edit Students
@app.route('/edit_student/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return "Student not found", 404  # Return error if student not found

    if request.method == 'POST':
        # Update student details with form data
        student.name = request.form['name']
        student.age = int(request.form['age'])
        student.department = request.form['department']
        
        db.session.commit()  # Save changes to the database
        return redirect(url_for('view_students'))  # Redirect to the students list page

    # Render the edit form with the current student details
    return render_template('edit_student.html', student=student)


@app.route('/delete_student/<student_id>', methods=['GET', 'POST'])
def delete_student(student_id):
    student = Student.query.get(student_id)  # Retrieve the student by ID
    if student:
        db.session.delete(student)  # Delete the student from the database
        db.session.commit()  # Commit the changes
        return redirect(url_for('view_students'))  # Redirect to the student list page
    else:
        return "Student not found", 404  # Return an error if the student is not found


# Route to view all students
@app.route('/view_students')
def view_students():
    students = Student.query.all()
    return render_template('view_students.html', students=students)

# Route to add professor
@app.route('/add_professor', methods=['GET', 'POST'])
def add_professor():
    if request.method == 'POST':
        professor_id = request.form['professor_id']
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        subjects = request.form['subjects']
        new_professor = Professor(id=professor_id, name=name, email=email, contact=contact, subjects=subjects)
        db.session.add(new_professor)
        db.session.commit()
        return redirect(url_for('view_professors'))
    return render_template('add_professor.html')

# Route to view all professors
@app.route('/view_professors')
def view_professors():
    professors = Professor.query.all()
    return render_template('view_professors.html', professors=professors)

# Route to add course
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_id = request.form['course_id']
        course_name = request.form['course_name']
        duration = request.form['duration']  # Get the duration from the form
        fees = request.form['fees']
        professor_id = request.form['professor_id']  # You may need to handle professor ID selection
        new_course = Course(id=course_id, name=course_name, duration=duration, fees=fees, professor_id=professor_id)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('view_courses'))
    professors = Professor.query.all()  # Fetch all professors to display in the form
    return render_template('add_course.html', professors=professors)

# Route to view all courses
@app.route('/view_courses')
def view_courses():
    courses = Course.query.all()
    return render_template('view_courses.html', courses=courses)

# Route to assign student to course
@app.route('/assign_student', methods=['GET', 'POST'])
def assign_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=course_id).first()
        if student and course:
            student.department = course.name  # Update student's department with the course name
            db.session.commit()
            return redirect(url_for('view_students'))
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('assign_student.html', students=students, courses=courses)

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


