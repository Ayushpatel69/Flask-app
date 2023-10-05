from flask import Flask, flash, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
import smtplib, ssl
import hashlib
import requests
import sqlite3 as sql
import openai
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

openai.api_key = 'your Open-AI key'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Registration_Database.db'
app.config['SECRET_KEY'] = "your secret key"
db = SQLAlchemy(app)

# Set up Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login_main'  # The login view's name (use the function name)

# User model for SQLAlchemy
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#For creating database and databae table
class registration_details(db.Model):
    registration_id = db.Column('User_ID', db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(30), unique = True) 
    password = db.Column(db.String(256))
    # confirm_password = db.Column(db.String(256))
    address = db.Column(db.String(500))
    hobbies = db.Column(db.String(50))
    gender = db.Column(db.String(10))

    def __init__(self, first_name, last_name, email, password, confirm_password, address, hobbies, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        # self.confirm_password = confirm_password
        self.address = address
        self.hobbies = hobbies
        self.gender = gender

#For Chatgpt question answers page routing
@app.route('/Chatgpt_question', methods = ['GET', 'POST'])
def Chatgpt_question():
    return render_template('Chatgpt_question.html')


# For home registration Page
@app.route('/registration', methods= ['GET', 'POST'])
def login():
    return render_template('Registration_Form.html')

#For home Login page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('Login.html') 

#For Storing form data into database
# /add_data is a regisrtaion page 
@app.route('/add_data', methods = ['GET', 'POST'])
def add_data():
   if request.method == 'POST':
        
        #check that all the form details are entered or not
        if not request.form['first_name'] or not request.form['last_name'] or not request.form['email'] or not request.form['password'] or not request.form['confirm_password'] or not request.form['address'] or not request.form['hobbies'] or not request.form['gender'] :
            flash('Please enter all the fields...!!')
            return redirect('/add_data')

        # Check if the passwords and confirm password are same or not
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect('/add_data')
        
       
        # Hash the password using hashlib.md5 (encrytion)
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

    
        #to store hoobies data into csv in database
        hobbies = request.form.getlist('hobbies')
        hobbies_csv = ' ,'.join(hobbies)
        
        #store entered data from form to database table
        registration_database = registration_details(request.form['first_name'],
                                                      request.form['last_name'],
                                                      request.form['email'],
                                                      hashed_password, 
                                                      request.form['confirm_password'], 
                                                      request.form['address'], 
                                                      hobbies_csv, 
                                                      request.form['gender'])
        db.session.add(registration_database)
        db.session.commit()
        flash('Record was successfully added')

        # execute on un-successfully form submission to take main form
        if db.session.add(registration_database) == False :
            return redirect('/add_data')
        if db.session.add(registration_database) == True :
        #For Sending confirmation mail to registered user
            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"
            # Default Mail from where confirmation mail will be send 
            sender_email = "your sending mail "
            #receiver mail will be taken from submit from  
            receiver_email = request.form['email'] # Enter receiver address
            password = 'your 2 step verification password'
            message = """Subject: Registration Form Submission

              Hello,

              This is a confirmation message that your form data has been submitted successfully.
              """
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message) 

   # execute on successfully form submission to get  joke.html page
   return redirect('/')

# Login page
@app.route('/login_main', methods=['GET', 'POST'])
def login_main():
    error = None
    if request.method == 'POST':
        user_email = request.form.get('user_email')
        entered_password = request.form.get('user_password')

        # applying encrytion to user entered password
        user_hashed_password = hashlib.md5(entered_password.encode()).hexdigest()

        # print(passhash)
        # database_path = "/media/apnoobcoder/Data Storage/Internship_Project/registration/instance/registration_Database"
        con = sql.connect('/media/apnoobcoder/Data Storage/Internship_Project_working_07_August/registration/instance/Registration_Database.db')
        cur = con.cursor()
        statement = f"SELECT email from registration_details WHERE email='{user_email}' AND password = '{user_hashed_password}';"
        cur.execute(statement)
        if not cur.fetchone():  # An empty result evaluates to False.
            error = 'Invalid username or password. Please try again!'
            return render_template('Login.html', error=error)
        else:
            # Set user_id in session to indicate the user is logged in
            session['user_id'] = user_email
            return redirect('/joke')
    else:
        return render_template('Login.html', error=error)

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

#For Displaying joke 
@app.route('/joke')
# @login_required
def display_joke():
    if 'user_id' in session:  # Check if the user is logged in  
        url = "https://icanhazdadjoke.com/"
        headers = {"Accept": "application/json"}
    
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                joke_data = response.json()
                joke = joke_data['joke']
                return render_template('Joke.html', joke=joke)
            else:
                flash("Failed to fetch a joke. Please try again later.", "error=error")
                return redirect('/')
        except requests.exceptions.RequestException as e:
            flash(f"Failed to fetch a joke: {e}", "error")
            return redirect('/')
    else:
        flash("Please log in to view the joke.", "error")
        return redirect('/login')

#For Chatgpt Question and Answers
@app.route('/Chatgpt_answers', methods=['GET', 'POST'])
def chatgpt_answers():
    question = request.form['ask_question']
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role": 'user', "content": question}])
    answer = completion.choices[0].message['content']
    return render_template('Chatgpt_question.html', answer=answer)

if __name__ == '__main__':
   with app.app_context():
    db.create_all()
app.run(debug = True)
