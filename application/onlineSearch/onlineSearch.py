from flask import Blueprint, render_template, request
from application import myDb

bp = Blueprint('onlineSearch', __name__, template_folder='templates', static_folder='static')

@bp.route("/search", methods = ['GET','POST'])
def search():
    myresult = []
    c=0
    msg = "Patient ID Does'nt Exists"
    if request.method == 'POST':
        form = request.form
        search_value = request.form['patient_id']
        c = int(search_value)
        myCursor = myDb.cursor()
        myCursor.execute("""SELECT ws_pat_name,ws_age,ws_doj,ws_rtype,ws_adrs,state,city FROM patient where ws_pat_id = %s """  % (c))
        myresult = myCursor.fetchall()
        
    return render_template('search.html',myresult=myresult,c=c)