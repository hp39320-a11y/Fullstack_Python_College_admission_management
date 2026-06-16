# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AcademicDetails(models.Model):
    academic_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Students', models.DO_NOTHING, blank=True, null=True)
    tenth_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    twelfth_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    previous_institution = models.CharField(max_length=100, blank=True, null=True)
    year_of_passing = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'academic_details'


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class AdmissionappApplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    address = models.TextField()
    ssc_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    hsc_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10)
    applied_on = models.DateTimeField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)
    course = models.ForeignKey('AdmissionappCourse', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'admissionapp_application'


class AdmissionappCourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    fees = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'admissionapp_course'


class Applications(models.Model):
    application_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Students', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey('Courses', models.DO_NOTHING, blank=True, null=True)
    second_course = models.ForeignKey('Courses', models.DO_NOTHING, related_name='applications_second_course_set', blank=True, null=True)
    application_status = models.CharField(max_length=8, blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'applications'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    total_seats = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courses'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Documents(models.Model):
    document_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Students', models.DO_NOTHING, blank=True, null=True)
    document_type = models.CharField(max_length=50, blank=True, null=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    upload_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents'


class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Students', models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=9, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payments'


class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    aadhaar_number = models.CharField(max_length=20, blank=True, null=True)
    caste = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_phone = models.CharField(max_length=15, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'students'

class Register(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    confirm_password = models.CharField(max_length=255, blank=True, null=True)
