// Handles all form related functionalities
var allInputFields = document.querySelectorAll('input');

allInputFields.forEach((field) => {
  field.addEventListener('blur', (e) => {
    e.target.touched = true;
  })
});

const validateLoginForm = function() {
  //
}

const validateResetForm = function() {
  //
}
