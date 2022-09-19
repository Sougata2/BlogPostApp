import os
from flask import Flask, render_template, flash, request
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
# app.config['SQLALCHEMY_DATABASE_URI'] =
# 'mysql+pymysql://root:sougata@localhost/users'


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
    phone = db.Column(db.String(20))
    date_added = db.Column(
        db.DateTime, default=datetime.now())

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

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
    phone = StringField('Phone Number', validators=[DataRequired()])
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
                            email=form.email.data,
                            phone=form.phone.data)

            db.session.add(new_user)
            db.session.commit()
            flash("User added!", 1)
        else:
            flash("User Already Added!", 0)

    our_users = User.query.order_by(User.date_added)

    return render_template("add.html", form=form, our_users=our_users)


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    form = AddUser()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f"{user_to_delete.name} Deleted Successfully", 'delete')
        our_users = User.query.order_by(User.date_added)

    except Exception:
        flash(f"There was  a problem deleteing the {user_to_delete.name}", 0)

    return render_template('delete.html', form=form,
                           user_to_delete=user_to_delete,
                           our_users=our_users)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    our_users = User.query.order_by(User.date_added)
    form = AddUser()
    name_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form.get('name')
        name_to_update.email = request.form.get('email')
        name_to_update.phone = request.form.get('phone')
        try:
            db.session.commit()
            flash("User Updated Successfully!", 1)

        except Exception:
            flash("Error! Looks like there was a problem...try again", 0)

    return render_template('update.html', form=form,
                           name_to_update=name_to_update,
                           our_users=our_users, id=id)


@app.route('/show_users')
def show_users():
    users = User.query.order_by(User.date_added)
    return render_template('show_users.html', users=users)


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
    # use app.run("0.0.0.0") to run over the internet.
