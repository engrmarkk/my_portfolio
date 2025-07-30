from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Message, Mail
from form import ContactForm
import os
from dotenv import load_dotenv

# Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'lkdhhjw6u3o8udk'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USER")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASS")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/")
def portfolio():
    form = ContactForm()
    return render_template('portfolio.html', form=form, date=datetime.now())


@app.route('/send', methods=["GET", "POST"])
def send_sms():
    if request.method == "POST":
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                # Get form data from JSON
                data = request.get_json()
                name = data.get('name', '').title()
                email = data.get('email', '').lower()
                message = data.get('message', '').title()
                
                # Validate required fields
                if not name or not email or not message:
                    return jsonify({
                        'success': False,
                        'message': 'All fields are required'
                    }), 400
                
                # HTML email content
                html_content = f'''
                <div style="font-family: Arial, sans-serif; color: #222;">
                  <h2 style="color: #28a745;">New Portfolio Message</h2>
                  <p><strong>Name:</strong> {name}</p>
                  <p><strong>Email:</strong> {email}</p>
                  <p><strong>Message:</strong></p>
                  <div style="background: #f8f9fa; padding: 1em; border-radius: 5px; border: 1px solid #eee;">
                    {message}
                  </div>
                </div>
                '''
                # Send email
                msg = Message('Portfolio: from ' + name, sender=email, recipients=['atmme1992@gmail.com'])
                msg.html = html_content
                mail.send(msg)
                
                return jsonify({
                    'success': True,
                    'message': 'Message sent successfully!'
                }), 200
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': 'Failed to send message. Please try again.'
                }), 500


if __name__ == '__main__':
    app.run(debug=True)
