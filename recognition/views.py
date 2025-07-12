import io
import base64
import cv2
import numpy as np
import face_recognition
from PIL import Image
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib import messages
from .models import Student, Attendance  # Ensure Student model is imported
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import timedelta

def home(request):
    """Home page with navigation to different features"""
    total_students = Student.objects.count()  # type: ignore[attr-defined]
    today_attendance = Attendance.objects.filter(
        timestamp__date=datetime.now().date()
    ).count()  # type: ignore[attr-defined]
    
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
            if Student.objects.filter(name=name).exists():  # type: ignore[attr-defined]
                messages.error(request, 'Student with this name already exists')
                return render(request, 'recognition/register.html')

            file_path = None

            # --- Handle base64 captured image ---
            captured_image_data = request.POST.get('capturedImageData')
            if captured_image_data:
                if ',' in captured_image_data:
                    captured_image_data = captured_image_data.split(',')[1]
                image_bytes = base64.b64decode(captured_image_data)
                pil_image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

            # --- Handle uploaded image ---
            elif request.FILES.get('image'):
                image_file = request.FILES['image']
                if image_file.content_type not in ['image/jpeg', 'image/png']:
                    messages.error(request, 'Only JPEG or PNG images are allowed.')
                    return render(request, 'recognition/register.html')
                pil_image = Image.open(image_file).convert('RGB')

            else:
                messages.error(request, 'Please provide a student photo either by capturing or uploading.')
                return render(request, 'recognition/register.html')

            # Save image as JPEG
            output = io.BytesIO()
            pil_image.save(output, format='JPEG', quality=95)
            output.seek(0)
            file_path = default_storage.save(
                f'faces/{name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg',
                ContentFile(output.getvalue(), name=f'{name}.jpg')
            )
            full_path = default_storage.path(file_path)

            # Read image using OpenCV and convert to RGB
            img_bgr = cv2.imread(full_path)
            
            # Validate image loading
            if img_bgr is None:
                raise ValueError("Failed to load image")

            # Convert to RGB directly
            rgb_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            
            # Ensure 8-bit RGB format
            if rgb_img.dtype != np.uint8:
                rgb_img = rgb_img.astype(np.uint8)
            
            # Additional validation
            print(f"Image shape: {rgb_img.shape}")
            print(f"Image dtype: {rgb_img.dtype}")
            print(f"Image min/max values: {rgb_img.min()}, {rgb_img.max()}")
            
            # Try face detection with more debugging
            face_locations = face_recognition.face_locations(rgb_img)
            print(f"Face locations found: {len(face_locations)}")
            
            if not face_locations:
                raise ValueError("No face detected in the image. Please ensure the image contains a clear, front-facing face.")
            
            encodings = face_recognition.face_encodings(rgb_img, face_locations)
            print(f"Face encodings created: {len(encodings)}")
            
            if not encodings:
                raise ValueError("Failed to create face encoding. Please try with a different image.")
            
            # Save student information
            Student.objects.create(  # type: ignore[attr-defined]
                name=name,
                encoding=encodings[0].tobytes()
            )
            
            messages.success(request, f'Student {name} registered successfully!')
            return redirect('home')

        except Exception as e:
            messages.error(request, f'Error registering student: {str(e)}')
            if file_path:
                try:
                    default_storage.delete(file_path)
                except:
                    pass
            return render(request, 'recognition/register.html')

    return render(request, 'recognition/register.html')

def recognize_face(request):
    """Display recognition page with camera feed"""
    students = Student.objects.all()  # type: ignore[attr-defined]
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
            
            if img is not None:
                # Convert BGR to RGB
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                return JsonResponse({'error': 'Failed to decode image'}, status=400)
            
            # Detect faces
            face_locations = face_recognition.face_locations(rgb_img)
            face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
            
            if not face_encodings:
                return JsonResponse({'message': 'No face detected'})
            
            # Get all registered students
            students = Student.objects.all()  # type: ignore[attr-defined]
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
                    best_match_index = int(np.argmin(face_distances))
                    if matches[best_match_index]:
                        student_name = known_names[best_match_index]
                        student = students[best_match_index]
                        
                        # Check if attendance already recorded today
                        today = datetime.now().date()
                        existing_attendance = Attendance.objects.filter(
                            student=student,
                            timestamp__date=today
                        ).first()  # type: ignore[attr-defined]
                        
                        if not existing_attendance:
                            # Record attendance
                            Attendance.objects.create(student=student)  # type: ignore[attr-defined]
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
            attendances = Attendance.objects.filter(timestamp__date=filter_date).order_by('-timestamp')  # type: ignore[attr-defined]
        except ValueError:
            attendances = Attendance.objects.all().order_by('-timestamp')  # type: ignore[attr-defined]
    else:
        # Default to today
        attendances = Attendance.objects.filter(
            timestamp__date=datetime.now().date()
        ).order_by('-timestamp')  # type: ignore[attr-defined]
    
    # Get statistics
    total_students = Student.objects.count()  # type: ignore[attr-defined]
    today_attendance = Attendance.objects.filter(
        timestamp__date=datetime.now().date()
    ).count()  # type: ignore[attr-defined]
    
    # Get attendance for last 7 days
    last_7_days = []
    for i in range(7):
        date = datetime.now().date() - timedelta(days=i)
        count = Attendance.objects.filter(timestamp__date=date).count()  # type: ignore[attr-defined]
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
        student = Student.objects.get(id=student_id)  # type: ignore[attr-defined]
        student_name = student.name
        student.delete()
        messages.success(request, f'Student {student_name} deleted successfully!')
    except Student.DoesNotExist:  # type: ignore[attr-defined]
        messages.error(request, 'Student not found')
    except Exception as e:
        messages.error(request, f'Error deleting student: {str(e)}')
    
    return redirect('home')
