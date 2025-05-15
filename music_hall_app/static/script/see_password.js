const campPassword = document.getElementById("password");
const eyes = document.getElementById("togglePass");
const img = document.getElementById('eye');
const btn_confirm = document.getElementById("btn_confirm");
const alert_password = document.getElementById("alert_password");

// confirmar senha
const campPassword_confirm = document.getElementById("password_confirm");
const eyes_confirm = document.getElementById("togglePass_confirm");
const img_confirm = document.getElementById("eye_confirm");

campPassword_confirm.addEventListener("change", function() {
    if(campPassword.value != campPassword_confirm.value) {
        alert_password.innerHTML = "Senhas Diferentes"
        alert_password.classList.remove("display_visibled")
        btn_confirm.setAttribute("disabled", "");
        btn_confirm.classList.remove("bg_cinza_claro", "color_branco");
    } else {
        alert_password.classList.add("display_visibled");
        btn_confirm.removeAttribute("disabled");
        btn_confirm.classList.add("bg_cinza_claro", "color_branco");
    }
})

eyes.addEventListener('click', function () {
    if(campPassword.type == "password") {
        campPassword.type = "text"
        img.src = "../static/icons/eye-open.svg";
    } else {
        campPassword.type = "password";
        img.src = "../static/icons/eye-closed.svg";
    }
});

eyes_confirm.addEventListener('click', function() {
    if(campPassword_confirm.type == "password") {
        campPassword_confirm.type = "text";
        img_confirm.src = "../static/icons/eye-open.svg";
    } else {
        campPassword_confirm.type = 'password';
        img_confirm.src = "../static/icons/eye-closed.svg";
    }
})