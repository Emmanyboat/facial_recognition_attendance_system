# Smart Attendance System

A Django-based web application that uses face recognition technology to automatically track student attendance in real-time.

## 🎯 Features

- **Automated Face Recognition**: Real-time face detection and identification
- **Student Registration**: Photo upload and live camera capture
- **Attendance Tracking**: Automatic attendance marking with duplicate prevention
- **Big Success Notifications**: Prominent visual feedback when attendance is marked
- **Comprehensive Reporting**: Detailed attendance analytics and statistics
- **Offline Operation**: Works without internet connection
- **Mobile Responsive**: Modern, responsive web interface
- **Real-time Processing**: Instant face recognition and attendance logging

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Webcam for face recognition

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Emmanyboat/facial_recognition_attendance_system.git
   cd facial_recognition_attendance_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   pip install face-recognition
   pip install opencv-python
   pip install pillow
   pip install numpy
   ```

4. **Setup database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the application**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   Open your browser and go to: `http://127.0.0.1:8000`

## 📋 Usage

### 1. Register Students
- Navigate to the "Register" page
- Enter student name
- Upload a photo or capture one using the webcam
- System will automatically detect faces and create encodings

### 2. Mark Attendance
- Go to the "Recognize" page
- Click "Start Camera" to begin face recognition
- Position students in front of the camera
- System will automatically detect and mark attendance
- Big success notification will appear for new attendance records

### 3. View Reports
- Visit the "Attendance" page
- View daily attendance records
- Check attendance statistics
- Filter by specific dates

## 🛠️ Technical Stack

### Backend
- **Django 4.x**: Web framework
- **Python 3.8+**: Programming language
- **SQLite**: Database (can be upgraded to PostgreSQL/MySQL)

### Face Recognition
- **face_recognition**: Core face recognition library
- **OpenCV**: Image processing and computer vision
- **NumPy**: Numerical computing
- **Pillow (PIL)**: Image manipulation

### Frontend
- **HTML5/CSS3**: Markup and styling
- **JavaScript**: Client-side functionality
- **Bootstrap 5**: UI framework
- **Font Awesome**: Icons

## 📁 Project Structure

```
face_attendance/
├── manage.py                 # Django management script
├── face_attendance/          # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── recognition/             # Main app directory
│   ├── __init__.py
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL configuration
│   └── templates/           # HTML templates
│       └── recognition/
│           ├── home.html    # Dashboard
│           ├── register.html # Registration page
│           ├── recognize.html # Recognition page
│           └── attendance.html # Attendance page
├── media/                   # Uploaded files
├── static/                  # Static files
├── db.sqlite3              # SQLite database
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── STUDY_GUIDE.md         # Comprehensive study guide
├── PROJECT_REPORT.md      # Project report
└── STUDY_GUIDE_PRESENTATION.md # Presentation outline
```

## 🔧 Configuration

### Database
The system uses SQLite by default. To use a different database:

1. Update `settings.py` with your database configuration
2. Run migrations: `python manage.py migrate`

### Face Recognition Settings
- **Tolerance**: Adjust face matching sensitivity in `views.py`
- **Processing Interval**: Modify recognition frequency in `recognize.html`
- **Image Quality**: Change JPEG quality in registration process

## 🐛 Troubleshooting

### Common Issues

**Camera Access Denied**
- Ensure browser has camera permissions
- Use HTTPS in production environments
- Check browser security settings

**Face Detection Fails**
- Ensure good lighting conditions
- Use clear, front-facing photos
- Check image quality and format
- Verify face is clearly visible in frame

**Installation Errors**
- Use Python 3.8 or higher
- Install system dependencies first
- Use virtual environment
- Check package compatibility

### Debug Information
The system includes debug prints for troubleshooting:
```python
print(f"Image shape: {rgb_img.shape}")
print(f"Image dtype: {rgb_img.dtype}")
print(f"Face locations found: {len(face_locations)}")
print(f"Face encodings created: {len(encodings)}")
```

## 🔒 Security Considerations

- Face encodings are stored as binary data, not actual images
- Input validation on all user inputs
- Error handling without sensitive information exposure
- Use HTTPS in production environments
- Implement user authentication for production use

## 📊 Features in Detail

### Student Registration
- Support for JPEG and PNG image formats
- Live camera capture via webcam
- Automatic face detection and validation
- Duplicate student name prevention
- Image quality optimization

### Face Recognition
- Real-time face detection from webcam
- Multi-face support for simultaneous recognition
- High accuracy face matching with configurable tolerance
- Automatic attendance marking for recognized students
- Real-time status indicators

### Attendance Management
- Daily attendance tracking with date filtering
- Duplicate attendance prevention per day
- Comprehensive statistics and analytics
- 7-day attendance history
- Export capabilities for reports

### User Interface
- Modern, responsive Bootstrap design
- Mobile-friendly interface
- Real-time status updates
- Big success notifications for attendance confirmation
- Intuitive navigation and user experience

## 🚀 Future Enhancements

- Multi-class support and management
- Time-based attendance tracking (arrival/departure)
- Export functionality (PDF/Excel reports)
- Email notifications for absences
- Mobile application development
- Cloud storage integration
- Advanced analytics and machine learning insights
- Multi-language support

## 📝 Documentation

- **STUDY_GUIDE.md**: Comprehensive technical documentation
- **PROJECT_REPORT.md**: 4-page project report
- **STUDY_GUIDE_PRESENTATION.md**: Presentation outline

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Student Name**: [Your Name]  
**Course**: [Course Name]  
**Institution**: [Institution Name]  
**Email**: [Your Email]  

## 🙏 Acknowledgments

- Django community for the excellent web framework
- face_recognition library developers
- OpenCV contributors
- Bootstrap team for the UI framework
- All contributors and testers

---

**Project Status**: ✅ **Completed Successfully**  
**Last Updated**: December 2024  
**Version**: 2.0  

*This project demonstrates the practical application of computer vision, web development, and database management in creating a useful real-world application.* 