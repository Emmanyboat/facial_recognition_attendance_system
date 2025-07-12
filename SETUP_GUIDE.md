# Smart Attendance System - Setup Guide

## Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- Webcam or USB camera
- Modern web browser

### 2. Installation Steps

#### Step 1: Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd face_attendance

# Or download and extract the ZIP file
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

**Option A: Automatic Installation (Recommended)**
```bash
python install.py
```

**Option B: Manual Installation**
```bash
pip install -r requirements.txt
```

#### Step 4: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Step 5: Start the Application
```bash
python run.py
```

The application will be available at: http://127.0.0.1:8000/

## Troubleshooting

### Common Installation Issues

#### 1. dlib Installation Problems

**Windows:**
```bash
# Install Visual Studio Build Tools first
# Download from: https://visualstudio.microsoft.com/downloads/
# Then install dlib
pip install dlib
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install cmake build-essential
pip install dlib
```

**macOS:**
```bash
brew install cmake
pip install dlib
```

#### 2. face_recognition Installation Issues

If face_recognition fails to install:
```bash
# Try installing dlib first
pip install dlib
# Then install face_recognition
pip install face_recognition
```

#### 3. OpenCV Installation Issues

```bash
# Try alternative installation
pip install opencv-python-headless
```

### Alternative Installation Methods

#### Using Conda (Recommended for Windows)
```bash
conda create -n face_attendance python=3.9
conda activate face_attendance
conda install -c conda-forge dlib
pip install face_recognition opencv-python django
```

#### Using pip with Pre-built Wheels
```bash
# For Windows users
pip install --only-binary=all dlib
pip install face_recognition
```

### System-Specific Instructions

#### Windows
1. Install Visual Studio Build Tools
2. Install CMake from https://cmake.org/download/
3. Use the installation script: `python install.py`

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-dev python3-pip cmake build-essential
pip3 install -r requirements.txt
```

#### macOS
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install cmake
pip3 install -r requirements.txt
```

### Verification

After installation, verify everything works:

```bash
python -c "import face_recognition; print('face_recognition OK')"
python -c "import cv2; print('OpenCV OK')"
python -c "import django; print('Django OK')"
```

### Running the Application

1. **Start the server:**
   ```bash
   python run.py
   ```

2. **Access the application:**
   - Open browser: http://127.0.0.1:8000/
   - Allow camera permissions when prompted

3. **Test the system:**
   - Register a student with a clear face photo
   - Test face recognition with the webcam
   - Check attendance records

### Camera Setup

1. **Enable camera permissions** in your browser
2. **Test camera access:**
   ```bash
   python test_camera.py
   ```

3. **Common camera issues:**
   - Ensure no other application is using the camera
   - Try refreshing the page
   - Check browser camera permissions

### Performance Optimization

1. **Good lighting** for better face detection
2. **Clear, front-facing photos** for registration
3. **Close unnecessary applications** during recognition
4. **Use SSD** for better database performance

### Security Notes

- The system stores face encodings, not actual images
- Use HTTPS in production
- Regular database backups recommended
- Access control through Django admin

### Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all dependencies are installed correctly
3. Verify Python version compatibility
4. Check camera permissions and access
5. Review error messages in the console

### Development Setup

For developers:

```bash
# Install development dependencies
pip install -r requirements.txt
pip install django-debug-toolbar

# Run tests
python manage.py test

# Create superuser
python manage.py createsuperuser
```

---

**Note**: This system requires significant computational resources for face recognition. Ensure your system meets the minimum requirements for optimal performance. 