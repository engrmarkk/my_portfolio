from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_mail import Message, Mail
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "change-me-in-production")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USER")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASS")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

RECIPIENT_EMAIL = 'atmme1992@gmail.com'


@app.route("/")
def portfolio():
    return render_template('index.html', date=datetime.now())


@app.route('/send', methods=["POST"])
def send_message():
    # Only accept AJAX/JSON requests
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request.'}), 400

    data = request.get_json()
    name    = (data.get('name', '') or '').strip().title()
    email   = (data.get('email', '') or '').strip().lower()
    message = (data.get('message', '') or '').strip()

    # Server-side validation
    if not name or not email or not message:
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'success': False, 'message': 'Please provide a valid email address.'}), 400

    html_content = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: auto;
                border: 1px solid #e0d8c8; border-radius: 6px; overflow: hidden;">
      <div style="background: #0a0a0f; padding: 24px 32px;">
        <h2 style="color: #c9a84c; margin: 0; font-size: 1.3rem; letter-spacing: 0.05em;">
          New Portfolio Message
        </h2>
      </div>
      <div style="padding: 32px; background: #fafaf8;">
        <p style="margin: 0 0 8px;"><strong>Name:</strong> {name}</p>
        <p style="margin: 0 0 8px;"><strong>Email:</strong>
          <a href="mailto:{email}" style="color: #c9a84c;">{email}</a>
        </p>
        <p style="margin: 16px 0 8px;"><strong>Message:</strong></p>
        <div style="background: #f0ece4; padding: 16px 20px; border-left: 3px solid #c9a84c;
                    border-radius: 3px; white-space: pre-wrap; color: #333; line-height: 1.6;">
          {message}
        </div>
        <p style="margin-top: 24px; font-size: 0.8rem; color: #999;">
          Sent via portfolio contact form &mdash; {datetime.now().strftime('%d %b %Y, %H:%M')}
        </p>
      </div>
    </div>
    """

    try:
        msg = Message(
            subject=f'Portfolio: New message from {name}',
            sender=app.config['MAIL_USERNAME'],   # must be your authenticated Gmail
            reply_to=email,                        # replies go back to the visitor
            recipients=[RECIPIENT_EMAIL]
        )
        msg.html = html_content
        mail.send(msg)
        return jsonify({'success': True, 'message': 'Message sent successfully!'}), 200

    except Exception as e:
        app.logger.error(f"Mail send failed: {e}")
        return jsonify({'success': False, 'message': 'Failed to send message. Please try again.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
