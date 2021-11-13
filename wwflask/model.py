from flask_sqlalchemy import SQLAlchemy
from . import app

db = SQLAlchemy(app)

user  = 'postgres'
pw   = 'admin'
data = 'test'
host = 'localhost'
port = '5432'

#app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{pw}@{host}:{port}/{data}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config ['SQLALCHEMY_RECORD_QUERIES'] = True


### Creat Model for DB with SQlalshemy ###
class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique = True,nullable= False)
    email = db.Column(db.String(30),unique = True , nullable = False)
    message = db.Column(db.String(50),nullable = False)

    def __init__(self,name,email,message):
        self.name = name
        self.email = email
        self.message = message

    def __repr__(self):
        return f'Post {self.name}'


#### create cv for user ####
class Cv(db.Model):

    __tablename__ = 'cv'
    id = db.Column(db.Integer ,primary_key = True,nullable = False)
    date = db.Column(db.String())
    fullname = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer(),  nullable=False)
    address = db.Column(db.String(30), nullable=False)

    computerskills = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50))
    objective = db.Column(db.String(50), nullable=False)
    #picture = db.Column(db.LargeBinary(500), nullable=False)
    picture = db.Column(db.String() , nullable = False)

    user = db.relationship('User', backref = db.backref('cvv',  lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self,data,fullname,email,phone,address,location,computerskill,objective,picture,user):
        self.date = data
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.address = address
        self.location = location
        self.computerskills = computerskill
        self.objective = objective
        self.picture = picture
        self.user = user


    def __repr__(self):
        return f'Post {self.fullname}'
###### leave comment and execute ########
#db.drop_all()           
#db.create_all()
