from flask import Blueprint, request, flash, render_template, jsonify, make_response
from application import myDb
from random import randint
from datetime import date

bp = Blueprint('managePatientInformation', __name__, template_folder='templates', static_folder='static')
  
myCursor = myDb.cursor()

def function1():
    flash("SSN Id should be of 9 digits!!")

@bp.route('/patientnew',methods=['POST','GET'])
def register():
    myresult2 = []
    patient_validation_ssnid=[]
    patient_ssn_new=''
    myc = 0
    date1 = ''
    patient_doj = ''
    type_room = ['------','General','Semi','Single']
    # updatesw_states = ['Maharashtra','MP', 'TN', 'Haryana','UP','Punjab']
    myCursor.execute("select distinct(district) from city where countrycode = 'IND' order by district")
    updatesw_states = list(map(lambda x: x[0],myCursor.fetchall()))
    updatesw_cities=[]
    udh = type(patient_doj)

    #Initializing date 
    msg = "E"
    p=date.today()
    if request.method == 'POST':
        patient_ssnid = int(request.form.get("ssn"))
        patient_ssn_new = str(patient_ssnid)
        patienti_validation_ssnid=[int(x) for x in patient_ssn_new]
        pid = randint(100000000, 999999999)
        patient_name=request.form["patient_name"]
        patient_adrs = request.form.get("addr")
        pstate = request.form["pstates"]
        pcities = request.form["pcities"]
        patient_age= int(request.form["pat_age"])
        patient_doj = request.form["patient_doj"]
        rtype=request.form["rtype"]
        if len(patient_ssn_new) == 9:
            myCursor.execute(("INSERT INTO patient(ws_ssn,ws_pat_id,ws_pat_name,ws_adrs,ws_age,ws_doj,ws_rtype,city,state) VALUES({},{},'{}','{}',{},'{}','{}','{}','{}')").format(patient_ssnid,pid,patient_name,patient_adrs,patient_age,patient_doj,rtype,pcities,pstate))
            myDb.commit()
        elif len(patient_ssn_new)!=9:
            function1()
    return render_template("newpatient.html",type_room=type_room,updatesw_states=updatesw_states,updatesw_cities=updatesw_cities)

@bp.route('/city/<state>')
def city(state):
    cities = myCursor.execute(("select name from city where countrycode = 'IND' and district = '{}' order by name").format(state))
    cities = list(map(lambda x: x[0], myCursor.fetchall()))
    return jsonify(cities)

@bp.route('/patientupdate',methods=['GET','POST'])
def update():
    myresult3=[]
    c=0
    c1=0
    patient_doj=''
    r_type=''
    pstate=''
    pcities=''
    patient_name=''
    patient_age=0
    pname=''
    update_data=[]
    type_room = ['------','General','Semi','Single']
    update_states = ['Maharashtra','MP', 'TN', 'Haryana','UP','Punjab','Kerala','Jharkand','Telengana','Karnataka','Goa']
    update_cities=['Thakurli','Mumbai','Pune','Indore','Chandigarh','Agra','Mohali','Chennai']
    if request.method == 'POST':
        patient_id = int(request.form.get('patient_id'))
        myCursor.execute("SELECT * FROM patient where ws_pat_id = %s " % (patient_id))
        myresult3=myCursor.fetchall()
        pname = request.form.get("patient_name")
        patient_age=request.form.get("pat_age")
        if patient_age != None:
            patient_age=int(patient_age)
        patient_doj=request.form.get('patient_doj')
        r_type=request.form.get('r_type')
        pstate=request.form.get('states')
        pcities=request.form.get('cities')
        adrs=request.form.get('addr')
        if pname!=None:
            myCursor.execute("SET FOREIGN_KEY_CHECKS=0")
            myCursor.execute("UPDATE patient SET ws_pat_name='%s', ws_age=%s,ws_doj='%s',ws_rtype='%s',ws_adrs='%s',state='%s',city='%s' WHERE  ws_pat_id=%s " %(pname,patient_age,patient_doj,r_type,adrs,pstate,pcities,patient_id))
        myDb.commit()
        myCursor.execute("""SET FOREIGN_KEY_CHECKS=1""")
    return render_template("update.html",myresult3=myresult3,update_states=update_states,update_cities=update_cities,type_room=type_room)

@bp.route('/patientdeletepage', methods=['GET', 'POST'])
def deletePage():
    return render_template("delete.html", m=[])


@bp.route('/patientgetpage', methods=['POST'])
def getPage():
    c=0
    patient_delete=0
    myresult9 = []
    m=[]
    search_value = request.get_json(force=True)
    print(search_value)
    c=int(search_value['patient_id'])
    myCursor.execute("""SELECT ws_pat_id, ws_pat_name, ws_age, ws_doj, ws_rtype, ws_adrs, city, state FROM patient where ws_pat_id = %s """ % (c))
    myresult9 = myCursor.fetchall()
    m = myresult9
    patient_delete = c
    if c==None or len(myresult9)==0:
        return jsonify({"message": "Patient Id doesn't exist"})
    return jsonify(m)

@bp.route("/patientdelete",methods=['POST'])
def delete():
    c=0
    patient_delete=0
    myresult9 = []
    m=[]
    search_value = request.get_json(force=True)
    c=int(search_value['patient_id'])
    print(search_value)
    myCursor.execute("""SELECT * FROM patient where ws_pat_id = %s """ % (c))
    myresult9 = myCursor.fetchall()
    m = myresult9
    patient_delete = c
    if m!=[]:
        myCursor.execute("SET FOREIGN_KEY_CHECKS=0")
        myCursor.execute("""DELETE FROM patient where ws_pat_id=%s """ %(patient_delete))
        myDb.commit()
        myCursor.execute("SET FOREIGN_KEY_CHECKS=1")
        myDb.commit()
        return jsonify({"message": "Patient Record deleted successfully."})
    if c==None or len(myresult9)==0:
        flash("Patient id does not exist", category="danger")
    return make_response(jsonify({"message": "Record not found"}))
    

@bp.route("/patientview")
def view():
    mview=myDb.cursor()
    mview.execute("SELECT * FROM patient")
    view_result = mview.fetchall()
    return render_template("display.html",view_result=view_result)