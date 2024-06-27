from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Message, Mail
from form import ContactForm
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Check if the environment variables are loaded
print(os.getenv("EMAIL_USER"), "EMAIL_USER directly after load_dotenv")
print(os.getenv("EMAIL_PASS"), "EMAIL_PASS directly after load_dotenv")

app = Flask(__name__)

app.config['SECRET_KEY'] = 'lkdhhjw6u3o8udk'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USER")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASS")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Final check if the variables are loaded in app.config
print(app.config['MAIL_USERNAME'], "MAIL_USERNAME in app.config")
print(app.config['MAIL_PASSWORD'], "MAIL_PASSWORD in app.config")



@app.route('/', methods=["GET", "POST"])
def portfolio():
    form = ContactForm()
    if request.method == "POST":
        if not form.name.data and not form.email.data and not form.message.data:
            flash('All fields are required', 'danger')
            return redirect(url_for('portfolio'))
        name = form.name.data.title()
        email = form.email.data.lower()
        message = form.message.data.title()
        msg = Message('Portfolio: from ' + name, sender=email, recipients=['atmme1992@gmail.com'])
        msg.body = f'{message}\nMy email address is: {email}'
        mail.send(msg)
        flash('Message Sent', 'success')
        return render_template('portfolio.html', form=form, date=datetime.utcnow())
    return render_template('portfolio.html', form=form, date=datetime.utcnow())


if __name__ == '__main__':
    app.run(debug=True)
