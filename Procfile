web: python admissionproject/manage.py migrate --noinput && gunicorn --chdir admissionproject admissionproject.wsgi:application --bind 0.0.0.0:$PORT
