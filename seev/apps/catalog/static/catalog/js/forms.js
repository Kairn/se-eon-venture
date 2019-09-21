// Handles all form related functionalities in catalog app

// Element references
var allForms = document.querySelectorAll('form');
var allInputFields = document.querySelectorAll('input, select, textarea');
var allButtons = document.querySelectorAll('button');
var allValidationMessages = document.querySelectorAll('.ie-msg');

// Validate add product form
const validateAddPrForm = function(form) {
  let valid = true;
  let submitBtn;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_product_code') {
      if (fe.required && !fe.value) {
        valid = false;
      } else if (fe.value && !isValidPrCode(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_CTG_PR);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_product_name') {
      if (fe.required && !fe.value) {
        valid = false;
      } else if (fe.value && !isOverLength(fe.value, 128)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_MAX('128'));
        }
      } else {
        removeValidationError(fe.name);
      }
    }
  }

  disEnaButton(submitBtn, valid);
};

// Trigger form validation based on input event
const triggerFormValidation = function(event) {
  let e = event;

  if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'SELECT' && e.target.tagName !== 'TEXTAREA') {
    return;
  }

  if (e.target.form.id === 'ctg-add-pr-form') {
    validateAddPrForm(e.target.form);
  } else if (e.target.form.id === '?') {
    //
  }
};

// Detect form input changes to trigger validation
allInputFields.forEach((field) => {
  field.addEventListener('input', (e) => {
    e.target.dirty = true;
    triggerFormValidation(e);
  })
});

// Detect whether a field has been touched (also validate)
allInputFields.forEach((field) => {
  field.addEventListener('blur', (e) => {
    e.target.touched = true;
    triggerFormValidation(e);
  })
});

// Initially disable all submit buttons
allButtons.forEach((button) => {
  if (button.type === 'submit') {
    button.disabled = true;
    button.classList.add('form-btn-dis');
  }
});

// Initially hide all validation messages
allValidationMessages.forEach((message) => {
  message.classList.add('ie-hide-up');
});
