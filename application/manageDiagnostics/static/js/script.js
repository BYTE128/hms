var patientIDGlobal = ''

var testList = []
let optionHTML = "<option selected>Select Test</option>";

document.querySelector("body").onload = function(){
    fetch(`${window.origin}/manageDiagnostics/fetchAllTests`, {
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
                testList.push(data[i][0]);
                optionHTML += "<option value='" + data[i][0] + "'>" + data[i][0] + "</option>";
            }
            document.querySelector(".testSelect").innerHTML = optionHTML;
        });
    });
}

$(document).ready(function() {
    $("#hideInitially").hide();
});


//Reuqest Patient Details and Tests Conducted
document.querySelector("#requestDetail").addEventListener('submit', fetchPatient);

function fetchPatient(e) {
    e.preventDefault();
    
    //Fetching Patient Details from patient table
    var pid = document.getElementById('patient_id')
    patientIDGlobal = pid.value;
    var entry = {'patientID': patientIDGlobal};
    pid.value = '';
    
    fetch(`${window.origin}/manageDiagnostics/fetchPatientDetails`, {
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
                
                var testTable = document.getElementById('testsTable')
                for(var i=1; i<data.length; i++){
                    var row = testTable.insertRow(-1);
                    for(var j in data[i]){
                        row.insertCell(j).innerHTML = "<span style='font-family: Muli; font-weight: 400'>" + data[i][j] + "</span>";
                    }
                }
                
                $("#hideInitially").show();
                
            }
        });
    });
}

//Add Tests Form
document.querySelector("#addTestsButton").addEventListener('click', addTestsFunc);

function addTestsFunc(e) {
    e.preventDefault();
    var rows = document.querySelectorAll("#addTestsTable tr td select, #addTestsTable tr td input");
    var rowObj = []
    rowObj.push({"patientID": patientIDGlobal});
    for(var i=0; i<rows.length; i+=2){
        if(rows[i].value != '' && rows[i].value != "Select Test"){
            var colObj = {
                "Test": rows[i].value,
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
        fetch(`${window.origin}/manageDiagnostics/addTests`, {
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
    var row = document.querySelector("#addTestsTable").insertRow(-1);
    row.insertCell(0).innerHTML = "<select id='testSelect" + selectCount + "' class='custom-select testSelect'>" + optionHTML + "</select>";
    selectCount++;
    row.insertCell(1).innerHTML = "<input type='text' class='input-group-text text-left rate w-100' disabled>";
    row.querySelector("td select").addEventListener('click', testSelectFunc);
});

document.querySelector("#deleteRow").addEventListener('click', function(e) {
    e.preventDefault();
    var table = document.querySelector("#addTestsTable");
    if(table.rows.length > 1) {
        table.deleteRow(-1);
    }
});

document.querySelector("td select").addEventListener('click', testSelectFunc);

function testSelectFunc(){
    test = this.value;
    var testObj = { "test": test };
    fetch(`${window.origin}/manageDiagnostics/showRate`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(testObj),
        cache: "no-cache",
        headers: new Headers({ 
            "content-type": "application/json"
        })
    }).then(response => {
        response.json().then(data => {
            var parentElementVar = this.parentElement.parentElement;
            parentElementVar.querySelector(".rate").value = data[0][0];
        });
    });
}