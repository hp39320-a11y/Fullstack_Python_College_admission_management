from django.core.management import call_command
from django.db.utils import OperationalError

class AutoMigrateMiddleware:
    _migrated = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not AutoMigrateMiddleware._migrated:
            try:
                call_command('migrate', interactive=False)
                self.seed_courses()
                AutoMigrateMiddleware._migrated = True
            except Exception as e:
                print("Middleware initial migration notice:", e)

        try:
            return self.get_response(request)
        except OperationalError:
            try:
                call_command('migrate', interactive=False)
                self.seed_courses()
                AutoMigrateMiddleware._migrated = True
            except Exception as e:
                print("Middleware fallback migration notice:", e)
            return self.get_response(request)

    def seed_courses(self):
        try:
            from .models import Courses
            if Courses.objects.count() == 0:
                Courses.objects.create(course_name="B.Tech Computer Science", duration="4 Years", total_seats=60)
                Courses.objects.create(course_name="Bachelor of Business Administration (BBA)", duration="3 Years", total_seats=45)
                Courses.objects.create(course_name="Bachelor of Computer Applications (BCA)", duration="3 Years", total_seats=50)
        except Exception as e:
            print("Seeding courses notice:", e)
