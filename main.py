from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, abort
import pandas as pd
from io import BytesIO
from flask import send_file

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
    try:
        new_user = Participant(
            name=request.form.get('name'),
            student_id=request.form.get('sid'),
            email=request.form.get('email'),
            event_category=request.form.get('category'),
            team_name=request.form.get('team')
        )
        db.session.add(new_user)
        db.session.commit()
        return {"status": "success"}, 200 # Sends a JSON signal back to JS
    except Exception as e:
        print(f"Error during registration: {e}")
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


@app.route('/download-data')
def download_data():
    # 1. Get password from URL for security
    entered_password = request.args.get('password')
    if entered_password != ADMIN_PASSWORD:
        abort(403)

    # 2. Fetch all participants
    participants = Participant.query.all()
    
    # 3. Create a list of dictionaries
    data = []
    for p in participants:
        data.append({
            "Name": p.name,
            "Student ID": p.student_id,
            "Email": p.email,
            "Event": p.event_category,
            "Team": p.team_name
        })

    # 4. Convert to Excel using Pandas
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Registrations')
    output.seek(0)

    return send_file(output, download_name="Ignite2026_Registrations.xlsx", as_attachment=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)