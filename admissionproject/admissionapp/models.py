from django.db import models


# ---------------- Students ----------------
class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True,
        null=True
    )

    nationality = models.CharField(max_length=50, blank=True, null=True)
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True)
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

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name or "Student"


# ---------------- Courses ----------------
class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    total_seats = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.course_name or "Course"


# ---------------- Applications ----------------
class Applications(models.Model):
    application_id = models.AutoField(primary_key=True)

    student = models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='primary_applications'
    )

    second_course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='secondary_applications'
    )

    application_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )

    submission_date = models.DateTimeField(auto_now_add=True)


# ---------------- Academic Details ----------------
class AcademicDetails(models.Model):
    academic_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True)

    tenth_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    twelfth_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    previous_institution = models.CharField(max_length=100, null=True, blank=True)
    year_of_passing = models.IntegerField(null=True, blank=True)


# ---------------- Documents ----------------
class Documents(models.Model):
    document_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True)

    document_type = models.CharField(max_length=50, null=True, blank=True)
    file_path = models.CharField(max_length=255, null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)


# ---------------- Payments ----------------
class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)

    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed')
        ],
        default='Pending'
    )

    payment_date = models.DateTimeField(auto_now_add=True)


# ---------------- Admin Profile ----------------
class AdminProfile(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name or "Admin"
    
class Register(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.first_name
    
