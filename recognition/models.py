from os import times
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    encoding = models.BinaryField()

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.student.name} - {self.timestamp}"

# Create your models here.
