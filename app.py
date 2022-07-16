import os
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime


# initializations
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'blog.sqlite')
# mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sougata@localhost/users'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'
db = SQLAlchemy(app)
Migrate(app, db)


# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(
        db.DateTime, default=datetime.now())

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return "<Name %r>" % self.name


# Forms
class NamerForm(FlaskForm):
    name = StringField("What's your name?",
                       validators=[DataRequired(message="Your Name")])
    submit = SubmitField("Submit")


class AddUser(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField('Submit')


# Views
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/name', methods=['GET', 'POST'])
def name():
    form = NamerForm()
    name = None
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")
    return render_template('name.html', form=form, name=name)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = AddUser()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            new_user = User(name=form.name.data,
                            email=form.email.data)
            db.session.add(new_user)
            db.session.commit()
            flash("User added!", 1)
        else:
            flash("User Already Added!", 0)

    our_users = User.query.order_by(User.date_added)

    return render_template("add.html", form=form, our_users=our_users)


# create custom Error pages
# invalid Url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(debug=True)
