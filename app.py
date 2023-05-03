from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import datetime
import bcrypt
import re
import mask as mask
import logging

app = Flask(__name__)
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
dbname = 'northwind'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://postgres:1234@localhost:5432/northwind'
#app.config['SQLALCHEMY_DATABASE_URL'] = 'postgres://username:password@localhost:5432/dbname'

db = SQLAlchemy(app)

class Contacts(db.Model):
    '''
    sno, name, phone_num, Subject,  email, timestamp
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone_num = db.Column(db.String(10), nullable=False)
    Subject = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


class Loginn(db.Model):
    '''
    sno,username,password,timestamp
    '''
    sno = db.Column(db.Integer, primary_key=True )
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

class Salt(db.Model):
    '''
    email,salt
    '''
    email = db.Column(db.String(50), primary_key=True)
    salt = db.Column(db.String(200), nullable=False)

class Signup(db.Model):
    '''
    email,password,repeatpassword,timestamp
    '''
    email = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    confirm_password=db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    


class Booki(db.Model):
    '''
    sno,name,email,phone,date_and_time,timestamp
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    date_and_time = db.Column(db.DateTime, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

@app.route("/")
def home():
    app.logger.info('Homepage accessed.')
    return render_template("index.html")

@app.route("/index1")
def home1():
    app.logger.info('Homepage 1 accessed.')
    return render_template("index1.html")

@app.route("/index2")
def home2():
    app.logger.info('Homepage 2 accessed.')
    return render_template("index2.html")


@app.route("/about")
def about():
    app.logger.info('About page accessed.')
    return render_template("about.html")

@app.route("/about1")
def about1():
    app.logger.info('About page 1 accessed.')
    return render_template("about1.html")

@app.route("/about2")
def about2():
    app.logger.info('About page 2 accessed.')
    return render_template("about2.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        Subject = request.form.get('Subject')
        timestamp = datetime.datetime.now()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            app.logger.error('Invalid email address entered.')
            return "Invalid email address. Please try again."

        phone_regex = r'^\d{10,12}$'
        if not re.match(phone_regex, phone):
            error = "Phone number must be between 10 and 12 digits."
            app.logger.error('Invalid Phone Number entered.')
            return "Invalid Phone Number. Please try again."

        entry = Contacts(name=name, phone_num=phone, Subject=Subject, email=email,timestamp=timestamp)
        db.session.add(entry)
        db.session.commit()
        app.logger.info('Contact entry added successfully')
        return "Contact entry added successfully!"
    app.logger.info("contact page accessed")
    return render_template("contact.html")

@app.route("/contact1", methods=['GET', 'POST'])
def contact1():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        Subject = request.form.get('Subject')
        timestamp = datetime.datetime.now()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            app.logger.error('Invalid email address entered.')
            return "Invalid email address. Please try again."

        phone_regex = r'^\d{10,12}$'
        if not re.match(phone_regex, phone):
            error = "Phone number must be between 10 and 12 digits."
            app.logger.error('Invalid Phone Number entered.')
            return "Invalid Phone Number. Please try again."
        entry = Contacts(name=name, phone_num=phone, Subject=Subject, email=email,timestamp=timestamp)
        db.session.add(entry)
        db.session.commit()
        app.logger.info('Contact entry added successfully')
        return "Contact entry added successfully!"
    app.logger.info("contact 1 page accessed")
    return render_template("contact1.html")

 

@app.route("/contact2", methods=['GET', 'POST'])
def contact2():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        Subject = request.form.get('Subject')
        timestamp = datetime.datetime.now()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            app.logger.error('Invalid email address entered.')
            return "Invalid email address. Please try again."

        phone_regex = r'^\d{10,12}$'
        if not re.match(phone_regex, phone):
            error = "Phone number must be between 10 and 12 digits."
            app.logger.error('Invalid Phone Number entered.')
            return "Invalid Phone Number. Please try again."

        entry = Contacts(name=name, phone_num=phone, Subject=Subject, email=email,timestamp=timestamp)
        db.session.add(entry)
        db.session.commit()
        app.logger("Contact entry added successfully")
        return "Contact entry added successfully!"
    app.logger.info("contact 2 page accessed")
    return render_template("contact2.html")


@app.route("/login_form", methods=['GET', 'POST'])
def logg():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get("password")
        timestamp = datetime.datetime.now()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            app.logger.error('Invalid email address entered.')
            return "Invalid email address. Please try again."
        
        user = Signup.query.filter_by(email=email).first()
        if not user:
            app.logger.warning('Invalid username or password entered.')
            return "Invalid username or password"
        hashed = bcrypt.hashpw(password.encode('utf-8'), mask.mask)
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        
            entry = Loginn(email=email, password=hashed,timestamp=timestamp)
            db.session.add(entry)  
            db.session.commit()
            salt_entry = Salt.query.filter_by(email=email).first()
            if salt_entry:
                salt = salt_entry.salt
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
                user = Signup.query.filter_by(email=email, password=hashed_password).first()
                if user:
                    app.logger.warning('User has successfully logged in.')
                    return render_template('index2.html', ans="Logged in successfully.")
                else:
                    app.logger.warning('Salt entry not found for the given user.')
                    return "Invalid username or password"
    app.logger.info("login page accessed")
    return render_template('login_form.html')

    

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        timestamp = datetime.datetime.now()

        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
          app.logger.error('Invalid email address entered.')
          return "Invalid email address. Please try again."
        
        if password != confirm_password:
            app.logger.error('Password and Confirm Password do not match. Please try again.')
            return "Password and Confirm Password do not match. Please try again."
        
        salt = bcrypt.gensalt().decode('utf-8')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
        
        user = Signup.query.filter_by(email=email).first()
        if user:
          app.logger.error('User already exists. Please log in.')
          return "User already exists. Please log in."
        
        entry = Signup(email=email, password=hashed_password, confirm_password=confirm_password,timestamp=timestamp)
        db.session.add(entry)
        db.session.commit()
        
        salt_entry = Salt(email=email, salt=salt)
        db.session.add(salt_entry)
        db.session.commit()

        app.logger.info('User signed up successfully.')
        return render_template('index1.html' ,ans="User signed up successfully.")
    else:
        app.logger.debug('Returning sign-up page.')
        return render_template('sign_up.html')


@app.route("/book", methods = ['GET','POST'])
def book():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email =request.form.get('email')
        phone= request.form.get('phone')
        date_and_time= request.form.get('date_and_time')
        timestamp = datetime.datetime.now()

        input_datetime = datetime.datetime.strptime(date_and_time, '%Y-%m-%dT%H:%M')
        current_datetime = datetime.datetime.now()
        if input_datetime <= current_datetime:
            app.logger.error('Invalid date and time entered.')
            return "Invalid date and time. Please try again."
        



        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            app.logger.error("Invalid email address entered.")
            return "Invalid email address. Please try again."

        phone_regex = r'^\d{10,12}$'
        if not re.match(phone_regex, phone):
            error = "Phone number must be between 10 and 12 digits."
            app.logger.error('Invalid Phone Number entered.')
            return "Invalid Phone Number. Please try again."
        
        existing_booking = Booki.query.filter_by(date_and_time=date_and_time).first()
        if existing_booking:
            app.logger.error("The requested date and time slot is already booked.")
            return "The requested date and time slot is already booked. Please choose another slot."

        entry = Booki(name=name,email=email, phone= phone, date_and_time=date_and_time ,timestamp= timestamp)
        db.session.add(entry)
        db.session.commit()
        app.logger.info('Booking made successfully.')
        return"Booked successfully"
    app.logger.debug('Returning booking page.')
    return render_template("book.html")



if __name__ == '__main__':
    with app.app_context():

        db.create_all()
        app.run(port=8080)
