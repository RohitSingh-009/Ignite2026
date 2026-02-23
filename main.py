from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ignite_secret_key'

# ✅ FIX HERE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model for Students
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    event_category = db.Column(db.String(50))  # Tech, Sports, Esports
    team_name = db.Column(db.String(100))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    new_user = Participant(
        name=request.form.get('name'),
        student_id=request.form.get('sid'),
        email=request.form.get('email'),
        event_category=request.form.get('category'),
        team_name=request.form.get('team')
    )
    db.session.add(new_user)
    db.session.commit()
    return "Registration Successful! See you at Ignite 2026."




# Set your secret password here
ADMIN_PASSWORD = "IgniteAdmin2026"

@app.route('/admin-ignite')
def admin_dashboard():
    # Check if the URL has ?password=IgniteAdmin2026
    entered_password = request.args.get('password')
    
    if entered_password != ADMIN_PASSWORD:
        # If password is wrong, show a 403 Forbidden error
        abort(403) 
    
    all_participants = Participant.query.all()
    return render_template('admin.html', participants=all_participants)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)