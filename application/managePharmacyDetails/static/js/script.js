var patientIDGlobal = ''

var medicineList = []
let optionHTML = "<option selected>Select Medicine</option>";

document.querySelector("body").onload = function(){
    fetch(`${window.origin}/managePharmacyDetails/fetchAllMedicines`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({}),
        cache: "no-cache",
        headers: new Headers({ 
            "content-type": "application/json"
        })
    }).then(response => {
        response.json().then(data => {
            for(var i in data){
                medicineList.push(data[i][0]);
                optionHTML += "<option value='" + data[i][0] + "'>" + data[i][0] + "</option>";
            }
            document.querySelector(".medicineSelect").innerHTML = optionHTML;
        });
    });
}

$(document).ready(function() {
    $("#hideInitially").hide();
});


//Reuqest Patient Details and Medicines Issued
document.querySelector("#requestDetail").addEventListener('submit', fetchPatient);

function fetchPatient(e) {
    e.preventDefault();
    
    //Fetching Patient Details from patient table
    var pid = document.getElementById('patient_id')
    patientIDGlobal = pid.value;
    var entry = {'patientID': patientIDGlobal};
    pid.value = '';
    
    fetch(`${window.origin}/managePharmacyDetails/fetchPatientDetails`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(response => {
        response.json().then(data => {
            if('message' in data){
                toastr.options = {
                    "closeButton": true,
                    "positionClass": "toast-top-full-width",
                    "newestOnTop": true
                }
                toastr.error(data['message']);
            } else {
                var patientTable = ['#patient_name', '#patient_age', '#patient_doj', '#country', '#paddr', '#pstate', '#pcity'];
                for(var i in data[0]){
                    document.querySelector(patientTable[i]).innerHTML = data[0][i];
                }
                
                var medicineTable = document.getElementById('medicineTable')
                for(var i=1; i<data.length; i++){
                    var row = medicineTable.insertRow(-1);
                    for(var j in data[i]){
                        row.insertCell(j).innerHTML = "<span style='font-family: Muli; font-weight: 400'>" + data[i][j] + "</span>";
                    }
                    row.insertCell(-1).innerHTML = "<span style='font-family: Muli; font-weight: 400'>" + data[i][1] * data[i][2] + "</span>";
                }
                
                $("#hideInitially").show();
                
            }
        });
    });
}

//Issue Medicines Form
document.querySelector("#issueMedicinesButton").addEventListener('click', issueMedicinesFunc);

function issueMedicinesFunc(e) {
    e.preventDefault();
    var rows = document.querySelectorAll("#issueMedicineTable tr td select, #issueMedicineTable tr td input");
    var rowObj = []
    rowObj.push({"patientID": patientIDGlobal});
    for(var i=0; i<rows.length; i+=5){
        if(rows[i+2].value != ''){
            var colObj = {
                "Medicine": rows[i].value,
                "Quantity": rows[i+2].value, 
                "Rate": rows[i+3].value
            };
            rowObj.push(colObj);
        } else {
            toastr.options = {
                "closeButton": true,
                "positionClass": "toast-top-full-width",
                "newestOnTop": true
            }
            toastr.error("Some fields are blank, that rows will not reflect.");
        }
    }
    
    if(rowObj.length > 1){
        fetch(`${window.origin}/managePharmacyDetails/issueMedicines`, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(rowObj),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then(response => {
            response.json().then(data => {
                toastr.options = {
                    "closeButton": true,
                    "positionClass": "toast-top-full-width",
                    "newestOnTop": true
                }
                toastr.success(data['message']);
                setTimeout(() => {
                    location.reload();
                    alert("This page will now refresh. Press OK");
                }, 5000);
            });
        });
    }
}

document.querySelector("#addRow").addEventListener('click', function(e) {
    e.preventDefault();
    var selectCount = 2;
    var row = document.querySelector("#issueMedicineTable").insertRow(-1);
    row.insertCell(0).innerHTML = "<select id='medicineSelect" + selectCount + "' class='custom-select medicineSelect'>" + optionHTML + "</select>";
    selectCount++;
    row.insertCell(1).innerHTML = "<input type='text' class='input-group-text text-left quantityAvailable w-100' disabled>";
    row.insertCell(2).innerHTML = "<input type='text' class='input-group-text text-left quantity w-100' placeholder='Enter quantity to issue'>";
    row.insertCell(3).innerHTML = "<input type='text' class='input-group-text text-left rate w-100' disabled>";
    row.insertCell(4).innerHTML = "<input type='text' class='input-group-text text-left amount w-100' disabled>";
    row.querySelector("td select").addEventListener('click', medicineSelectFunc);
});

document.querySelector("#deleteRow").addEventListener('click', function(e) {
    e.preventDefault();
    var table = document.querySelector("#issueMedicineTable");
    if(table.rows.length > 1) {
        table.deleteRow(-1);
    }
});

document.querySelector("td select").addEventListener('click', medicineSelectFunc);

function medicineSelectFunc(){
    medicine = this.value;
    var medicineObj = { "medicine": medicine };
    fetch(`${window.origin}/managePharmacyDetails/showQuantity`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(medicineObj),
        cache: "no-cache",
        headers: new Headers({ 
            "content-type": "application/json"
        })
    }).then(response => {
        response.json().then(data => {
            var parentElementVar = this.parentElement.parentElement;
            parentElementVar.querySelector(".quantityAvailable").value = data[0][0];
            parentElementVar.querySelector(".rate").value = data[0][1];
            parentElementVar.querySelector(".quantity").onchange = function() {
                parentElementVar.querySelector(".amount").value = this.value * data[0][1];
            }
        });
    });
}