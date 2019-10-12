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
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
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
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
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

// Validate edit product form
const validateEditPrForm = function(form) {
  let valid = true;
  let submitBtn;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_product_name') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else if (fe.value === fe.getAttribute('data-name')) {
        valid = false;
        removeValidationError(fe.name);
      } else {
        removeValidationError(fe.name);
      }
    }
  }

  disEnaButton(submitBtn, valid);
};

// Validate add spec form
const validateAddSpForm = function(form) {
  let valid = true;
  let submitBtn;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_leaf_name') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else if (fe.value && !isValidSpecCode(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_CTG_SPEC);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_spec_label') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_default_value') {
      let dt = document.getElementById('id_data_type').value;

      if (dt === 'BO' && fe.value && !isValidBoolean(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_INV_BOOL);
        }
      } else if (dt === 'QTY' && fe.value && !isValidQuantity(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_INV_QUAN);
        }
      } else {
        removeValidationError(fe.name);
      }
    }
  }

  disEnaButton(submitBtn, valid);
};

// Validate add feature form
const validateAddFetForm = function(form) {
  let valid = true;
  let submitBtn;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_feature_code') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else if (fe.value && !isValidFetCode(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_CTG_FET);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_feature_name') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_limit') {
      if (fe.value && !isValidQuantity(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_INV_LMT);
        }
      } else {
        removeValidationError(fe.name);
      }
    }
  }

  disEnaButton(submitBtn, valid);
};

// Validate edit feature form
const validateEditFetForm = function(form) {
  let valid = true;
  let submitBtn;

  // Change flags
  nameFlag = false;
  limitFlag = false;
  extFlag = false;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_feature_name') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else {
        removeValidationError(fe.name);
        if (fe.value !== fe.getAttribute('data-name')) {
          nameFlag = true;
        }
      }
    } else if (fe.id === 'id_limit') {
      if (fe.value && !isValidQuantity(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_INV_LMT);
        }
      } else {
        removeValidationError(fe.name);
        if (fe.value && fe.value !== fe.getAttribute('data-value')) {
          limitFlag = true;
        }
      }
    } else if (fe.id === 'id_is_extended') {
      if (fe.value !== fe.getAttribute('data-value')) {
        extFlag = true;
      }
    }
  }

  if (!nameFlag && !limitFlag && !extFlag) {
    valid = false;
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
  } else if (e.target.form.id === 'ctg-edit-pr-form') {
    validateEditPrForm(e.target.form);
  } else if (e.target.form.id === 'ctg-add-spec-form') {
    validateAddSpForm(e.target.form);
  } else if (e.target.form.id === 'ctg-add-fet-form') {
    validateAddFetForm(e.target.form);
  } else if (e.target.form.id === 'ctg-edit-fet-form') {
    validateEditFetForm(e.target.form);
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

// Display extended option
if (document.getElementById('ctg-edit-fet-form')) {
  let extField = document.getElementById('id_is_extended');

  if (extField && extField.getAttribute('data-value') === 'Y') {
    extField.selectedIndex = 1;
  }
};
