"""
WSGI config for admissionproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admissionproject.settings')

application = get_wsgi_application()

try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)

    from admissionapp.models import Courses
    if Courses.objects.count() == 0:
        Courses.objects.create(course_name="B.Tech Computer Science", duration="4 Years", total_seats=60)
        Courses.objects.create(course_name="Bachelor of Business Administration (BBA)", duration="3 Years", total_seats=45)
        Courses.objects.create(course_name="Bachelor of Computer Applications (BCA)", duration="3 Years", total_seats=50)
except Exception as e:
    print(f"WSGI Auto-migration notice: {e}")

