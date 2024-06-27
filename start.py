import subprocess
import os


def run_python_service(service_path):
    cmd = ['python', 'run.py']
    subprocess.Popen(cmd, cwd=service_path)


def run_frontend(frontend_path):
    cmd = ['npm', 'run', 'serve']
    subprocess.Popen(cmd, cwd=frontend_path)


if __name__ == '__main__':
    base_path = os.path.dirname(os.path.abspath(__file__))
    user_service_path = os.path.join(base_path, 'user-service')
    email_service_path = os.path.join(base_path, 'email-service')
    booking_service_path = os.path.join(base_path, 'booking-service')
    frontend_path = os.path.join(base_path, 'frontend')

    run_python_service(user_service_path)
    run_python_service(email_service_path)
    run_python_service(booking_service_path)

    run_frontend(frontend_path)
