from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email


class AddToolForm(FlaskForm):
    status = StringField('Ezkoz status', validators=[DataRequired()])
    status_date = StringField('Status Datum')
    tool_id = StringField('Azonosito', validators=[DataRequired()]) 
    tool_name = StringField('Megnevezes', validators=[DataRequired()]) 
    tool_location = StringField('Tarolas helye', validators=[DataRequired()])
    tool_type = StringField('Ezkoz tipusa', validators=[DataRequired()]) 
    tool_brand = StringField('Gyarto', validators=[DataRequired()]) 
    tool_serial = StringField('Gyari szam', validators=[DataRequired()]) 
    tool_accuracy = StringField('Pontossag', validators=[DataRequired()])  
    tool_range = StringField('Mereshatar', validators=[DataRequired()])  
    max_deviation = StringField('Megengedett elteres', validators=[DataRequired()]) 
    notes = StringField('Megjegyzes')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    

class AddCalibrationForm(FlaskForm):
    parent_tool = StringField("Kalibralt szerszam azonosito")
    calibration_date = DateField("Kalibralas idopontja", validators=[DataRequired()])
    next_calibration = DateField("Kovetkezo kalibracio idopontja", validators=[DataRequired()])
    temperature = IntegerField("Kornyezeti Homerseklet", validators=[DataRequired()])
    calibration_by = StringField("Kalibralast Vegezte", validators=[DataRequired()])
    rating = StringField("Minosites", validators=[DataRequired()])
    actual_deviation = StringField("Mert elteres", validators=[DataRequired()])
    etalon = StringField("Vizsgalati etalon azonosito", validators=[DataRequired()])
    KULSO_I_A = FloatField("Kulso ertek 1.a")
    KULSO_II_A = FloatField("Kulso ertek 2.a") 
    KULSO_III_A = FloatField("Kulso ertek 3.a") 
    KULSO_I_B = FloatField("Kulso ertek 1.b") 
    KULSO_II_B = FloatField("Kulso ertek 2.b")
    KULSO_III_B = FloatField("Kulso ertek 3.b")
    BELSO_I_A = FloatField("Belso ertek 1.a")
    BELSO_II_A = FloatField("Belso ertek 2.a")
    BELSO_III_A = FloatField("Belso ertek 3.a")
    BELSO_I_B = FloatField("Belso ertek 1.b")
    BELSO_II_B = FloatField("Belso ertek 2.b")
    BELSO_III_B = FloatField("Belso ertek 3.b")
    submit = SubmitField("Submit")
