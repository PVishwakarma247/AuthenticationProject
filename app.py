from flask import Flask, render_template, request, redirect, flash, session, url_for, get_flashed_messages
import random, string, os
import mysql.connector
from mysql.connector import Error
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
from dotenv import load_dotenv

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = os.getenv("KEY")
load_dotenv()

# configuration of database
def data_fetch_query(query, params=None, fetch=False):
    cursor = None
    db = None
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Root@123',
            database='authentication',
            port=3306
        )
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        db.commit()

    except Error as e:
        print(f"ERROR -> {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# EMAIL CONFIGURATION FOR VERIFICATION OF EMAIL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASS")
mail = Mail(app)


def generateOtp(length=4):
    return ''.join(random.choices(string.digits, k=length))

def sendVerificationEmail(email, otp):
    msg = Message("Verify your Email", sender=os.getenv("EMAIL"), recipients=[email])
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
        query = "select * From users where 1=1 AND email = %s"
        params = [email]
        user = data_fetch_query(query, params, fetch=True)
        if user:
            stored_password = user[0]['password']

            if check_password_hash(stored_password, password):
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
        
        query = "select * from users where 1=1 AND email = %s"
        params = [email]
        existing_user = data_fetch_query(query, params, fetch=True)
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
    query = "SELECT * FROM users WHERE email = %s"
    params = [email]
    user = data_fetch_query(query, params, fetch=True)
    return render_template('dashboard.html', user = user[0]['name'])

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

            query = "insert into users (name, email, password) values (%s, %s, %s)"
            params = [name, email, hashed_password]
            data_fetch_query(query, params)

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