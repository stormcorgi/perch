"""gunicorn configuration"""

wsgi_app = "flask_app:application"
chdir = "/root/perch/perch"
