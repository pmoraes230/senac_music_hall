const campPassword = document.getElementById("password");
const eyes = document.getElementById("togglePass");
const img = document.getElementById('eye');

eyes.addEventListener('click', function () {
    if(campPassword.type == "password") {
        campPassword.type = "text"
        img.src = "static/icons/eye-open.svg";
    } else {
        campPassword.type = "password";
        img.src = "static/icons/eye-closed.svg";
    }
})