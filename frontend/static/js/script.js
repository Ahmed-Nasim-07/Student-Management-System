/* =================================
   STUDENT PAGE
================================= */

function addStudent(){

let name = document.getElementById("name").value.trim();
let age = document.getElementById("age").value;
let phone = document.getElementById("phone").value.trim();
let deptID = document.getElementById("deptID").value;
let studentID = document.getElementById("studentID").value.trim();

if(studentID === "" || name === "" || age === "" || phone === "" || deptID === ""){
    alert("Please fill all required student fields");
    return;
}

if(age <= 0 || age > 120){
    alert("Age must be between 1 and 120");
    return;
}

if(phone.length < 10){
    alert("Phone number must be at least 10 digits");
    return;
}

alert("Student added successfully");

}



/* =================================
   COURSE PAGE
================================= */

function addCourse(){

let courseName = document.getElementById("courseName").value.trim();
let courseID = document.getElementById("courseID").value.trim();
let deptID = document.getElementById("deptID").value;

if(courseName === "" || courseID === "" || deptID === ""){
    alert("Please fill all required course fields");
    return;
}

alert("Course added successfully");

}



/* =================================
   MARKS PAGE
================================= */

function addMarks(){

let studentID = document.getElementById("studentID").value.trim();
let courseID = document.getElementById("courseID").value.trim();
let marks = document.getElementById("marks").value;

if(studentID === "" || courseID === "" || marks === ""){
    alert("Please fill all required marks fields");
    return;
}

marks = Number(marks);

if(isNaN(marks)){
    alert("Marks must be a number");
    return;
}

if(marks < 0 || marks > 100){
    alert("Marks must be between 0 and 100");
    return;
}

alert("Marks added successfully");

}



/* =================================
   ATTENDANCE PAGE
================================= */

function addAttendance(){

let studentID = document.getElementById("studentID").value.trim();
let courseID = document.getElementById("courseID").value.trim();
let attendance = document.getElementById("attendance").value;

if(studentID === "" || courseID === "" || attendance === ""){
    alert("Please fill all required attendance fields");
    return;
}

attendance = Number(attendance);

if(isNaN(attendance)){
    alert("Attendance must be a number");
    return;
}

if(attendance < 0 || attendance > 100){
    alert("Attendance must be between 0 and 100%");
    return;
}

alert("Attendance recorded successfully");

}



/* =================================
   SEARCH PAGE
================================= */

function searchStudents(){

let name = document.getElementById("name").value.toLowerCase().trim();
let studentID = document.getElementById("studentID").value.trim();
let deptName = document.getElementById("deptName").value.toLowerCase().trim();
let deptID = document.getElementById("deptID").value.trim();
let marks = document.getElementById("marks").value;
let attendance = document.getElementById("attendance").value;

let table = document.getElementById("resultTable");

if(!table) return;

let rows = table.getElementsByTagName("tr");

for(let i = 1; i < rows.length; i++){

    let cols = rows[i].getElementsByTagName("td");

    let id = cols[0].innerText;
    let studentName = cols[1].innerText.toLowerCase();
    let department = cols[2].innerText.toLowerCase();
    let studentMarks = Number(cols[3].innerText);
    let studentAttendance = Number(cols[4].innerText);

    let show = true;

    if(name && !studentName.includes(name)) show = false;

    if(studentID && id !== studentID) show = false;

    if(deptName && !department.includes(deptName)) show = false;

    if(deptID && deptID !== department) show = false;

    if(marks){
        marks = Number(marks);
        if(studentMarks < marks) show = false;
    }

    if(attendance){
        attendance = Number(attendance);
        if(studentAttendance < attendance) show = false;
    }

    rows[i].style.display = show ? "" : "none";
}

}