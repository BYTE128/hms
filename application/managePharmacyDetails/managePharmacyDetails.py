from flask import Blueprint, render_template, request, jsonify
from application import myDb

########### User Story 7 Hospital Management System ###########
###################### Issue Medicines ########################

bp = Blueprint('managePharmacyDetails', __name__, template_folder='templates', static_folder='static')

#Render Base File
@bp.route('/managePharmacyDetails')
def managePharmacyDetails():
    return render_template('issueMedicine.html')

#Fetch Patient Details alongwith Medicnes Issued
@bp.route("/fetchPatientDetails", methods = ['POST'])
def fetchPatientDetails():
    myResult = []
    req = request.get_json(force=True)
    patientId = req.get('patientID')
    if patientId != None and patientId != '':
        myCursor = myDb.cursor()
        myCursor.execute("SELECT ws_pat_name,ws_age,ws_doj,ws_rtype,ws_adrs,state,city FROM patient where ws_pat_id = %s" % (int(patientId)))
        myResult = myCursor.fetchall()
        myCursor.close()
        if myResult == []:
            return jsonify({"message": "Patient ID dosesn't exist"})
    else:
        return jsonify({"message": "Please enter full 9 digit Patient ID"})

    myCursor = myDb.cursor()
    myCursor.execute("select medicinesmaster.med_name, medicines.quan_issued, medicinesmaster.rate from medicines JOIN medicinesmaster on medicines.ws_med_id = medicinesmaster.med_id where medicines.ws_pat_id = %s order by medicinesmaster.med_name" % (patientId))
    myResult.extend(myCursor.fetchall())
    myCursor.close()
    return jsonify(myResult)

#Issue Medicines
@bp.route('/issueMedicines', methods = ['POST'])
def issueMedicines():
    req = request.get_json(force=True)
    print(req)
    patientIDDict = req.pop(0)
    for i in req:
        myCursor = myDb.cursor()
        myCursor.execute("select med_id from medicinesmaster where med_name = '%s'" % (i['Medicine'].upper()))
        myResult = myCursor.fetchall()
        medId = myResult[0][0]
        myCursor.execute("update medicinesmaster set quantity = quantity - {} where med_id = {}".format(int(i['Quantity']), medId))
        myCursor.execute("select * from medicines where ws_pat_id = {} and ws_med_id = {}".format(int(patientIDDict['patientID']), medId))
        myResult = myCursor.fetchall()
        if myResult == []:
            myCursor.execute("insert into medicines values({}, {}, {})".format(int(patientIDDict['patientID']), medId, int(i['Quantity'])))
        else:
            myCursor.execute("update medicines set quan_issued = quan_issued + {} where ws_pat_id = {} and ws_med_id = {}".format(int(i['Quantity']), int(patientIDDict['patientID']), medId))
        myCursor.close()
        myDb.commit()
    return jsonify({"message": "Medicines Issued Successfully"})

#Fetch All Medicine Names
@bp.route('/fetchAllMedicines', methods = ['POST'])
def fetchAllMedicines():
    myCursor = myDb.cursor()
    myCursor.execute("select med_name from medicinesmaster")
    myResult = myCursor.fetchall()
    return jsonify(myResult)

#Fetch Quantity Available
@bp.route('/showQuantity', methods = ['POST'])
def showQuantity():
    req = request.get_json(force=True)
    print(req)
    myCursor = myDb.cursor()
    myCursor.execute("select quantity,rate from medicinesmaster where med_name = '%s'" % (req['medicine']))
    myResult = myCursor.fetchall()
    return jsonify(myResult)