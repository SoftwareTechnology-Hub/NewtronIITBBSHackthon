# NewtronIITBBSHackthon
# E-Learning Platform

This is a Django-based e-learning platform designed to facilitate online learning. It allows faculty to create and manage courses, quizzes, and assignments, while students can enroll in courses, take quizzes, and submit assignments. The platform is built using Python, Django, and SQLite3.

## Features

### Admin Dashboard:
- Manage users (Faculty and Students)
- Approve or remove course enrollments
- Manage system settings and configurations
- View platform usage statistics
- Assign roles to users (Admin, Faculty, Student)
  
### Faculty Dashboard:
- Create and manage courses
- Set and manage assignments
- Create quizzes and evaluate student performance
- View student submissions and grades

### Student Dashboard:
- Enroll in courses
- Take quizzes
- Submit assignments
- View grades and feedback

## Requirements

To run this project, you'll need the following:
- Python 3.x
- Django 4.x
- SQLite3 (default database)

## Installation

## 1. Clone the repository:

   git clone https://github.com/SoftwareTechnology-Hub/NewtronIITBBSHackthon.git
   
## 2.Navigate to the project directory:
  
  cd NewtronIITBBSHackthon

## 3.Create a virtual environment
  
  python -m venv venv

## 4.Activate the virtual environment:
  
  venv\Scripts\activate

## 5.Install the required dependencies:
 
  pip install -r requirements.txt

## 6.Apply migrations to set up the database:
  
  python manage.py migrate

## 7.Create a superuser to access the Django admin panel:
  
  python manage.py createsuperuser

## 8.Start the development server:
  
  python manage.py runserver




