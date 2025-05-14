const campPassword = document.getElementById("password");
const eyes = document.getElementById("togglePass");
const img = document.getElementById('eye');

// confirmar senha
const campPassword_confirm = document.getElementById("password_confirm");
const eyes_confirm = document.getElementById("togglePass_confirm");
const img_confirm = document.getElementById("eye_confirm");

eyes.addEventListener('click', function () {
    if(campPassword.type == "password") {
        campPassword.type = "text"
        img.src = "static/icons/eye-open.svg";
    } else {
        campPassword.type = "password";
        img.src = "static/icons/eye-closed.svg";
    }
});

eyes_confirm.addEventListener('click', function() {
    if(campPassword_confirm.type == "password") {
        campPassword_confirm.type = "text";
        img_confirm.src = "static/icons/eye-open.svg";
    } else {
        campPassword_confirm.type = 'password';
        img_confirm.src = "static/icons/eye-closed.svg";
    }
})