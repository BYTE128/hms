from flask import Blueprint, render_template, request, jsonify
from application import myDb

########### User Story 8 Hospital Management System ###########
###################### Add new tests ########################

bp = Blueprint('manageDiagnostics', __name__, template_folder="templates", static_folder="static")

#Render Base File
@bp.route('/manageDiagnostics')
def manageDiagnostics():
    return render_template('addTest.html')

#Fetch Patient Details alongwith Tests Done
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
    myCursor.execute("select diagnosticsmaster.test_name, diagnosticsmaster.rate from diagnosticstable JOIN diagnosticsmaster on diagnosticstable.ws_test_id = diagnosticsmaster.test_id where diagnosticstable.ws_pat_id = %s order by diagnosticsmaster.test_name" % (patientId))
    myResult.extend(myCursor.fetchall())
    myCursor.close()
    return jsonify(myResult)

# Add Tests
@bp.route('/addTests', methods = ['POST'])
def addTests():
    req = request.get_json(force=True)
    print(req)
    patientIDDict = req.pop(0)
    for i in req:
        myCursor = myDb.cursor()
        myCursor.execute("select test_id from diagnosticsmaster where test_name = '%s'" % (i['Test'].upper()))
        myResult = myCursor.fetchall()
        testId = myResult[0][0]
        myCursor.execute("insert into diagnosticstable values({}, {})".format(int(patientIDDict['patientID']), testId))
        myCursor.close()
        myDb.commit()
    return jsonify({"message": "Tests Added Successfully"})

#Fetch All Tests Names
@bp.route('/fetchAllTests', methods = ['POST'])
def fetchAllTests():
    myCursor = myDb.cursor()
    myCursor.execute("select test_name from diagnosticsmaster")
    myResult = myCursor.fetchall()
    return jsonify(myResult)

#Fetch Quantity Available
@bp.route('/showRate', methods = ['POST'])
def showRate():
    req = request.get_json(force=True)
    print(req)
    myCursor = myDb.cursor()
    myCursor.execute("select rate from diagnosticsmaster where test_name = '%s'" % (req['test']))
    myResult = myCursor.fetchall()
    return jsonify(myResult)