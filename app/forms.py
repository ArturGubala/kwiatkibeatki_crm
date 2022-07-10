from wtforms import Form, StringField, PasswordField, validators, SubmitField
from flask_login import current_user


class LoginForm(Form):
    email = StringField(
        validators=[validators.DataRequired(), validators.InputRequired()])
    password = PasswordField()
    submit = SubmitField("Zaloguj")


class UpdateUserInformationForm(Form):
    name = StringField(
        validators=[validators.DataRequired(), validators.InputRequired()]
    )
    surname = StringField()
    phone_number = StringField()
    email_address = StringField(
        validators=[validators.DataRequired(), validators.InputRequired()])
    submit = SubmitField("Zapisz")
