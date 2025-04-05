from django.urls import path
from . import views
from .views import login_view
from .views import create_faculty
from .views import edit_user
from .views import create_course
from .views import create_course, edit_course
from .views import delete_course  # Import the delete_course view
from .views import admin_announcements, delete_announcement  # ✅ Import the views
from .views import faculty_create_course, faculty_edit_course, faculty_dashboard
from .views import start_course
from .views import edit_lecture

from .views import upload_assignment, submit_assignment, grade_submission



urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path("login/", login_view, name="login"),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path("create_course/", create_course, name="create_course"),
    path("edit_course/<int:course_id>/", edit_course, name="edit_course"),
    path("delete_course/<int:course_id>/", delete_course, name="delete_course"),  # ✅ Ensure this line is present
    path("admin_announcements/", admin_announcements, name="admin_announcements"),
    path("delete_announcement/<int:announcement_id>/", delete_announcement, name="delete_announcement"),
    path("student_details/<int:student_id>/", views.student_details, name="student_details"),

    path("faculty_dashboard/", faculty_dashboard, name="faculty_dashboard"),
    path("faculty_create_course/", faculty_create_course, name="faculty_create_course"),
    path("faculty_edit_course/<int:course_id>/", faculty_edit_course, name="faculty_edit_course"),
    path("start_course/<int:course_id>/", start_course, name="start_course"),
    path("edit_lecture/<int:lecture_id>/", edit_lecture, name="edit_lecture"),
    path("faculty_notifications/", views.faculty_notifications, name="faculty_notifications"),

    path("enroll_course/<int:course_id>/", views.enroll_course, name="enroll_course"),
    path("available_courses/", views.available_courses, name="available_courses"),
    path("course_details/<int:course_id>/", views.course_details, name="course_details"),

    path("view_course/<int:course_id>/", views.view_course, name="view_course"),

    path('create_assignment/', views.create_assignment, name='create_assignment'),
    path('submit_assignment/', views.submit_assignment, name='submit_assignment'),
    path("create_faculty/", create_faculty, name="create_faculty"),
    path("edit_user/<int:user_id>/", edit_user, name="edit_user"),
    path('upload_assignment/', upload_assignment, name='upload_assignment'),  # ✅ Add this line
    path('submit_assignment/', submit_assignment, name='submit_assignment'),
    path('grade_submission/<int:submission_id>/', grade_submission, name='grade_submission'),

    path('faculty/create_quiz_full/', views.create_quiz_full, name='create_quiz_full'),
    path("faculty/quiz/<int:quiz_id>/add_question/", views.add_question, name="add_question"),
    path("faculty/quiz/<int:quiz_id>/finalize/", views.finalize_quiz, name="finalize_quiz"),
    path('faculty/quiz_list/', views.faculty_quiz_list, name='faculty_quiz_list'),
    path('faculty/quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),

    path('student/quiz_list/', views.student_quiz_list, name='student_quiz_list'),
    path('student/quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('student/quiz/submit/<int:quiz_id>/', views.submit_quiz, name='submit_quiz'),
    path('faculty/quiz_list/', views.faculty_quiz_list, name='faculty_quiz_list'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz_results/', views.quiz_results, name='quiz_results'),  # ✅ Allow general results page
    path('courses/', views.course_list, name='course_list'),


]
