from wtforms import Form, PasswordField, BooleanField, StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired, NumberRange
from flask_wtf import FlaskForm
from datetime import date

class RegistrationForm(FlaskForm):
    Username   = StringField(validators=[Length(min=4, max=25),DataRequired()], render_kw={"placeholder": "Username"})
    Email      = StringField(validators=[Length(min=4, max=25),DataRequired(), Email()], render_kw={"placeholder": "Email Address"})
    Password   = PasswordField(validators=[Length(min=4, max=18), DataRequired(), EqualTo("Confirm", message="Passwords must match")], render_kw={"placeholder": "Password"})
    Confirm    = PasswordField(validators=[DataRequired()],render_kw={"placeholder": "Confirm Password"})
    Acceptance = BooleanField("Do you accept our terms of service?",validators=[InputRequired()])
    submit     = SubmitField("Submit")

class LoginForm(FlaskForm):
    Email      = StringField(validators = [Length(min=4, max=25),DataRequired()],render_kw = {"placeholder": "Email Address"})
    Password   = PasswordField(validators = [Length(min=4, max=18),DataRequired()],render_kw = {"placeholder": "Password"})
    submit     = SubmitField("Submit")

class ZooBooking(FlaskForm):
    TimeSlot   = DateField(validators=[InputRequired()], default=date.today, label="What day would you like to visit:")
    Attendees  = IntegerField(validators=[InputRequired(),NumberRange(1,30)],render_kw = {"placeholder": "Attendees"})
    submit     = SubmitField("Submit")

class HotelBooking(FlaskForm):
    StartTime  = DateField(validators=[InputRequired()], default=date.today, label="What day would you like to start your visit:")
    EndTime    = DateField(validators=[InputRequired()], label="What day would you like to end your visit:")
    Attendees  = IntegerField(validators=[InputRequired(),NumberRange(1,6)],render_kw = {"placeholder": "Attendees"})
    submit     = SubmitField("Submit")