from flask import Flask, render_template, request, redirect, flash, session, url_for, get_flashed_messages
import pymongo, random, string
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = "nobodyhere"

# configuration of database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['credentials']
users_collection = db['loginUsers']

# EMAIL CONFIGURATION FOR VERIFICATION OF EMAIL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True # OR TLS
app.config['MAIL_USERNAME'] = 'priyanshuvishwakarma281@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'priyanshuvishwakarma281@gmail.com'
app.config['MAIL_PASSWORD'] = 'ytya oswe uxlr zxcz'
mail = Mail(app)


def generateOtp(length=4):
    return ''.join(random.choices(string.digits, k=length))

def sendVerificationEmail(email, otp):
    msg = Message("Verify your Email", sender='priyanshuvishwakarma281@gmail.com', recipients=[email])
    msg.body = f"Your Otp for email verification is: {otp}"
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email {e}")
        return False

@app.route('/', methods = ['Get', 'Post'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['pass']        
        if not(email.endswith('@gmail.com')):
            flash("Enter valid Mail", "danger")
            return render_template('login.html')
        user = users_collection.find_one({"email": email})
        if user:
            if check_password_hash(user['password'], password):
                session['email'] = email
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid password!", "danger")
        else:
            flash("User not found!", "danger")

    return render_template('login.html')

    
@app.route('/register', methods = ['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form['email']
        password = request.form['pass']

        if not(email.endswith('@gmail.com')):
            flash("Enter valid Mail", "danger")
            return render_template('register.html')

        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            flash("Email already registered! Try logging in.", "danger")
            return redirect(url_for('login'))
        
        otp = generateOtp()
        if sendVerificationEmail(email, otp):
            session['otp'] = otp
            session['email'] = email
            session['name'] = name
            session['password'] = password

            return redirect(url_for('verify'))
        
        flash("Try Again after some time", "danger")
    return render_template('register.html')
        
@app.route('/dashboard')
def dashboard():

    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session.get('email')
    user = users_collection.find_one({"email": email})
    return render_template('dashboard.html', user = user['name'])

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash("Logout Successfull!", "success")
    return redirect(url_for('login'))

@app.route('/verifyEmail', methods=['GET', 'POST'])
def verify():
    if 'otp' not in session and 'email' not in session:
        flash("UnKnownError Occured", "danger")
        return render_template('register.html')
    
    if request.method == 'POST':
        enteredOtp = request.form.get('otp', '')

        name = session.get('name')
        email = session.get('email')
        password = session.get('password')
        otp = session.get('otp')

        if not enteredOtp:
            flash("Please enter the OTP", "danger")
            return render_template('verifyEmail.html', email)

        if enteredOtp == otp:
            hashed_password = generate_password_hash(password)
            users_collection.insert_one({
                "name": name,
                "email": email,
                "password": hashed_password
            })

            session.pop('name')
            session.pop('email')
            session.pop('password')
            session.pop('otp')

            flash("Successfully registered!", "success")
            return redirect(url_for('login'))
        else:
            flash("Invalid OTP! Please try again.", "danger")
            return render_template('verifyEmail.html', email = session.get('email'))
    return render_template('verifyEmail.html', email = session.get('email'))

if __name__ == "__main__":
    app.run(debug = True)