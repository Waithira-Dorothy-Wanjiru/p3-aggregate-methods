from datetime import datetime

# ------------------------
# Student Class
# ------------------------
class Student:
    def __init__(self, name):
        self.name = name
        self._enrollments = []
        self._grades = {}  # {enrollment: grade}

    def enroll(self, course):
        """Enroll the student in a course."""
        if isinstance(course, Course):
            enrollment = Enrollment(self, course)
            self._enrollments.append(enrollment)
            course.add_enrollment(enrollment)
        else:
            raise TypeError("course must be an instance of Course")

    def get_enrollments(self):
        """Return a copy of enrollments."""
        return self._enrollments.copy()

    def course_count(self):
        """Return the number of courses this student is enrolled in."""
        return len(self._enrollments)

    def set_grade(self, enrollment, grade):
        """Set a grade for a given enrollment."""
        if enrollment in self._enrollments:
            self._grades[enrollment] = grade
        else:
            raise ValueError("Student is not enrolled in this course")

    def aggregate_average_grade(self):
        """Return the average grade across all enrollments."""
        if not self._grades:
            return None  # Avoid division by zero
        total_grades = sum(self._grades.values())
        num_courses = len(self._grades)
        return total_grades / num_courses

# ------------------------
# Course Class
# ------------------------
class Course:
    def __init__(self, title):
        self.title = title
        self._enrollments = []

    def add_enrollment(self, enrollment):
        """Add an enrollment to this course."""
        if isinstance(enrollment, Enrollment):
            self._enrollments.append(enrollment)
        else:
            raise TypeError("enrollment must be an instance of Enrollment")

    def get_enrollments(self):
        """Return a copy of enrollments."""
        return self._enrollments.copy()

    def student_count(self):
        """Return the number of students enrolled in this course."""
        return len(self._enrollments)

    def get_students(self):
        """Return a list of students enrolled in this course."""
        return [enrollment.student for enrollment in self._enrollments]

# ------------------------
# Enrollment Class
# ------------------------
class Enrollment:
    all = []

    def __init__(self, student, course):
        if isinstance(student, Student) and isinstance(course, Course):
            self.student = student
            self.course = course
            self._enrollment_date = datetime.now()
            type(self).all.append(self)
        else:
            raise TypeError("Invalid types for student and/or course")

    def get_enrollment_date(self):
        """Return the enrollment datetime."""
        return self._enrollment_date

    @classmethod
    def aggregate_enrollments_per_day(cls):
        """Return a dict with dates as keys and enrollment counts as values."""
        enrollment_count = {}
        for enrollment in cls.all:
            date = enrollment.get_enrollment_date().date()
            enrollment_count[date] = enrollment_count.get(date, 0) + 1
        return enrollment_count

# ------------------------
# Example Usage
# ------------------------
if __name__ == "__main__":
    # Create students
    alice = Student("Alice")
    bob = Student("Bob")

    # Create courses
    math = Course("Math")
    physics = Course("Physics")

    # Enroll students
    alice.enroll(math)
    alice.enroll(physics)
    bob.enroll(math)

    # Set grades
    alice.set_grade(alice.get_enrollments()[0], 90)
    alice.set_grade(alice.get_enrollments()[1], 80)
    bob.set_grade(bob.get_enrollments()[0], 70)

    # Use aggregate methods
    print("Alice's course count:", alice.course_count())          # 2
    print("Bob's average grade:", bob.aggregate_average_grade())  # 70.0
    print("Alice's average grade:", alice.aggregate_average_grade())  # 85.0
    print("Math student count:", math.student_count())            # 2
    print("Physics students:", [s.name for s in physics.get_students()])  # ['Alice']
    print("Enrollments per day:", Enrollment.aggregate_enrollments_per_day())
