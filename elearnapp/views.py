from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *

def index(request):
    return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import CustomUser

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if username and email and password and role:
            user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)
            return redirect('login')  # Redirect to login page after registration

    return render(request, 'register.html')


from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']  # Get selected role

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Ensure the selected role matches the user's actual role
            if (role == "admin" and user.is_superuser) or (role == user.role):
                login(request, user)

                if role == "student":
                    return redirect('student_dashboard')
                elif role == "faculty":
                    return redirect('faculty_dashboard')
                elif role == "admin":  # Redirect Super Admin to Admin Dashboard
                    return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid role selected for this user.")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")




from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, CustomUser

from django.shortcuts import render
from .models import Course, CustomUser

from django.shortcuts import render, redirect
from .models import Course, CustomUser

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Course, CustomUser, Assignment, Submission

# Faculty Dashboard - Manage Assignments & Track Performance
@login_required
def faculty_dashboard(request):
    if request.user.role != "faculty":
        return redirect("login")  # Only faculty can access

    courses = Course.objects.filter(faculty=request.user)
    assignments = Assignment.objects.filter(course__in=courses)

    # Fetch student submissions
    course_submissions = {}
    for course in courses:
        submissions = Submission.objects.filter(assignment__course=course)
        course_submissions[course] = submissions

    context = {
        "courses": courses,
        "assignments": assignments,
        "course_submissions": course_submissions,  # Student submissions tracking
    }
    return render(request, "faculty_dashboard.html", context)


# Upload Assignments (Faculty Only)
@login_required
def upload_assignment(request):
    if request.user.role != "faculty":
        return redirect("login")

    if request.method == "POST":
        course_id = request.POST.get("course")
        title = request.POST.get("title")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")

        course = get_object_or_404(Course, id=course_id, faculty=request.user)
        Assignment.objects.create(course=course, title=title, description=description, deadline=deadline)

        return redirect("faculty_dashboard")

    courses = Course.objects.filter(faculty=request.user)
    return render(request, "upload_assignment.html", {"courses": courses})


# Grade Assignment and Provide Feedback
@login_required
def grade_submission(request, submission_id):
    if request.user.role != "faculty":
        return redirect("login")

    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == "POST":
        grade = request.POST.get("grade")
        feedback = request.POST.get("feedback")

        submission.grade = grade
        submission.feedback = feedback
        submission.save()

        return redirect("faculty_dashboard")

    return render(request, "grade_submission.html", {"submission": submission})


# Student Dashboard - Submit Assignments & View Grades

# Submit Assignments (Student)
@login_required
def submit_assignment(request):
    if request.user.role != "student":
        return redirect("login")

    if request.method == "POST" and request.FILES.get("file"):
        assignment_id = request.POST.get("assignment")
        assignment = get_object_or_404(Assignment, id=assignment_id)

        # Prevent multiple submissions
        if Submission.objects.filter(assignment=assignment, student=request.user).exists():
            return redirect("student_dashboard")

        file = request.FILES["file"]
        Submission.objects.create(assignment=assignment, student=request.user, file=file)

        return redirect("student_dashboard")

    assignments = Assignment.objects.exclude(
        id__in=Submission.objects.filter(student=request.user).values_list("assignment_id", flat=True)
    )
    return render(request, "submit_assignment.html", {"assignments": assignments})


# View Assignment Feedback & Grades (Student)
@login_required
def view_feedback(request):
    if request.user.role != "student":
        return redirect("login")

    submissions = Submission.objects.filter(student=request.user).exclude(grade__isnull=True)

    return render(request, "view_feedback.html", {"submissions": submissions})

def faculty_create_course(request):
    if request.user.role != "faculty":
        return redirect("login")

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        start_date = request.POST["start_date"]
        image = request.FILES.get("image")  # Optional file upload

        Course.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            faculty=request.user,
            image=image
        )

        return redirect("faculty_dashboard")

    return render(request, "faculty_create_course.html")


def faculty_edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, faculty=request.user)

    if request.method == "POST":
        course.title = request.POST["title"]
        course.description = request.POST["description"]
        course.start_date = request.POST["start_date"]
        course.save()
        return redirect("faculty_dashboard")

    return render(request, "faculty_edit_course.html", {"course": course})
from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Lecture
from django.core.files.storage import FileSystemStorage
from datetime import date

def start_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST.get("content", "")
        upload_date = request.POST.get("upload_date", str(date.today()))  # Get selected date, default to today

        # Handle PDF upload
        pdf_file = request.FILES.get("pdf_file", None)
        pdf_path = None
        if pdf_file:
            fs = FileSystemStorage(location="media/pdfs/")
            pdf_path = fs.save(pdf_file.name, pdf_file)

        # Handle Video upload
        video_file = request.FILES.get("video_file", None)
        video_path = None
        if video_file:
            fs = FileSystemStorage(location="media/videos/")
            video_path = fs.save(video_file.name, video_file)

        # Save lecture with the selected date
        Lecture.objects.create(
            course=course, title=title, content=content, 
            pdf_file=pdf_path, video_file=video_path, created_at=upload_date
        )

        return redirect("start_course", course_id=course.id)

    # Fetch lectures and group by date
    lectures = course.lectures.all().order_by("-created_at")
    lectures_by_date = defaultdict(list)

    for lecture in lectures:
        lectures_by_date[lecture.created_at].append(lecture)

    return render(request, "start_course.html", {"course": course, "lectures_by_date": dict(lectures_by_date)})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lecture
from django.core.files.storage import default_storage

def edit_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)

    if request.method == "POST":
        lecture.title = request.POST["title"]
        lecture.content = request.POST["content"]

        if "pdf_file" in request.FILES:
            if lecture.pdf_file:
                default_storage.delete(lecture.pdf_file.path)  # Delete old file
            lecture.pdf_file = request.FILES["pdf_file"]

        if "video_file" in request.FILES:
            if lecture.video_file:
                default_storage.delete(lecture.video_file.path)  # Delete old file
            lecture.video_file = request.FILES["video_file"]

        lecture.save()
        return redirect("faculty_dashboard")

    return render(request, "faculty_edit_lecture.html", {"lecture": lecture})
from django.shortcuts import render, redirect
from .models import Notification, CustomUser

def faculty_notifications(request):
    faculty = request.user  # Get logged-in faculty

    if request.method == "POST":
        title = request.POST["title"]
        message = request.POST["message"]
        Notification.objects.create(faculty=faculty, title=title, message=message)
        return redirect("faculty_dashboard")

    notifications = Notification.objects.filter(faculty=faculty).order_by("-created_at")  # Get latest first
    return render(request, "faculty_notifications.html", {"notifications": notifications})

from django.shortcuts import render
from .models import CustomUser, Course, Assignment, Submission

def admin_dashboard(request):
    users = CustomUser.objects.all().order_by("role")  # Fetch all users sorted by role
    faculties = CustomUser.objects.filter(role="faculty")  # Fetch only faculty members
    courses = Course.objects.all()  # Fetch all courses
    users = CustomUser.objects.all().order_by('role')  # Fetch all users
    courses = Course.objects.all()
    assignments = Assignment.objects.all()
    submissions = Submission.objects.all()
    available_courses = Course.objects.all()  # Or apply filtering if needed


    context = {
        "users": users,
        'available_courses': available_courses,
        "assignments": assignments,
        "submissions": submissions,
    }
    return render(request, "admin_dashboard.html", context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.role = request.POST["role"]
        user.save()
        return redirect("admin_dashboard")  # Redirect back to Admin Dashboard

    return render(request, "edit_user.html", {"user": user})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, CustomUser

from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, CustomUser
from datetime import datetime

def create_course(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        faculty_id = request.POST["faculty"]
        start_date = request.POST["start_date"]  # Get start date from form input

        faculty = get_object_or_404(CustomUser, id=faculty_id)

        # Convert start_date to Python's date format
        formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        Course.objects.create(
            title=title, 
            description=description, 
            faculty=faculty, 
            start_date=formatted_start_date  # Save the formatted date
        )
        return redirect("admin_dashboard")

    faculties = CustomUser.objects.filter(role="faculty")
    return render(request, "create_course.html", {"faculties": faculties})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    faculties = CustomUser.objects.filter(role="faculty")  # Get faculty members

    if request.method == "POST":
        course.title = request.POST["title"]
        course.description = request.POST["description"]
        faculty_id = request.POST["faculty"]
        course.faculty = get_object_or_404(CustomUser, id=faculty_id)
        course.start_date = request.POST["start_date"]  # Get the updated start date
        course.save()
        return redirect("admin_dashboard")

    return render(request, "edit_course.html", {"course": course, "faculties": faculties})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect("admin_dashboard")  # Redirect back to the admin dashboard
def create_assignment(request):
    if request.user.role != 'faculty':
        return redirect('dashboard')

    if request.method == 'POST':
        course_id = request.POST.get('course')
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')

        course = Course.objects.get(id=course_id)

        if course and title and description and deadline:
            Assignment.objects.create(course=course, title=title, description=description, deadline=deadline)
            return redirect('dashboard')

    courses = Course.objects.filter(faculty=request.user)
    return render(request, 'create_assignment.html', {'courses': courses})
    from django.shortcuts import render, redirect
from .models import Announcement

def admin_announcements(request):
    announcements = Announcement.objects.all().order_by('-created_at')

    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")
        Announcement.objects.create(title=title, message=message)
        return redirect("admin_announcements")

    return render(request, "admin_announcements.html", {"announcements": announcements})

def delete_announcement(request, announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)
    announcement.delete()
    return redirect("admin_announcements")
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, CustomUser
from django.shortcuts import render, get_object_or_404
from .models import CustomUser

def student_details(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
    return render(request, "student_details.html", {"student": student})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Assignment, Submission, CustomUser

@login_required
def student_dashboard(request):
    student = request.user
    
    # Fetch courses
    available_courses = Course.objects.exclude(students=student)  # Courses not yet enrolled
    enrolled_courses = Course.objects.filter(students=student)  # Enrolled courses
    
    # Fetch pending assignments (Not yet submitted)
    pending_assignments = Assignment.objects.filter(course__in=enrolled_courses).exclude(
        submission__student=student
    )
    
    # Fetch submitted assignments
    submitted_assignments = Submission.objects.filter(student=student)

    # Fetch grades & feedback for submitted assignments
    graded_assignments = submitted_assignments.exclude(grade__isnull=True)

    # Handle assignment submission
    if request.method == "POST" and request.FILES.get("file"):
        assignment_id = request.POST.get("assignment")
        assignment = Assignment.objects.get(id=assignment_id)
        file = request.FILES["file"]
        
        # Create submission
        Submission.objects.create(assignment=assignment, student=student, file=file)
        return redirect("student_dashboard")

    context = {
        "available_courses": available_courses,
        "enrolled_courses": enrolled_courses,
        "pending_assignments": pending_assignments,
        "submitted_assignments": submitted_assignments,
        "graded_assignments": graded_assignments,
    }
    
    return render(request, "student_dashboard.html", context)
def available_courses(request):
    courses = Course.objects.all()  # Get all available courses
    return render(request, "available_courses.html", {"courses": courses})

def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Get course details
    return render(request, "course_details.html", {"course": course})
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user
    
    if student.role == "student":
        course.students.add(student)  # Enroll the student
        return redirect("student_dashboard")

    return redirect("student_dashboard")
def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user in course.students.all():  # Ensure only enrolled students can access
        lectures = course.lectures.all()  # Get lectures using the correct related name
        return render(request, "view_course.html", {"course": course, "lectures": lectures})

    return redirect("student_dashboard")


def submit_assignment(request):
    if request.user.role != 'student':
        return redirect('dashboard')

    if request.method == 'POST' and request.FILES.get('file'):
        assignment_id = request.POST.get('assignment')
        assignment = Assignment.objects.get(id=assignment_id)
        
        file = request.FILES['file']

        Submission.objects.create(assignment=assignment, student=request.user, file=file)
        return redirect('dashboard')

    assignments = Assignment.objects.all()
    return render(request, 'submit_assignment.html', {'assignments': assignments})
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import CustomUser

def create_faculty(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Create Faculty User
        faculty = CustomUser.objects.create(
            username=username,
            email=email,
            role="faculty",  # Set role as Faculty
            password=make_password(password)  # Hash password
        )
        
        faculty.save()
        return redirect("admin_dashboard")  # Redirect back to Admin Dashboard

    return redirect("admin_dashboard")  # If accessed via GET, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, StudentResponse
from django.contrib import messages

# ✅ Faculty creates a quiz
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice
from django.http import JsonResponse

import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question

import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
import json
from .models import Quiz, Question

@login_required
def create_quiz_full(request):
    if request.method == "POST":
        title = request.POST.get("title")
        time_limit = request.POST.get("time_limit")
        quiz_data_json = request.POST.get("quiz_data")

        if not all([title, time_limit, quiz_data_json]):
            return HttpResponseBadRequest("Missing fields")

        # Create Quiz object
        quiz = Quiz.objects.create(
            faculty=request.user,
            title=title,
            time_limit=int(time_limit)
        )

        # Parse and save questions
        try:
            questions = json.loads(quiz_data_json)
            for q in questions:
                Question.objects.create(
                    quiz=quiz,
                    text=q["text"],
                    option1=q["option1"],
                    option2=q["option2"],
                    option3=q["option3"],
                    option4=q["option4"],
                    correct_option=q["correct_option"]
                )
        except Exception as e:
            quiz.delete()
            return HttpResponseBadRequest(f"Invalid question data: {e}")

        return redirect("faculty_dashboard")  # or wherever you want

    return render(request, "create_quiz_full.html")

from .models import Quiz

def show_quizzes(request):
    quizzes = Quiz.objects.prefetch_related('question_set').all()
    return render(request, 'create_quiz_full.html', {'quizzes': quizzes})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Choice

from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Choice

def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        question_text = request.POST.get("question_text")
        choices = [request.POST.get(f"choice_{i}") for i in range(1, 5)]
        correct_choice_index = request.POST.get("correct_choice")  # Should be 1,2,3 or 4

        if question_text and correct_choice_index and any(choices):
            question = Question.objects.create(quiz=quiz, text=question_text)

            # Save choices to database
            for i, choice_text in enumerate(choices, start=1):
                if choice_text:  # Ensure choice is not empty
                    is_correct = (str(i) == correct_choice_index)  # Check if this is the correct choice
                    Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)

            return redirect("add_question", quiz_id=quiz.id)  # Redirect to refresh page

    return render(request, "add_question.html", {"quiz": quiz})


@login_required
def finalize_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, "finalize_quiz.html", {"quiz": quiz})


# ✅ Faculty adds questions

# ✅ Faculty views quiz results
@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, faculty=request.user)
    responses = StudentResponse.objects.filter(quiz=quiz)

    student_scores = {}
    for response in responses:
        if response.student not in student_scores:
            student_scores[response.student] = 0
        if response.is_correct:
            student_scores[response.student] += 1

    return render(request, "quiz_results.html", {"quiz": quiz, "student_scores": student_scores})

# ✅ Student views available quizzes
@login_required
def student_quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, "quiz_list.html", {"quizzes": quizzes})

# ✅ Student takes a quiz
from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()

    if request.method == 'POST':
        # You can add scoring logic later here if needed
        return render(request, 'quiz_submitted.html')  # thank you page

    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})

# ✅ Student submits quiz
@login_required
def submit_quiz(request, quiz_id):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, id=quiz_id)
        for question in Question.objects.filter(quiz=quiz):
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                selected_choice = Choice.objects.get(id=choice_id)
                StudentResponse.objects.create(
                    student=request.user,
                    quiz=quiz,
                    question=question,
                    selected_choice=selected_choice,
                    is_correct=selected_choice.is_correct
                )
        messages.success(request, "Quiz submitted successfully!")
        return redirect('student_quiz_list')

    return JsonResponse({'error': 'Invalid request'}, status=400)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Quiz

@login_required
def faculty_quiz_list(request):
    quizzes = Quiz.objects.filter(faculty=request.user)
    return render(request, "faculty_quiz_list.html", {"quizzes": quizzes})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Quiz, Question

import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Quiz, Question

@login_required
def faculty_quiz_list(request):
    quizzes = Quiz.objects.filter(faculty=request.user).prefetch_related('question_set')
    
    quiz_data = []
    for quiz in quizzes:
        question_details = []
        for q in quiz.question_set.all():
            try:
                q_data = json.loads(q.text)  # Parse stored question JSON
                question_details.append({
                    'text': q_data.get('question_text', ''),
                    'choices': q_data.get('choices', []),
                    'correct_index': int(q_data.get('correct_index', -1))
                })
            except Exception:
                question_details.append({
                    'text': q.text,
                    'choices': [],
                    'correct_index': -1
                })

        quiz_data.append({
            'title': quiz.title,
            'time_limit': quiz.time_limit,
            'questions': question_details,
            'question_count': len(question_details)
        })

    return render(request, 'faculty_quiz_list.html', {'quizzes': quiz_data})
from django.shortcuts import render
from .models import Course

def course_list(request):
    courses = Course.objects.select_related('faculty').all()
    return render(request, 'course_list.html', {'courses': courses})
