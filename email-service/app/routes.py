import smtplib
from email.mime.text import MIMEText
from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('email', __name__)


@bp.route('/send', methods=['POST'])
def send_email():
    data = request.get_json()
    to_email = data.get('to')
    subject = data.get('subject')
    body = data.get('body')

    if not to_email or not subject or not body:
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = current_app.config['EMAIL_FROM']
        msg['To'] = to_email

        with smtplib.SMTP(current_app.config['SMTP_SERVER'], current_app.config['SMTP_PORT']) as server:
            server.starttls()
            server.login(current_app.config['SMTP_USERNAME'], current_app.config['SMTP_PASSWORD'])
            server.sendmail(current_app.config['EMAIL_FROM'], to_email, msg.as_string())

        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Failed to send email: {str(e)}'}), 500
