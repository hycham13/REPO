from wwflask import app
from flask import render_template , redirect , url_for , request , flash , session , make_response
from flask_bootstrap import Bootstrap
from model import db , User , Cv
from forms import Contact , CvForm , Validecontact
import os

#### init bootstrap #####
Bootstrap(app)

### configuration app ####
app.config[ 'SECRET_KEY' ] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

#### Configur Session  DataBase ####
db.session.configure(autoflush = False)  ##db.sqlalchemy(app,session_options={"autoflush": False})


@app.route('/')
def index():
    name = request.args.get('s')
    return render_template('index.html' , name = name)


@app.route('/register' , methods = ('GET' , 'POST'))
def register():
    form = Contact()
    if form.validate_on_submit():
        user = User(form.name.data , form.email.data , form.message.data)
        db.session.add(user)
        db.session.commit()
        s = f'{form.name.data}'
        return redirect(url_for('index' , s = s))
    return render_template('register.html' , form = form)


@app.route('/register_profile' , methods = ('GET' , 'POST'))
@app.route('/static')
def register_profile():
    form = CvForm(request.form)
    if request.method == 'POST':
        date = form.date.data
        fullname = form.fullname.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        location = form.location.data
        computerskills = form.computerskills.data
        objective = form.objective.data

        ###### upload picture into static folder #######
        picture = request.files[ 'picture' ]
        picture.save(os.path.join('static' , picture.filename))
        print(picture.filename)

        dic = { 'date': date ,
                'fullname': fullname ,
                'email': email ,
                'phone': phone ,
                'address': address ,
                'location': location ,
                'computerskills': computerskills ,
                'objective': objective ,
                'picture': picture
                }
        valid_user = User.query.filter(User.email == dic.get('email')).first()
        try:
            cv = Cv(date , fullname , email , phone , address , location , computerskills , objective ,
                    str(picture.filename) , user = valid_user)
            valid_user.cvv.append(cv)
            db.session.add(valid_user)
            db.session.commit()
        except:
            db.session.rollback()

        return render_template('home.html')
    return render_template('register_profile.html' , form = form)


@app.route('/profile')
def profile():
    if session[ 'loggin_in' ]:
        cvuser = Cv.query.filter_by(fullname = session[ 'loggin_in' ]).first()
        if cvuser:
            dic = { 'date': str(cvuser.date) ,
                    'fullname': cvuser.fullname ,
                    'email': cvuser.email ,
                    'phone': cvuser.phone ,
                    'address': cvuser.address ,
                    'location': cvuser.location ,
                    'computerskills': cvuser.computerskills ,
                    'objective': cvuser.objective
                    }
            picture = cvuser.picture

            return render_template('profile.html' , dic = dic , picture = picture)
        else:
            pass
    return make_response(" <h1> This Cv  is not exicte </h1>")


@app.route('/home')
def home():
    if not session.get('loggin_in'):
        return render_template('login.html')
    return render_template('home.html')


@app.route('/login' , methods = ('POST' , 'GET'))
def login():
    vform = Validecontact()
    if vform.validate_on_submit():
        fname = vform.name.data
        email = vform.email.data
        existen_user = User.query.filter(User.name == fname and User.email == email).first()
        if existen_user is not None:
            session[ 'loggin_in' ] = fname  # True
            return redirect(url_for('home'))
        else:
            flash('Invalid username or email. Please try again!')
    return render_template('login.html' , form = vform)


@app.route('/logout')
def logout():
    session[ 'loggin_in' ] = False
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug = True)
