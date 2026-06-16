from django.urls import path
from . import views 

urlpatterns = [
    # =========================
    # USER SIDE
    # =========================
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register_view, name='register'),
    path('register/success/', views.register_success, name='register_success'),

    path('courses/', views.course_list, name='course_list'),

    path('student-register/', views.student_register, name='student_register'),
    path('academic-details/', views.academic_details, name='academic_details'),
    path('upload-documents/', views.documents_upload, name='documents_upload'),

    path('apply/', views.apply, name='apply'),
    path('dashboard/', views.student_dashboard, name='dashboard'),

    path('payment/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('download-application-slip/',views.download_application_slip,name='download_application_slip'),
    path('download-allotment-slip/<int:student_id>/',views.download_allotment_slip,name='download_allotment_slip'),

    # =========================
    # ADMIN SIDE
    # =========================
    path('admin-register/', views.admin_register, name='admin_register'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    path('admin-panel/', views.admin_home, name='admin_home'),
    path('admin-panel/dashboard/', views.admin_dashboard_full, name='admin_dashboard'),

    path('admin-panel/students/', views.admin_students, name='admin_students'),
    path('admin-panel/students/<int:id>/', views.admin_student_detail, name='admin_student_detail'),
    path('admin-panel/applications/', views.admin_applications, name='admin_applications'),

    path('admin-panel/applications/update/<int:id>/', views.update_application, name='update_application'),

    path('admin-panel/payments/', views.admin_payments, name='admin_payments'),

    path('admin-panel/courses/', views.admin_courses, name='admin_courses'),
    path('admin-panel/courses/add/', views.add_course, name='add_course'),
    path('admin-panel/courses/delete/<int:id>/', views.delete_course, name='delete_course'),
    path('admin-panel/students/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('admin-panel/students-full-table/',views.students_full_table,name='students_full_table'),
    path('admin-panel/export-students-excel/',views.export_students_excel,name='export_students_excel'),

]