import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admissionproject.settings')
django.setup()

from admissionapp.models import Course
from django.contrib.auth.models import User

# Create courses
courses = [
    {
        'name': 'B.Tech Computer Science',
        'description': 'Advanced computer science course with focus on AI, Data Science and Software Engineering.',
        'duration': '4 Years',
        'fees': 15000.00
    },
    {
        'name': 'B.Tech Information Technology',
        'description': 'Comprehensive study of networks, security, and enterprise systems.',
        'duration': '4 Years',
        'fees': 14000.00
    },
    {
        'name': 'B.Des Graphic Design',
        'description': 'Master the art of visual communication and digital experience design.',
        'duration': '3 Years',
        'fees': 12000.00
    },
    {
        'name': 'BBA Marketing',
        'description': 'Understand market dynamics and consumer behavior in the digital age.',
        'duration': '3 Years',
        'fees': 10000.00
    }
]

for c_data in courses:
    course, created = Course.objects.get_or_create(
        name=c_data['name'],
        defaults={
            'description': c_data['description'],
            'duration': c_data['duration'],
            'fees': c_data['fees']
        }
    )
    if created:
        print(f"Created course: {course.name}")
    else:
        print(f"Course already exists: {course.name}")

# Create superuser if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin@123')
    print("Created superuser: admin / admin@123")
else:
    print("Superuser already exists.")
