from flask import Blueprint, request, render_template
from application import myDb
from datetime import date

bp = Blueprint('patientBilling', __name__, template_folder='templates', static_folder='static')

@bp.route("/billing", methods = ['POST','GET'])
def patientBilling():
    myCursor = myDb.cursor()
    patient_info = []
    myResult = []
    myResult1 = []
    total = []
   
    if request.method == 'POST':
        ws_pat_id = int(request.form.get('ws_pat_id'))
        print(ws_pat_id)

        #patient related info
        myCursor.execute(""" SELECT ws_pat_id, ws_pat_name, ws_adrs, ws_age, ws_doj, ws_rtype FROM patient WHERE ws_pat_id = %s""" %(ws_pat_id))
        patient_info = myCursor.fetchone()
        print(patient_info)
        date1 = patient_info[4]
        f_date = date(int(date1[0:4]), int(date1[5:7]), int(date1[8:]))
        l_date = date.today()
        delta = l_date - f_date
        total_days = delta.days + 1
        total.append(total_days)
        if patient_info[5] == "Semi":
          total_amt = 4000
        elif patient_info[5] == "Single":
          total_amt = 8000
        else :
          total_amt = 2000
        sum_patient = total_days*total_amt
        print(sum_patient)
        total.append(sum_patient)

        #medicine related info
        myCursor = myDb.cursor()
        myCursor.execute("select medicinesmaster.med_name, medicines.quan_issued, medicinesmaster.rate from medicines JOIN medicinesmaster on medicines.ws_med_id = medicinesmaster.med_id where medicines.ws_pat_id = %s order by medicinesmaster.med_name" % (ws_pat_id))
        myResult = myCursor.fetchall()
        myCursor.close()
        print(myResult)
        length=len(myResult)
        sum_medicine = 0
        for x in range(0,length):
          sum1 = myResult[x][1]*myResult[x][2]
          sum_medicine = sum_medicine+sum1 
        print(sum_medicine)
        total.append(sum_medicine)

        #diagnosis related info
        myCursor = myDb.cursor()
        myCursor.execute("select diagnosticsmaster.test_name, diagnosticsmaster.rate from diagnosticstable JOIN diagnosticsmaster on diagnosticstable.ws_test_id = diagnosticsmaster.test_id where diagnosticstable.ws_pat_id = %s order by diagnosticsmaster.test_name" % (ws_pat_id))
        myResult1 = myCursor.fetchall()
        myCursor.close()
        print(myResult1)
        length1=len(myResult1)
        sum_diagnosis = 0
        for x in range(0,length1):
          sum_diagnosis = sum_diagnosis + myResult1[x][1]
        print(sum_diagnosis)
        total.append(sum_diagnosis)
      
        #grand related info
        grand_total = sum_patient+sum_medicine+sum_diagnosis
        total.append(grand_total)

    return render_template('printBill.html',patient_info = patient_info,myResult = myResult,len1 = len(myResult),myResult1 = myResult1,len2=len(myResult1),total = total)
   