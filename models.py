from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Update the URI for PostgreSQL (replace with your credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:P5GDd7x4fkpvrdGVmkbhLMFInOz41PRF@dpg-cva5ip7noe9s73e42ns0-a.oregon-postgres.render.com/dbname_05pv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Student model
class Student(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    courses = db.relationship('Course', secondary='student_course')
    fees = db.relationship('Fee', foreign_keys='Fee.student_id', lazy=True)

# Define Professor model
class Professor(db.Model):
    __tablename__ = 'professor'
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contact = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    subjects = db.Column(db.String(200), nullable=True)

# Define Course model
class Course(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    professor_id = db.Column(db.String(50), db.ForeignKey('professor.id'), nullable=False)
    fees = db.Column(db.Float, nullable=False)

    def __init__(self, id, name, duration, fees, professor_id):
        self.id = id
        self.name = name
        self.duration = duration  # Ensure this is properly initialized
        self.fees = fees
        self.professor_id = professor_id

# Association table between students and courses
class StudentCourse(db.Model):
    student_id = db.Column(db.String(50), db.ForeignKey('student.id'), primary_key=True)
    course_id = db.Column(db.String(50), db.ForeignKey('course.id'), primary_key=True)

class Fee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.String(100), db.ForeignKey('course.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships to Student and Course without backref
    student = db.relationship('Student', foreign_keys=[student_id])
    course = db.relationship('Course', foreign_keys=[course_id])


with app.app_context():
    db.create_all()  # Create the tables in the database
