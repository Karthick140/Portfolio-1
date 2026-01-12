import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-for-flashing-messages')

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

# Projects Data
PROJECTS = {
    'entrepreneurs-platform': {
        'title': 'Single Window Platform for Entrepreneurs',
        'short_desc': 'A web-based platform for government schemes and business registrations.',
        'long_desc': 'A Single Window Platform for Entrepreneurs is a Flask-based web application designed to simplify the process of starting and managing a business. The platform brings together multiple services such as business registration, scheme information, loan details, and support services in one place. The system helps entrepreneurs save time by avoiding multiple websites and offices.',
        'tech': ['Python', 'Flask', 'SQLite', 'HTML', 'CSS', 'JavaScript', 'Flask-Mail'],
        'features': ['User Registration & Login', 'Email Notifications', 'Scheme & Service Listings', 'Secure Data Handling'],
        'image': '/static/img/startup_platform.jpg'
    },
    'tnpsc-education': {
        'title': 'R-Square Academy',
        'short_desc': 'WordPress-based educational platform for exam preparation.',
        'long_desc': 'Developed a comprehensive educational platform using WordPress, specifically focused on TNPSC exam preparation. The site provides structured exam details, a complete syllabus, downloadable study materials, and real-time updates for students. It features an SEO-friendly structure and a simple, accessible layout for a seamless learning experience.',
        'tech': ['WordPress', 'PHP', 'HTML', 'CSS', 'JavaScript'],
        'features': ['Custom WordPress Theme', 'Exam Syllabus & Materials', 'SEO Optimized', 'Responsive Design'],
        'image': '/static/img/rsquare_academy.png',
        'url': 'https://rsqr.shivanaadi.com/'
    },
    'personal-portfolio': {
        'title': 'Personal Portfolio',
        'short_desc': 'Personal portfolio website to showcase skills and projects.',
        'long_desc': 'Designed and developed my personal portfolio website to showcase my skills, projects, and experience. The website is fully responsive and highlights my work in web development and software testing.',
        'tech': ['HTML', 'CSS', 'JavaScript', 'GitHub'],
        'features': ['Modern Design', 'Project Showcases', 'Responsive Layout', 'Contact Integration'],
        'image': 'https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&q=80&w=800'
    }
}

@app.route('/')
def index():
    return render_template('index.html', projects=PROJECTS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/freelance')
def freelance():
    return render_template('freelance.html')

@app.route('/project/<project_id>')
def project_detail(project_id):
    project = PROJECTS.get(project_id)
    if not project:
        return redirect(url_for('index'))
    return render_template('project_detail.html', project=project)

@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject', 'New Portfolio Contact')
        message_body = request.form.get('message')
        
        try:
            msg = Message(
                subject=f"New Message from {name}: {subject}",
                recipients=[app.config['MAIL_USERNAME']],
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_body}"
            )
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            print(f"Error sending mail: {e}")
            flash('There was an error sending your message. Please try again later.', 'error')
            
        return redirect(url_for('index', _anchor='contact'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
