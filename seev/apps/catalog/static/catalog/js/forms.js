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

// Validate edit specification form
const validateEditSpForm = function(form) {
  let valid = true;
  let submitBtn;

  // Change flags
  nameFlag = false;
  dvFlag = false;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_spec_label') {
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
    } else if (fe.id === 'id_default_value') {
      let dt = document.getElementById('id_data_type').value;

      if (dt === 'Boolean' && fe.value && !isValidBoolean(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_INV_BOOL);
        }
      } else if (dt === 'Quantity' && fe.value && !isValidQuantity(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_INV_QUAN);
        }
      } else {
        removeValidationError(fe.name);
        if (fe.value && fe.value !== fe.getAttribute('data-value')) {
          dvFlag = true;
        }
      }
    }
  }

  if (!nameFlag && !dvFlag) {
    valid = false;
  }

  disEnaButton(submitBtn, valid);
};

// Validate add value form
const validateAddValForm = function(form) {
  let valid = true;
  let submitBtn;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_code') {
      if (fe.required && !fe.value) {
        valid = false;
        if (fe.touched) {
          displayValidationError(fe.name, VE_REQUIRED);
        }
      } else {
        removeValidationError(fe.name);
      }
    } else if (fe.id === 'id_translation') {
      if (fe.required && !fe.value) {
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

// Validate restriction form
const validateSaveResForm = function(form) {
  let valid = true;
  let submitBtn;

  let chgFlag = false;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.disabled) {
      continue;
    } else if (fe.type === 'text') {
      if (fe.value && (!isValidQuantity(fe.value) || fe.value == '0')) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_INV_RES);
        }
      } else {
        removeValidationError(fe.name);
        if (fe.value && fe.value !== fe.getAttribute('data-value')) {
          chgFlag = true;
        }
        if (!fe.value && fe.getAttribute('data-value')) {
          chgFlag = true;
        }
      }
    } else if (fe.tagName === 'SELECT') {
      if (fe.value !== fe.getAttribute('data-value') && (fe.value === 'Y' || fe.getAttribute('data-value'))) {
        chgFlag = true;
      }
    }
  }

  if (!chgFlag) {
    valid = false;
  }

  disEnaButton(submitBtn, valid);
};

// Validate price form
const validatePriceForm = function(form) {
  let valid = true;
  let submitBtn;

  let chgFlag = false;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.disabled) {
      continue;
    } else if (fe.type === 'text') {
      if (fe.value && !isValidPrice(fe.value)) {
        valid = false;
        if (fe.touched && fe.dirty) {
          displayValidationError(fe.name, VE_INV_PRI);
        }
      } else {
        removeValidationError(fe.name);
        if (fe.value && fe.value !== fe.getAttribute('data-price')) {
          chgFlag = true;
        }
        if (!fe.value && fe.getAttribute('data-value')) {
          chgFlag = true;
        }
      }
    }
  }

  if (!chgFlag) {
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
  } else if (e.target.form.id === 'ctg-edit-spec-form') {
    validateEditSpForm(e.target.form);
  } else if (e.target.form.id === 'ctg-add-value-form') {
    validateAddValForm(e.target.form);
  } else if (e.target.form.id === 'ctg-conf-rule-form') {
    validateSaveResForm(e.target.form);
  } else if (e.target.form.id === 'ctg-conf-pri-form') {
    validatePriceForm(e.target.form);
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

// Display restriction form options
if (document.getElementById('ctg-conf-rule-form')) {
  let aofield = document.getElementById('id_alpha_only');
  let nofield = document.getElementById('id_num_only');
  let eofield = document.getElementById('id_email_only');
  let nnfield = document.getElementById('id_not_null');

  if (aofield && aofield.getAttribute('data-value') === 'Y') {
    aofield.selectedIndex = 1;
  }
  if (nofield && nofield.getAttribute('data-value') === 'Y') {
    nofield.selectedIndex = 1;
  }
  if (eofield && eofield.getAttribute('data-value') === 'Y') {
    eofield.selectedIndex = 1;
  }
  if (nnfield && nnfield.getAttribute('data-value') === 'Y') {
    nnfield.selectedIndex = 1;
  }
};
