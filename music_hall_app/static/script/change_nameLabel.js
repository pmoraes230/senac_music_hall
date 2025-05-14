const labelImg = document.getElementById("label_img");
const imgInput = document.getElementById("input_img");

imgInput.addEventListener("change", function() {
    const imgName = imgInput.value.split(/(\\|\/)/g).pop()
    labelImg.innerHTML = imgName
})