import os
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import AddToolForm, LoginForm, RegisterForm, AddCalibrationForm
import csv
import datetime


app = Flask(__name__)
csrf = CSRFProtect(app)
bootstrap = Bootstrap5(app)


db = SQLAlchemy()
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tools.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
csrf.init_app(app)

# 'tools' and 'users' database structure


class Tools(db.Model):
    __tablename__ = "tools"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255))       # Ezkoz status
    status_date = db.Column(db.String(255))  # Status Datum
    tool_id = db.Column(db.Integer)     # Azonosito
    tool_name = db.Column(db.String(255))  # Megnevezes
    tool_location = db.Column(db.String(255))  # Tarolas helye
    tool_type = db.Column(db.String(255))  # Ezkoz tipusa
    tool_brand = db.Column(db.String(255))  # Gyarto
    tool_serial = db.Column(db.String(255))  # Gyari szam
    tool_accuracy = db.Column(db.String(255))  # Pontossag
    tool_range = db.Column(db.String(255))  # Mereshatar #
    max_deviation = db.Column(db.String(255))  # Megengedett elteres
    notes = db.Column(db.String(255))  # Megjegyzes
    calibs = db.relationship("Calibrations", backref="parent_tool")


class Calibrations(db.Model):
    __tablename__ = "calibrations"
    id = db.Column(db.Integer, primary_key=True)
    # Szerszam azonosito a 'tools' tablabol
    parent_id = db.Column(db.Integer, db.ForeignKey("tools.id"))
    calibration_by = db.Column(db.String)  # Kalibralo szemely neve
    calibration_date = db.Column(db.DateTime)  # Kalibralas idopontja
    next_calibration = db.Column(db.DateTime)  # Kovetkezo kalibralas idopontja
    rating = db.Column(db.String)  # Minosites
    temperature = db.Column(db.Integer)  # Kornyezeti homerseklet
    actual_deviation = db.Column(db.String(255))  # Mert elteres
    etalon = db.Column(db.String(255))  # Vizsgalati etalon azonosito
    KULSO_I_A = db.Column(db.Numeric(precision=4, scale=2))
    KULSO_II_A = db.Column(db.Numeric(precision=4, scale=2))
    KULSO_III_A = db.Column(db.Numeric(precision=4, scale=2))
    KULSO_I_B = db.Column(db.Numeric(precision=4, scale=2))
    KULSO_II_B = db.Column(db.Numeric(precision=4, scale=2))
    KULSO_III_B = db.Column(db.Numeric(precision=4, scale=2))
    BELSO_I_A = db.Column(db.Numeric(precision=4, scale=2))
    BELSO_II_A = db.Column(db.Numeric(precision=4, scale=2))
    BELSO_III_A = db.Column(db.Numeric(precision=4, scale=2))
    BELSO_I_B = db.Column(db.Numeric(precision=4, scale=2))
    BELSO_II_B = db.Column(db.Numeric(precision=4, scale=2))
    BELSO_III_B = db.Column(db.Numeric(precision=4, scale=2))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    htm_id = db.Column(db.Integer)
    registered = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    still_employed = db.Column(db.Boolean, default=True)


# Create the 'tools' and 'users' database
with app.app_context():
    db.create_all()


# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    # return User.query.get(user_id)
    return User.query.filter_by(id=user_id).first()


# INDEX LOGIN PAGE -- REDIRECT TO HOMEPAGE IF LOGGED IN
@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()

    # Debug
    # print(form.validate_on_submit())
    # print(form.errors)

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(
            username=form.username.data).first()
        if not user:
            flash("That username does not exist. Please try again.")
            print("usr")
            return redirect(url_for('index'))

        elif not check_password_hash(user.password, form.password.data):
            flash("Incorrect password. Please try again.")
            print("psw")
            return redirect(url_for('index'))

        else:
            login_user(user)
            user.last_login = datetime.date.today()
            db.session.commit()
            return redirect(url_for('home'))

    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


# TOOL PAGE
@app.route("/home")
@login_required
def home():
    tools = db.session.execute(db.select(Tools).order_by("tool_id")).scalars()
    return render_template('index.html', tools=tools, logged_in=current_user.is_authenticated)


# SELEJTEK LISTAZASA
@app.route("/scraps")
@login_required
def scraps():
    tools = db.session.execute(
        db.select(Tools).filter_by(status="Selejt")).scalars()
    return render_template('index.html', tools=tools, logged_in=current_user.is_authenticated)


# REGISTER USER PAGE
@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = RegisterForm()

    # Debug
    # print(form.validate_on_submit())
    # print(form.errors)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("You've already signed up with that email. Sign in instead.")
            return redirect(url_for('login_page'))

        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=generate_password_hash(
                            form.password.data, "pbkdf2:sha256", 8),
                        registered=datetime.date.today(),
                        last_login=datetime.date.today())
        if new_user:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))

        return redirect(url_for('home'))

    return render_template('register.html', form=form)


# ADD TOOL TO THE DATABASE
@app.route("/add-tool", methods=["POST", "GET"])
@login_required
def add_tool():
    if request.method == "POST":
        new_entry = Tools(status=request.form["status"],
                          status_date=request.form["status_date"],
                          tool_id=request.form["tool_id"],
                          tool_name=request.form["tool_names"],
                          tool_location=request.form["tool_location"],
                          tool_type=request.form["tool_type"],
                          tool_brand=request.form["tool_brand"],
                          tool_serial=request.form["tool_serial"],
                          tool_accuracy=request.form["tool_accuracy"],
                          tool_range=request.form["tool_range"],
                          max_deviation=request.form["max_deviation"],
                          notes=request.form["notes"])
        if new_entry:
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add_tool_page.html', logged_in=current_user.is_authenticated)


# REMOVE SELECTED RECORD FROM THE DATABASE
@app.route("/delete/<int:tool_id>")
@login_required
def remove_record(tool_id):
    record_to_remove = Tools.query.filter_by(id=tool_id).first()
    if record_to_remove:
        db.session.delete(record_to_remove)
        db.session.commit()
        return redirect(url_for('home'))

# REMOVE SELECTED CELIBRATION FROM DB


@app.route("/delete-calib/<int:tool_id>/<int:cal_id>")
@login_required
def delete_calibration(tool_id, cal_id):
    record_to_remove = Calibrations.query.filter_by(id=cal_id).first()
    if record_to_remove:
        db.session.delete(record_to_remove)
        db.session.commit()
        return redirect(url_for('tool_details', tool_id=tool_id))


# TODO FINISH THE MODIFY TOOL FUNCTION
# MODIFY THE SELECTED TOOLS PROPETIES
@login_required
@app.route("/modify/<int:tool_id>")
def modify_tool(tool_id):
    form = AddToolForm()
    return render_template('modify_tool.html', form=form, logged_in=current_user.is_authenticated)


@app.route("/logout")
def user_logout():
    logout_user()
    return redirect(url_for('index'))


# IMPORT THE DATA FROM THE 'tools_csv' FILE
@app.route("/import")
@login_required
def import_excel():
    with open('excel/tool_csv.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:

            new_entry = Tools(status=row[0],
                              status_date=row[1],
                              tool_id=row[2],
                              tool_name=row[3],
                              tool_location=row[4],
                              tool_type=row[5],
                              tool_brand=row[6],
                              tool_serial=row[7],
                              tool_accuracy=row[8],
                              tool_range=row[9],
                              max_deviation=row[12],
                              notes=row[17])
            db.session.add(new_entry)
            db.session.commit()


# Return all the details about the selected tool
@app.route("/details/<int:tool_id>")
@login_required
def tool_details(tool_id):
    tool_data = Tools.query.filter_by(id=tool_id).first()
    calibrations = Calibrations.query.filter_by(parent_id=tool_data.id).all()
    if tool_data:

        print(type(calibrations))

        return render_template('details.html', tool_data=tool_data, calibrations=calibrations, logged_in=current_user.is_authenticated)


# Add a new calibration to the selected tool
@app.route("/new-calibration/<int:tool_id>", methods=["POST", "GET"])
@login_required
def add_calibration(tool_id):
    form = AddCalibrationForm()
    owner = Tools.query.filter_by(id=tool_id).first()

    # Debug
    # print(form.validate_on_submit())
    # print(form.errors)

    if form.validate_on_submit():
        new_record = Calibrations(parent_tool=owner,
                                  calibration_by=form.calibration_by.data,
                                  calibration_date=form.calibration_date.data,
                                  next_calibration=form.next_calibration.data,
                                  rating=form.rating.data,
                                  actual_deviation=form.actual_deviation.data,
                                  etalon=form.etalon.data,
                                  temperature=form.temperature.data,
                                  KULSO_I_A=form.KULSO_I_A.data,
                                  KULSO_II_A=form.KULSO_II_A.data,
                                  KULSO_III_A=form.KULSO_III_A.data,
                                  KULSO_I_B=form.KULSO_I_B.data,
                                  KULSO_II_B=form.KULSO_II_B.data,
                                  KULSO_III_B=form.KULSO_III_B.data,
                                  BELSO_I_A=form.BELSO_I_A.data,
                                  BELSO_II_A=form.BELSO_II_A.data,
                                  BELSO_III_A=form.BELSO_III_A.data,
                                  BELSO_I_B=form.BELSO_I_B.data,
                                  BELSO_II_B=form.BELSO_II_B.data,
                                  BELSO_III_B=form.BELSO_III_B.data)
        db.session.add(new_record)
        db.session.commit()
        if new_record:
            return redirect(url_for('tool_details', tool_id=owner.id))

    return render_template('calibration.html', form=form, logged_in=current_user.is_authenticated)


# Search for a record based on tool ID
@app.route("/search", methods=["POST", "GET"])
@login_required
def search():
    if request.method == "POST":
        result = Tools.query.filter_by(tool_id=request.form["search"])

        return render_template('search_results.html', results=result, logged_in=current_user.is_authenticated)


# Filter records based on tool names
@app.route("/filter-by", methods=["POST", "GET"])
@login_required
def filter_by():
    if request.method == "POST":
        result = Tools.query.filter_by(tool_name=request.form["tool_names"])

        return render_template('search_results.html', results=result, logged_in=current_user.is_authenticated)


# Error handling
@app.errorhandler(401)
def unauthorised(e):
    return render_template("401.html"), 401


if __name__ == "__main__":
    app.run(debug=True)
