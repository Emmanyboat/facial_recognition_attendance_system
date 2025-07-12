from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_face, name='register'),
    path('recognize/', views.recognize_face, name='recognize'),
    path('process-recognition/', views.process_recognition, name='process_recognition'),
    path('attendance/', views.view_attendance, name='view_attendance'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
]