from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email


class AddToolForm(FlaskForm):
    status = SelectField("Ezkoz Status", choices=[
                         "Kalibralt", "Lejart", "Selejt"], validators=[DataRequired()])
    status_date = StringField('Status Datum')
    tool_id = StringField('Azonosito', validators=[DataRequired()])
    tool_name = StringField('Megnevezes', validators=[DataRequired()])
    tool_location = StringField('Tarolas helye', validators=[DataRequired()])
    tool_type = StringField('Ezkoz tipusa', validators=[DataRequired()])
    tool_brand = StringField('Gyarto', validators=[DataRequired()])
    tool_serial = StringField('Gyari szam', validators=[DataRequired()])
    tool_accuracy = StringField('Pontossag', validators=[DataRequired()])
    tool_range = StringField('Mereshatar', validators=[DataRequired()])
    max_deviation = StringField(
        'Megengedett elteres', validators=[DataRequired()])
    notes = StringField('Megjegyzes')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    htm_id = IntegerField("HTM Azonosito", validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddCalibrationForm(FlaskForm):
    parent_tool = StringField("Kalibralt szerszam azonosito")
    calibration_date = DateField(
        "Kalibralas idopontja", validators=[DataRequired()], format='%Y-%m-%d')
    next_calibration = DateField(
        "Kovetkezo kalibracio idopontja", validators=[DataRequired()], format='%Y-%m-%d')
    temperature = IntegerField(
        "Kornyezeti Homerseklet", validators=[DataRequired()])
    calibration_by = StringField(
        "Kalibralast Vegezte", validators=[DataRequired()])
    rating = SelectField("Minosites", choices=[
                         "Megfelel", "Selejt"], validators=[DataRequired()])
    actual_deviation = StringField("Mert elteres", validators=[DataRequired()])
    etalon = StringField("Vizsgalati etalon azonosito",
                         validators=[DataRequired()])
    KULSO_I_A = FloatField("Kulso ertek 1.a", default=0)
    KULSO_II_A = FloatField("Kulso ertek 2.a", default=0)
    KULSO_III_A = FloatField("Kulso ertek 3.a", default=0)
    KULSO_I_B = FloatField("Kulso ertek 1.b", default=0)
    KULSO_II_B = FloatField("Kulso ertek 2.b", default=0)
    KULSO_III_B = FloatField("Kulso ertek 3.b", default=0)
    BELSO_I_A = FloatField("Belso ertek 1.a", default=0)
    BELSO_II_A = FloatField("Belso ertek 2.a", default=0)
    BELSO_III_A = FloatField("Belso ertek 3.a", default=0)
    BELSO_I_B = FloatField("Belso ertek 1.b", default=0)
    BELSO_II_B = FloatField("Belso ertek 2.b", default=0)
    BELSO_III_B = FloatField("Belso ertek 3.b", default=0)
    submit = SubmitField("Submit")
