// Handles all form related functionalities in core app

// General DOM element references
var allForms = document.querySelectorAll('form');
var allInputFields = document.querySelectorAll('input, select, textarea');
var allButtons = document.querySelectorAll('button');
var allValidationMessages = document.querySelectorAll('.ie-msg');
var psrForm = document.getElementById('psr-form');

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

// Validate register form
const validateRegisterForm = function(form) {
  let valid = true;
  let submitBtn;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_entity_name') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_contact_email' || fe.id === 'id_recovery_email') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else if (fe.value && !isValidEmail(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_EMAIL);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_contact_phone') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else if (fe.value && !isValidPhone(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_PHONE);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_signature_letter') {
      if (!fe.value) {
        displayValidationError(fe.name, VE_NOFILE);
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_username') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else if (fe.value && !isValidCredentials(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_USERNAME);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_password') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else if (fe.value && !isPsStrong(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_PSWEAK);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_confirm_password') {
      let psfe = document.getElementById('id_password');

      if (psfe && psfe.value && isPsStrong(psfe.value)) {
        if (fe.required && !fe.value) {
          valid = false;
          if (fe.touched) {
            displayValidationError(fe.name, VE_REQUIRED);
          }
        } else if (fe.value && fe.value !== psfe.value) {
          valid = false;
          if (fe.touched && fe.dirty) {
            displayValidationError(fe.name, VE_PSCONFIRM);
          }
        } else {
          removeValidationError(fe.name);
        }
      } else {
        valid = false;
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_pin') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else if (fe.value && !isValidPin(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_PIN);
        }
      } else {
        removeValidationError(fe.name);
      }
    }
  }

  disEnaButton(submitBtn, valid);
};

// Validate enrollment form
const validateEnrollForm = function(form) {
  let valid = true;
  let submitBtn;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_customer_name') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_contact_email') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else if (fe.value && !isValidEmail(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_EMAIL);
        }
      } else {
        removeValidationError(fe.name);
      }
    }
  }

  disEnaButton(submitBtn, valid);
};

// Validate opportunity form
const validateOppoForm = function(form) {
  let valid = true;
  let submitBtn;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_customer') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_deal_limit') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else if (fe.value && !isValidAmount(fe.value, 1, 32)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_BAD_DEAL_LIMIT);
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

  if (e.target.form.id === 'login-form') {
    validateLoginForm(e.target.form);
  } else if (e.target.form.id === 'psr-form') {
    validateResetForm(e.target.form);
  } else if (e.target.form.id === 'register-form') {
    validateRegisterForm(e.target.form);
  } else if (e.target.form.id === 'customer-form') {
    validateEnrollForm(e.target.form);
  } else if (e.target.form.id === 'oppo-form') {
    validateOppoForm(e.target.form);
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

// Clear all validation related data when form resets
allButtons.forEach((button) => {
  if (button.type === 'reset') {
    button.addEventListener('click', (e) => {
      let targetForm = e.target.form;

      for (let i = 0; i < targetForm.length; ++i) {
        let element = targetForm[i];

        if (element.type === 'submit') {
          element.disabled = true;
          element.classList.add('form-btn-dis');
        }
        if (!element.id.startsWith('id_')) {
          continue;
        }
        if (element.tagName === 'INPUT' || element.tagName === 'SELECT' || element.tagName === 'TEXTAREA') {
          element.touched = false;
          element.dirty = false;
          removeValidationError(element.name);
        }
      }
    })
  }
});

// Disable password reset
psrForm.addEventListener('submit', (e) => {
  e.preventDefault();
  showSnackMessage('Not available');
});
