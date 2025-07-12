from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Student, Attendance
import face_recognition
import cv2
import numpy as np
from datetime import datetime, timedelta
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import json
import base64
from django.views.decorators.csrf import csrf_exempt

def home(request):
    """Home page with navigation to different features"""
    total_students = Student.objects.count()
    today_attendance = Attendance.objects.filter(
        timestamp__date=datetime.now().date()
    ).count()
    
    context = {
        'total_students': total_students,
        'today_attendance': today_attendance,
    }
    return render(request, 'recognition/home.html', context)

def register_face(request):
    """Register a new student's face"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            if not name:
                messages.error(request, 'Name is required')
                return render(request, 'recognition/register.html')
            
            # Check if student already exists
            if Student.objects.filter(name=name).exists():
                messages.error(request, 'Student with this name already exists')
                return render(request, 'recognition/register.html')
            
            image = request.FILES.get('image')
            if not image:
                messages.error(request, 'Image is required')
                return render(request, 'recognition/register.html')
            
            # Save image temporarily
            file_path = default_storage.save(f'faces/{name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg', image)
            full_path = default_storage.path(file_path)
            
            # Load and process image
            img = face_recognition.load_image_file(full_path)
            encodings = face_recognition.face_encodings(img)
            
            if not encodings:
                messages.error(request, 'No face detected in the image. Please upload a clear face image.')
                # Clean up the saved file
                default_storage.delete(file_path)
                return render(request, 'recognition/register.html')
            
            # Save student with face encoding
            student = Student.objects.create(
                name=name, 
                encoding=encodings[0].tobytes()
            )
            
            messages.success(request, f'Student {name} registered successfully!')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'Error registering student: {str(e)}')
            return render(request, 'recognition/register.html')
    
    return render(request, 'recognition/register.html')

def recognize_face(request):
    """Display recognition page with camera feed"""
    students = Student.objects.all()
    context = {
        'students': students,
        'total_students': students.count()
    }
    return render(request, 'recognition/recognize.html', context)

@csrf_exempt
def process_recognition(request):
    """Process face recognition from camera feed"""
    if request.method == 'POST':
        try:
            # Get image data from request
            data = json.loads(request.body)
            image_data = data.get('image')
            
            if not image_data:
                return JsonResponse({'error': 'No image data received'}, status=400)
            
            # Decode base64 image
            image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            
            # Convert to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convert BGR to RGB
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            face_locations = face_recognition.face_locations(rgb_img)
            face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
            
            if not face_encodings:
                return JsonResponse({'message': 'No face detected'})
            
            # Get all registered students
            students = Student.objects.all()
            known_encodings = [np.frombuffer(s.encoding) for s in students]
            known_names = [s.name for s in students]
            
            if not known_encodings:
                return JsonResponse({'message': 'No registered students found'})
            
            recognized_students = []
            
            for face_encoding in face_encodings:
                # Compare with known faces
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                
                if True in matches:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        student_name = known_names[best_match_index]
                        student = students[best_match_index]
                        
                        # Check if attendance already recorded today
                        today = datetime.now().date()
                        existing_attendance = Attendance.objects.filter(
                            student=student,
                            timestamp__date=today
                        ).first()
                        
                        if not existing_attendance:
                            # Record attendance
                            Attendance.objects.create(student=student)
                            recognized_students.append({
                                'name': student_name,
                                'status': 'Attendance recorded',
                                'new_record': True
                            })
                        else:
                            recognized_students.append({
                                'name': student_name,
                                'status': 'Already marked present today',
                                'new_record': False
                            })
                else:
                    recognized_students.append({
                        'name': 'Unknown',
                        'status': 'Face not recognized',
                        'new_record': False
                    })
            
            return JsonResponse({
                'recognized_students': recognized_students,
                'total_faces': len(face_encodings)
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def view_attendance(request):
    """View attendance records"""
    # Get date filter
    date_filter = request.GET.get('date')
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            attendances = Attendance.objects.filter(timestamp__date=filter_date).order_by('-timestamp')
        except ValueError:
            attendances = Attendance.objects.all().order_by('-timestamp')
    else:
        # Default to today
        attendances = Attendance.objects.filter(
            timestamp__date=datetime.now().date()
        ).order_by('-timestamp')
    
    # Get statistics
    total_students = Student.objects.count()
    today_attendance = Attendance.objects.filter(
        timestamp__date=datetime.now().date()
    ).count()
    
    # Get attendance for last 7 days
    last_7_days = []
    for i in range(7):
        date = datetime.now().date() - timedelta(days=i)
        count = Attendance.objects.filter(timestamp__date=date).count()
        last_7_days.append({
            'date': date,
            'count': count,
            'percentage': round((count / total_students * 100) if total_students > 0 else 0, 1)
        })
    
    context = {
        'attendances': attendances,
        'total_students': total_students,
        'today_attendance': today_attendance,
        'attendance_percentage': round((today_attendance / total_students * 100) if total_students > 0 else 0, 1),
        'last_7_days': last_7_days,
        'selected_date': date_filter or datetime.now().strftime('%Y-%m-%d')
    }
    
    return render(request, 'recognition/attendance.html', context)

def delete_student(request, student_id):
    """Delete a student and their attendance records"""
    try:
        student = Student.objects.get(id=student_id)
        student_name = student.name
        student.delete()
        messages.success(request, f'Student {student_name} deleted successfully!')
    except Student.DoesNotExist:
        messages.error(request, 'Student not found')
    except Exception as e:
        messages.error(request, f'Error deleting student: {str(e)}')
    
    return redirect('home')
