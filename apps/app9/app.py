from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres123@localhost/pre-registration'
db = SQLAlchemy(app)

# Create our database model

def send_email(email, height, average_value, count):
    FROM_EMAIL='myemal@gmail.com'
    FROM_PASSWORD='mypassword'
    message="Hey there, your height is <strong> %s</strong>. <br> \
    Average height of <strong>%s</strong> users is <strong>%s</strong>. <br> \
    Thanks!" \
    % (height, count, average_value)
    print("e: ",email)
    print("m: ",message)
    subject="Subject test"
    toList=[email]


    gmail = smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(FROM_EMAIL,FROM_PASSWORD)

    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=','.join(toList)
    msg['From']=FROM_EMAIL

    gmail.send_message(msg)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)

    def __init__(self, email, height):
        self.email = email
        self.height = height

#    def __repr__(self):
#        return '<E-mail %r>' % self.email

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

# Save e-mail to database and send to success page
@app.route('/prereg')
def prereg():
    email_ = None
    height_ = None
    if request.method == 'POST':
        email_ = request.form['email_name']
        print("Email is: ",email_)
        height_ = request.form['height_name']

        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email_).count():
            reg = User(email_, height_)
            db.session.add(reg)
            db.session.commit()
            average_query=db.session.query(func.avg(User.height))
            average_value=round(average_query.scalar(),1)
            count=db.session.query(User.height).count()

            #print(float(average.all()[0]))
            #print(type(average))
            #print(average.value(User.height))
            send_email(email_, height_, average_value, count)
            return render_template('success.html')
    return render_template('index.html', text="Seems like we've got something from that email already!")

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
