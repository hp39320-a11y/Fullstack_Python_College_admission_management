from django.contrib import admin
from .models import Students, Courses, Applications, AcademicDetails, Documents, Payments, Register, AdminProfile

# Customizing the Django Admin Site Headers
admin.site.site_header = "Modern College Admin Portal"
admin.site.site_title = "Admissions Admin"
admin.site.index_title = "Welcome to the Admissions Backend Management"

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('gender', 'created_at')

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_name', 'duration', 'total_seats')
    search_fields = ('course_name',)

@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'student', 'course', 'application_status', 'submission_date')
    list_filter = ('application_status', 'submission_date')
    search_fields = ('student__first_name', 'course__course_name')

@admin.register(AcademicDetails)
class AcademicDetailsAdmin(admin.ModelAdmin):
    list_display = ('academic_id', 'student', 'tenth_marks', 'twelfth_marks', 'year_of_passing')
    search_fields = ('student__first_name',)

@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'student', 'document_type', 'upload_date')
    list_filter = ('document_type', 'upload_date')

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'student', 'amount', 'payment_status', 'transaction_id')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('transaction_id', 'student__first_name')

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'name', 'email', 'role')

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'email')