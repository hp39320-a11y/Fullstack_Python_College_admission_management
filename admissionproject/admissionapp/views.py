from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .decorators import admin_required
from .models import Courses, Applications, Register, Students, AcademicDetails, Documents, Payments, AdminProfile
import requests
from django.http import HttpResponse
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.units import inch
from django.conf import settings
import os
from openpyxl import Workbook

def home(request):
    courses = Courses.objects.all()[:3]   # ✅ FIXED
    return render(request, 'admissionapp/home.html', {'courses': courses})


def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "admissionapp/register.html", {
                "error": "Passwords do not match"
            })

        if Register.objects.filter(email=email).exists():
            return render(request, "admissionapp/register.html", {
                "error": "Email already exists"
            })

        user = Register.objects.create(
            first_name=name,
            email=email,
            password=password
        )

        # Redirect to success page
        return redirect("register_success")

    return render(request, "admissionapp/register.html")


def register_success(request):
    return render(request, "admissionapp/register_success.html")


def sync_student_id(request):
    """Ensure student_id is in session if a Students record exists for this user."""
    if 'student_id' not in request.session and 'user_id' in request.session:
        try:
            user = Register.objects.get(student_id=request.session['user_id'])
            student = Students.objects.filter(email=user.email).first()
            if student:
                request.session['student_id'] = student.student_id
                return student
        except Register.DoesNotExist:
            pass
    elif 'student_id' in request.session:
        return Students.objects.filter(student_id=request.session['student_id']).first()
    return None

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(email=email, password=password)

            # store session
            request.session['user_id'] = user.student_id
            request.session['user_name'] = user.first_name
            
            # Sync student_id if they already completed full registration
            sync_student_id(request)

            return redirect('home')

        except Register.DoesNotExist:
            return render(request, 'admissionapp/login.html', {
                'error': 'Invalid email or password'
            })

    return render(request, 'admissionapp/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def course_list(request):
    courses = Courses.objects.all()   # ✅ FIXED
    return render(request, 'admissionapp/courses.html', {'courses': courses})


def student_register(request):
    if 'user_id' not in request.session:
        return redirect('login')

    if request.method == "POST":
        student = Students.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            password=request.POST.get('password'),
            date_of_birth=request.POST.get('date_of_birth'),
            gender=request.POST.get('gender'),
            nationality=request.POST.get('nationality'),
            aadhaar_number=request.POST.get('aadhaar_number'),
            caste=request.POST.get('caste'),
            religion=request.POST.get('religion'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            father_name=request.POST.get('father_name'),
            father_phone=request.POST.get('father_phone'),
            mother_name=request.POST.get('mother_name'),
            mother_phone=request.POST.get('mother_phone'),
        )

        request.session['student_id'] = student.student_id

        return redirect('academic_details')

    return render(request, 'admissionapp/student_register.html')

def academic_details(request):
    student = sync_student_id(request)
    if not student:
        messages.warning(request, "Please complete your personal registration first.")
        return redirect('student_register')

    # Fetch existing record if it exists
    academic_record = AcademicDetails.objects.filter(student=student).first()

    if request.method == "POST":
        try:
            # Use update_or_create to prevent multiple records for the same student
            AcademicDetails.objects.update_or_create(
                student=student,
                defaults={
                    'tenth_marks': request.POST.get('tenth_marks') or None,
                    'twelfth_marks': request.POST.get('twelfth_marks') or None,
                    'previous_institution': request.POST.get('previous_institution'),
                    'year_of_passing': request.POST.get('year_of_passing') or None,
                }
            )
            messages.success(request, "Academic details updated successfully.")
            return redirect('documents_upload')
        except Exception as e:
            messages.error(request, f"Error saving academic details: {e}")
            return render(request, 'admissionapp/academic_details.html', {
                'error': str(e),
                'academic': academic_record
            })
        
    return render(request, 'admissionapp/academic_details.html', {'academic': academic_record})

from django.core.files.storage import FileSystemStorage

def documents_upload(request):
    student = sync_student_id(request)
    if not student:
        return redirect('student_register')

    if request.method == "POST":
        fs = FileSystemStorage()

        # Handle 10th Marksheet
        if 'tenth_doc' in request.FILES:
            tenth_file = request.FILES['tenth_doc']
            tenth_name = fs.save(f"documents/{student.student_id}_10th_{tenth_file.name}", tenth_file)
            Documents.objects.create(student=student, document_type="10th Marksheet", file_path=fs.url(tenth_name))

        # Handle 12th Marksheet
        if 'twelfth_doc' in request.FILES:
            twelfth_file = request.FILES['twelfth_doc']
            twelfth_name = fs.save(f"documents/{student.student_id}_12th_{twelfth_file.name}", twelfth_file)
            Documents.objects.create(student=student, document_type="12th Marksheet", file_path=fs.url(twelfth_name))

        # Handle ID Proof
        if 'id_doc' in request.FILES:
            id_file = request.FILES['id_doc']
            id_name = fs.save(f"documents/{student.student_id}_id_{id_file.name}", id_file)
            Documents.objects.create(student=student, document_type="ID Proof", file_path=fs.url(id_name))

        return redirect('apply')

    return render(request, 'admissionapp/documents_upload.html')
def apply(request):
    student = sync_student_id(request)
    if not student:
        return redirect('login')

    if request.method == "POST":
        primary_course = request.POST.get("primary_course")
        second_course = request.POST.get("second_course")

        Applications.objects.create(
            student=student,
            course_id=primary_course,
            second_course_id=second_course if second_course else None
        )

        return redirect('payment')

    return render(request, 'admissionapp/apply.html', {
        'courses': Courses.objects.all()
    })
RAZORPAY_KEY_ID = getattr(settings, 'RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def payment(request):
    if 'student_id' not in request.session:
        return redirect('student_register')

    student = Students.objects.get(student_id=request.session['student_id'])
    amount = 500 # Application fee is static: 500 Rs
    currency = "INR"

    try:
        razorpay_order = razorpay_client.order.create({
            "amount": int(amount * 100),
            "currency": currency,
            "payment_capture": "1"
        })
        order_id = razorpay_order['id']
    except Exception as e:
        # Fallback for dummy/missing test keys so page renders
        print(f"Razorpay Error: {e}")
        order_id = "order_test_fallback"

    payment_record = Payments.objects.create(
        student=student,
        amount=amount,
        payment_method='Razorpay',
        transaction_id=order_id,
        payment_status='Pending'
    )

    context = {
        'amount': amount,
        'razorpay_order_id': order_id,
        'razorpay_merchant_key': RAZORPAY_KEY_ID,
        'currency': currency,
        'student': student
    }
    return render(request, 'admissionapp/payment.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            })

            payment_record = Payments.objects.get(transaction_id=order_id)
            payment_record.payment_status = 'Completed'
            payment_record.save()

            return render(request, 'admissionapp/payment_success.html')

        except razorpay.errors.SignatureVerificationError:
            payment_record = Payments.objects.get(transaction_id=order_id)
            payment_record.payment_status = 'Failed'
            payment_record.save()

            return render(request, 'admissionapp/payment_failed.html')

    return redirect('home')
def course_list(request):
    courses = Courses.objects.all()
    return render(request, 'admissionapp/courses.html', {'courses': courses})


# ✅ ADMIN REGISTER
def admin_register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if AdminProfile.objects.filter(email=email).exists():
            return render(request, "adminpanel/admin_register.html", {
                "error": "Email already exists"
            })

        AdminProfile.objects.create(
            name=name,
            email=email,
            password=make_password(password)
        )

        return redirect("admin_login")

    return render(request, "adminpanel/admin_register.html")


# ✅ ADMIN LOGIN
def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            admin = AdminProfile.objects.get(email=email)

            if check_password(password, admin.password):
                request.session['admin_id'] = admin.admin_id
                request.session['admin_name'] = admin.name
                request.session['is_admin'] = True   # ✅ ADD THIS

                return redirect('admin_home')
            else:
                raise AdminProfile.DoesNotExist

        except AdminProfile.DoesNotExist:
            return render(request, "adminpanel/admin_login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "adminpanel/admin_login.html")
# ✅ LOGOUT
def admin_logout(request):
    request.session.flush()
    return redirect("home")

def check_admin(request):
    return request.session.get('is_admin')


@admin_required
def admin_home(request):
    if not check_admin(request):
        return redirect('admin_login')

    # Statistics for Dashboard
    total_students = Students.objects.count()
    total_applications = Applications.objects.count()
    pending_applications = Applications.objects.filter(application_status='Pending').count()
    total_courses = Courses.objects.count()
    
    # Calculate Total Revenue
    from django.db.models import Sum
    total_revenue = Payments.objects.filter(payment_status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
    
    recent_applications = Applications.objects.all().order_by('-submission_date')[:5]
    recent_payments = Payments.objects.all().order_by('-payment_date')[:5]

    context = {
        'total_students': total_students,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'total_courses': total_courses,
        'total_revenue': total_revenue,
        'recent_applications': recent_applications,
        'recent_payments': recent_payments,
    }

    return render(request, 'adminpanel/dashboard.html', context)

@admin_required
def admin_dashboard_full(request):
    if not check_admin(request):
        return redirect('admin_login')
    return render(request, 'adminpanel/powerbi_dashboard.html')

@admin_required
def admin_students(request):
    students = Students.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/students.html', {'students': students})


# VIEW SINGLE STUDENT FULL DETAILS
@admin_required
def admin_student_detail(request, id):
    student = Students.objects.get(student_id=id)
    applications = Applications.objects.filter(student=student)
    documents = Documents.objects.filter(student=student)
    academic = AcademicDetails.objects.filter(student=student).first()
    
    return render(request, 'adminpanel/student_detail.html', {
        'student': student,
        'applications': applications,
        'documents': documents,
        'academic': academic
    })

@admin_required
def admin_applications(request):
    if not check_admin(request):
        return redirect('admin_login')

    applications = Applications.objects.all()
    return render(request, 'adminpanel/applications.html', {'applications': applications})

@admin_required
def update_application(request, id):

    if not check_admin(request):
        return redirect('admin_login')

    app = Applications.objects.get(application_id=id)

    if request.method == "POST":

        # OLD STATUS
        old_status = app.application_status

        # NEW STATUS
        new_status = request.POST.get('status')

        # COURSE
        course = app.course

        # =========================
        # MANAGE SEATS
        # =========================

        if course:

            # Pending → Approved
            if new_status == 'Approved' and old_status != 'Approved':

                if course.total_seats and course.total_seats > 0:
                    course.total_seats -= 1
                    course.save()

            # Approved → Other
            elif new_status != 'Approved' and old_status == 'Approved':

                course.total_seats += 1
                course.save()

        # =========================
        # UPDATE APPLICATION STATUS
        # =========================

        app.application_status = new_status
        app.save()

        # =========================
        # SEND EMAIL USING N8N
        # =========================

        # Only first time approval
        if new_status == "Approved" and old_status != "Approved":

            data = {
                "student_name": app.student.first_name,
                "email": app.student.email,
                "course": app.course.course_name,
            }

            print("Sending Data To n8n:")
            print(data)

            try:

                response = requests.post(
                    "https://harip2005.app.n8n.cloud/webhook/admission-approved",
                    json=data
                )

                print("Status Code:", response.status_code)
                print("Response:", response.text)

            except Exception as e:

                print("Webhook Error:", e)

        return redirect('admin_applications')

    return render(request, 'adminpanel/update_application.html', {
        'app': app
    })
@admin_required
def admin_payments(request):
    if not check_admin(request):
        return redirect('admin_login')

    payments = Payments.objects.all()
    return render(request, 'adminpanel/payments.html', {'payments': payments})

@admin_required
def admin_courses(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    courses = Courses.objects.all()
    return render(request, 'adminpanel/courses.html', {'courses': courses})


# ADD COURSE
@admin_required
def add_course(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    if request.method == "POST":
        Courses.objects.create(
            course_name=request.POST.get('course_name'),
            duration=request.POST.get('duration'),
            total_seats=request.POST.get('total_seats'),
        )
        return redirect('admin_courses')

    return render(request, 'adminpanel/add_course.html')


# DELETE COURSE
@admin_required
def delete_course(request, id):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    course = Courses.objects.get(course_id=id)
    course.delete()

    return redirect('admin_courses')

def delete_student(request, id):
    student = get_object_or_404(Students, student_id=id)
    student.delete()
    return redirect('admin_students')

def student_dashboard(request):
    # Check if student is logged in
    user_id = request.session.get('user_id')
    student_id = request.session.get('student_id')

    if not user_id and not student_id:
        return redirect('login')

    # If we have student_id in session, use it
    if student_id:
        student = get_object_or_404(Students, student_id=student_id)
    else:
        # Check if a student record exists for this user email
        reg_user = get_object_or_404(Register, student_id=user_id)
        student = Students.objects.filter(email=reg_user.email).first()
        if not student:
            # No detailed registration yet
            return redirect('student_register')
        # Store in session for future
        request.session['student_id'] = student.student_id

    applications = Applications.objects.filter(student=student).order_by('-submission_date')
    latest_application = applications.first()
    payments = Payments.objects.filter(student=student).order_by('-payment_date')
    academic = AcademicDetails.objects.filter(student=student).first()
    
    return render(request, 'admissionapp/dashboard.html', {
        'student': student,
        'applications': applications,
        'application': latest_application,
        'payments': payments,
        'academic': academic
    })

def download_application_slip(request):

    # LOGIN CHECK
    if 'student_id' not in request.session:
        return redirect('login')

    try:
        student = Students.objects.get(
            student_id=request.session['student_id']
        )

    except Students.DoesNotExist:
        return redirect('login')

    # FETCH DATA
    application = Applications.objects.filter(
        student=student
    ).last()

    payment = Payments.objects.filter(
        student=student
    ).last()

    academic = AcademicDetails.objects.filter(
        student=student
    ).first()

    # PDF RESPONSE
    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="Application_Slip_{student.student_id}.pdf"'
    )

    # DOCUMENT
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    elements = []

    # SECTION STYLE
    style_section = styles['Heading2']

    style_section.textColor = colors.HexColor("#1e3a8a")

    style_section.fontSize = 14

    style_section.spaceBefore = 20

    style_section.spaceAfter = 10

    # ==========================================
    # HEADER
    # ==========================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        'admissionapp/static/admissionapp/images/logo.png'
    )

    if os.path.exists(logo_path):

        logo_img = Image(
            logo_path,
            width=0.9 * inch,
            height=0.9 * inch
        )

    else:
        logo_img = ""

    college_info = Paragraph(
        """
        <font size="22" color="#1e3a8a">
        <b>NEW MEN COLLEGE</b>
        </font>

        <br/>

        <font size="10" color="#64748b">

        NH Bypass Road, Kochi, Kerala - 682001

        <br/>

        Phone: +91 9876543210

        <br/>

        Email: admissions@newmencollege.com

        </font>
        """,
        styles['Normal']
    )

    header_table = Table(
        [[logo_img, college_info]],
        colWidths=[1.2 * inch, 5.0 * inch]
    )

    header_table.setStyle(TableStyle([

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('ALIGN', (0, 0), (0, 0), 'LEFT'),

    ]))

    elements.append(header_table)

    elements.append(Spacer(1, 10))

    elements.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#cbd5e1")
        )
    )

    elements.append(Spacer(1, 15))

    # ==========================================
    # TITLE
    # ==========================================

    elements.append(

        Paragraph(
            "<b>ADMISSION APPLICATION SLIP (2026-27)</b>",
            styles['Heading1']
        )

    )

    elements.append(Spacer(1, 20))

    # ==========================================
    # PERSONAL DETAILS
    # ==========================================

    elements.append(

        Paragraph(
            "<b>PERSONAL DETAILS</b>",
            style_section
        )

    )

    personal_data = [

        ['Student Name',
         f"{student.first_name} {student.last_name}"],

        ['Student ID',
         f"NMC-{student.student_id:04d}"],

        ['Application ID',
         f"APP-{application.application_id:04d}"
         if application else "N/A"],

        ['Email Address',
         student.email],

        ['Phone Number',
         student.phone],

        ['Date of Birth',
         student.date_of_birth.strftime('%d %b, %Y')
         if student.date_of_birth else "N/A"],

        ['Gender',
         student.gender],

        ['Address',
         Paragraph(
             f"{student.address}, {student.city}, "
             f"{student.state} - {student.zip_code}",
             styles['Normal']
         )],

        ['Guardian Details',
         f"{student.father_name} (Father), "
         f"{student.mother_name} (Mother)"],

    ]

    t_personal = Table(
        personal_data,
        colWidths=[170, 330]
    )

    t_personal.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (0, -1),
         colors.HexColor("#f8fafc")),

        ('TEXTCOLOR', (0, 0), (0, -1),
         colors.HexColor("#475569")),

        ('FONTNAME', (0, 0), (0, -1),
         'Helvetica-Bold'),

        ('GRID', (0, 0), (-1, -1),
         0.5, colors.HexColor("#e2e8f0")),

        ('BOTTOMPADDING', (0, 0), (-1, -1),
         10),

        ('TOPPADDING', (0, 0), (-1, -1),
         10),

        ('LEFTPADDING', (0, 0), (-1, -1),
         12),

        ('VALIGN', (0, 0), (-1, -1),
         'MIDDLE'),

    ]))

    elements.append(t_personal)

    # ==========================================
    # ADMISSION DETAILS
    # ==========================================

    elements.append(

        Paragraph(
            "<b>ADMISSION & PAYMENT DETAILS</b>",
            style_section
        )

    )

    admission_data = [

        ['Applied Course',
         application.course.course_name
         if application else "N/A"],

        ['Second Preference',
         application.second_course.course_name
         if application and application.second_course else "-"],

        ['Submission Date',
         application.submission_date.strftime('%d %b, %Y')
         if application else "N/A"],

        ['Application Status',
         application.application_status
         if application else "N/A"],

        ['Payment Status',
         payment.payment_status
         if payment else "Unpaid"],

        ['Amount Paid',
         f"INR {payment.amount}"
         if payment else "N/A"],

        ['Transaction ID',
         payment.transaction_id
         if payment else "N/A"],

    ]

    t_admission = Table(
        admission_data,
        colWidths=[170, 330]
    )

    t_admission.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (0, -1),
         colors.HexColor("#f8fafc")),

        ('TEXTCOLOR', (0, 0), (0, -1),
         colors.HexColor("#475569")),

        ('FONTNAME', (0, 0), (0, -1),
         'Helvetica-Bold'),

        ('GRID', (0, 0), (-1, -1),
         0.5, colors.HexColor("#e2e8f0")),

        ('BOTTOMPADDING', (0, 0), (-1, -1),
         10),

        ('TOPPADDING', (0, 0), (-1, -1),
         10),

        ('LEFTPADDING', (0, 0), (-1, -1),
         12),

    ]))

    elements.append(t_admission)

    # ==========================================
    # ACADEMIC DETAILS
    # ==========================================

    if academic:

        elements.append(

            Paragraph(
                "<b>ACADEMIC DETAILS</b>",
                style_section
            )

        )

        academic_data = [

            ['10th Marks',
             f"{academic.tenth_marks}%"],

            ['12th Marks',
             f"{academic.twelfth_marks}%"],

            ['Year of Passing',
             str(academic.year_of_passing)],

            ['Previous Institution',
             academic.previous_institution],

        ]

        t_academic = Table(
            academic_data,
            colWidths=[170, 330]
        )

        t_academic.setStyle(TableStyle([

            ('BACKGROUND', (0, 0), (0, -1),
             colors.HexColor("#f8fafc")),

            ('TEXTCOLOR', (0, 0), (0, -1),
             colors.HexColor("#475569")),

            ('FONTNAME', (0, 0), (0, -1),
             'Helvetica-Bold'),

            ('GRID', (0, 0), (-1, -1),
             0.5, colors.HexColor("#e2e8f0")),

            ('BOTTOMPADDING', (0, 0), (-1, -1),
             10),

            ('TOPPADDING', (0, 0), (-1, -1),
             10),

            ('LEFTPADDING', (0, 0), (-1, -1),
             12),

        ]))

        elements.append(t_academic)

    # ==========================================
    # DECLARATION
    # ==========================================

    elements.append(Spacer(1, 35))

    elements.append(

        Paragraph(
            "<b>DECLARATION</b>",
            style_section
        )

    )

    declaration_text = f"""

    <font size="10" color="#334155">

    I, <b>{student.first_name} {student.last_name}</b>,
    son/daughter of <b>{student.father_name}</b>,
    hereby declare that all information provided in this
    application form is true and correct.

    <br/><br/>

    I understand that admission will be confirmed only
    after verification of original documents and payment
    of required admission fees.

    </font>

    """

    elements.append(

        Paragraph(
            declaration_text,
            styles['BodyText']
        )

    )

    elements.append(Spacer(1, 60))

    # ==========================================
    # NAME SECTION
    # ==========================================

    signature_data = [[

        Paragraph(
            f"""
            <para align="center">

            ___________________________

            <br/><br/>

            <b>{student.first_name} {student.last_name}</b>

            <br/>

            Name of Applicant

            </para>
            """,
            styles['Normal']
        ),

        Paragraph(
            f"""
            <para align="center">

            ___________________________

            <br/><br/>

            <b>{student.father_name}</b>

            <br/>

            Name of Parent / Guardian

            </para>
            """,
            styles['Normal']
        )

    ]]

    signature_table = Table(
        signature_data,
        colWidths=[250, 250]
    )

    signature_table.setStyle(TableStyle([

        ('ALIGN', (0, 0), (-1, -1),
         'CENTER'),

        ('VALIGN', (0, 0), (-1, -1),
         'MIDDLE'),

    ]))

    elements.append(signature_table)

    elements.append(Spacer(1, 30))

    # ==========================================
    # FOOTER
    # ==========================================

    footer_text = """

    <font size="8" color="#64748b">

    This is a computer-generated application slip.

    <br/><br/>

    Please bring this slip and all original documents
    during admission verification.

    </font>

    """

    elements.append(

        Paragraph(
            footer_text,
            styles['Normal']
        )

    )

    # BUILD PDF
    doc.build(elements)

    return response
def download_allotment_slip(request, student_id):

    try:

        student = Students.objects.get(
            student_id=student_id
        )

    except Students.DoesNotExist:

        return HttpResponse("Student Not Found")

    application = Applications.objects.filter(
        student=student
    ).last()

    payment = Payments.objects.filter(
        student=student
    ).last()

    academic = AcademicDetails.objects.filter(
        student=student
    ).first()

    if not application:

        return HttpResponse(
            "No application found."
        )

    if application.application_status != "Approved":

        return HttpResponse(
            "Allotment Slip Available Only After Approval."
        )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="Allotment_Slip_{student.student_id}.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    elements = []

    style_section = styles['Heading2']

    style_section.textColor = colors.HexColor("#1e3a8a")

    style_section.fontSize = 14

    logo_path = os.path.join(
        settings.BASE_DIR,
        'admissionapp/static/admissionapp/images/logo.png'
    )

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=0.9 * inch,
            height=0.9 * inch
        )

    else:

        logo = ""

    college_info = Paragraph(
        """
        <font size="22" color="#1e3a8a">
        <b>NEW MEN COLLEGE</b>
        </font>

        <br/>

        <font size="10" color="#64748b">

        NH Bypass Road, Kochi, Kerala - 682001

        <br/>

        Phone: +91 9876543210

        <br/>

        Email: admissions@newmencollege.com

        </font>
        """,
        styles['Normal']
    )

    header_table = Table(
        [[logo, college_info]],
        colWidths=[1.2 * inch, 5 * inch]
    )

    elements.append(header_table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "<b>PROVISIONAL ALLOTMENT SLIP</b>",
            styles['Heading1']
        )
    )

    elements.append(Spacer(1, 20))

    student_data = [

        ['Student Name',
         f"{student.first_name} {student.last_name}"],

        ['Student ID',
         f"NMC-{student.student_id:04d}"],

        ['Course',
         application.course.course_name],

        ['Application Status',
         application.application_status],

        ['Father Name',
         student.father_name],

        ['Phone',
         student.phone],

        ['Email',
         student.email],

    ]

    table = Table(
        student_data,
        colWidths=[180, 320]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (0, -1),
         colors.HexColor("#f1f5f9")),

        ('FONTNAME', (0, 0), (0, -1),
         'Helvetica-Bold'),

        ('GRID', (0, 0), (-1, -1),
         0.5, colors.grey),

        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),

        ('TOPPADDING', (0, 0), (-1, -1), 10),

    ]))

    elements.append(table)

    elements.append(Spacer(1, 30))

    note = Paragraph(
        """
        <font size="10">

        Please carry this allotment slip along with
        all original documents during admission verification.

        </font>
        """,
        styles['BodyText']
    )

    elements.append(note)

    doc.build(elements)

    return response

@admin_required
def students_full_table(request):

    students = Students.objects.all().order_by('-student_id')

    student_data = []

    for student in students:

        academic = AcademicDetails.objects.filter(
            student=student
        ).first()

        application = Applications.objects.filter(
            student=student
        ).last()

        student_data.append({

            'student': student,

            'academic': academic,

            'application': application

        })

    return render(
        request,
        'adminpanel/students_table.html',
        {
            'student_data': student_data
        }
    )

@admin_required
def export_students_excel(request):

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Students"

    headers = [

        'Student ID',
        'Name',
        'Email',
        'Phone',
        'DOB',
        'Gender',
        'Nationality',
        'Aadhaar',
        'Caste',
        'Religion',
        'Father',
        'Mother',
        '10th Marks',
        '12th Marks',
        'Institution',
        'Year',
        'Course',
        'Status'

    ]

    worksheet.append(headers)

    students = Students.objects.all()

    for student in students:

        academic = AcademicDetails.objects.filter(
            student=student
        ).first()

        application = Applications.objects.filter(
            student=student
        ).last()

        worksheet.append([

            student.student_id,

            f"{student.first_name} {student.last_name}",

            student.email,

            student.phone,

            str(student.date_of_birth),

            student.gender,

            student.nationality,

            student.aadhaar_number,

            student.caste,

            student.religion,

            student.father_name,

            student.mother_name,

            academic.tenth_marks if academic else "N/A",

            academic.twelfth_marks if academic else "N/A",

            academic.previous_institution if academic else "N/A",

            academic.year_of_passing if academic else "N/A",

            application.course.course_name
            if application else "N/A",

            application.application_status
            if application else "N/A"

        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = (
        'attachment; filename=students.xlsx'
    )

    workbook.save(response)

    return response