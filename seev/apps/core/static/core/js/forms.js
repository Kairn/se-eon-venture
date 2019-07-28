// Handles all form related functionalities

// General DOM element references
var allForms = document.querySelectorAll('form');
var allInputFields = document.querySelectorAll('input');
var allButtons = document.querySelectorAll('button');
var allValidationMessages = document.querySelectorAll('.ie-msg');

// Validate login form
const validateLoginForm = function(form) {
  let valid = true;
  let submitBtn;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_username') {
      if (!fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_password') {
      if (!fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else {
        removeValidationError(fe.name);
      }
    }
  }

  disEnaButton(submitBtn, valid);
};

// Validate password reset form
const validateResetForm = function(form) {
  let valid = true;
  let submitBtn;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_email') {
      if (!fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_pin') {
      if (!fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else {
        removeValidationError(fe.name);
      }
    }
  }

  disEnaButton(submitBtn, valid);
};

// Show field error message after validation
const displayValidationError = function(name, errMsg) {
  let errId = `ie_${name}`;
  let me = document.getElementById(errId);
  me.innerText = errMsg;
  me.classList.remove('ie-hide-up');
};

// Remove field error message
const removeValidationError = function(name) {
  let errId = `ie_${name}`;
  let me = document.getElementById(errId);
  me.innerText = '';
  me.classList.add('ie-hide-up');
};

// Trigger form validation based on input event
const triggerFormValidation = function(event) {
  let e = event;

  if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'SELECT' && e.target.tagName !== 'TEXTAREA') {
    return;
  }

  if (e.target.form.id === 'login-form') {
    validateLoginForm(e.target.form);
  } else if (e.target.form.id === 'psr-form') {
    validateResetForm(e.target.form);
  } else if (e.target.form.id === '') {
    //
  }
}

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
