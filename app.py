from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# initializations
app = Flask(__name__)
app.secret_key = 'secret_key'


# Forms
class NamerForm(FlaskForm):
    name = StringField("What's your name?",
                       validators=[DataRequired(message="Your Name")])
    submit = SubmitField("Submit")


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
    return render_template('name.html', form=form, name=name)


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
