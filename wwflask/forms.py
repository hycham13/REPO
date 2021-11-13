from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileRequired
from wtforms import StringField,TextField,TextAreaField,IntegerField,DateField,SubmitField,FileField,SelectField
from wtforms.validators import DataRequired,Email,ValidationError,Length
from datetime import datetime
from wwflask.model import User

class Unique(object):
    def __init__(self, model, field, message=u'This element already exists.'):
        # model = User objecte
        # field = User.name or User.email
        self.model = model
        self.field = field
        self.message = message
    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

### Creat register form ###
class Contact(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Unique(User,User.name),Length(min=3, max=20)])
    email  = TextField('Email Adresse',validators=[DataRequired(),Email(),Unique(User,User.email)])
    message = TextAreaField('Message',validators=[DataRequired(),Length(min=6, max=50)])


###### login form #####
class Validecontact(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = TextField('Email Adresse', validators=[DataRequired(), Email()])

######   register profile cv #####
class CvForm(FlaskForm):
    picture = FileField('Pictures', validators=[FileRequired(),FileAllowed(['jpg', 'png','gif'], 'Images only!')])
    date = DateField('Date',validators=[DataRequired()],render_kw = {'placeholder':'years-month-day'} )
    fullname = StringField('FullName', validators=[DataRequired(), Unique(User, User.name), Length(min=3, max=20)])
    email = TextField('Email Adresse', validators=[DataRequired(), Email(), Unique(User, User.email)])
    phone = IntegerField('PhoneNumber',validators=[DataRequired(),Length(min=10,max=10)])
    address = StringField('Adresse', validators=[DataRequired()]  )
    location = SelectField('Location',validators =[DataRequired()],choices = [('location','select location'),('annaba','Annaba'),('algeria','Algeria')],)
    computerskills = StringField('Computerskills', validators=[DataRequired()],render_kw = {'placeholder':'entry all computer skills such as word,excel, programing language ...........etc'} )
    objective = StringField('Objective', validators=[DataRequired()],render_kw = {'placeholder' : 'entry objective'})
    submit = SubmitField('Submit')