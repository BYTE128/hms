from flask import Blueprint,render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from application import myDb

########### User Story 1 Hospital Management System ###########
####################### Website Login #########################

bp = Blueprint('websiteLogin', __name__, template_folder='templates', static_folder='static')

#Login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username != None:
            myCursor = myDb.cursor()
            myCursor.execute("select password,user_type from userstore where username = '{}'".format(username))
            myResult = myCursor.fetchall()
            myCursor.close()
            if myResult != [] and check_password_hash(myResult[0][0], password):
                session['username'] = username.upper()
                session['user_type'] = myResult[0][1]
                return redirect(url_for('main.index'))
        flash("Username doesn't exist or Password incorrect", "danger")

    return render_template("login.html")

#Logout
@bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect(url_for('main.index'))

#Function to add user to database, not to be accessed by user
@bp.route('/<username>/<password>/<user_type>')
def add_user(username, password, user_type):
    myCursor = myDb.cursor()
    myCursor.execute("select username from userstore")
    if username in list(map(lambda x:x[0],myCursor.fetchall())):
        flash("This username already exists. Try another One!", "danger")
        return redirect(url_for('index'))
    myCursor.execute("insert into userstore(username, password, user_type) values('{}', '{}', '{}')".format(username, generate_password_hash(password), user_type))
    myDb.commit()
    myCursor = myDb.cursor()
    flash("User {} created successfully! User can start using this id.".format(username), "success")
    return redirect(url_for('main.index'))