// Handles all form related functionalities in order app

// Element references
var allForms = document.querySelectorAll('form');
var allInputFields = document.querySelectorAll('input, select, textarea');
var allButtons = document.querySelectorAll('button');
var allRadios = document.querySelectorAll('.seev-radio-outer');
var allRadioDots = document.querySelectorAll('.seev-radio-inner');

// Check radio button
const checkRadio = function(radio) {
  if (radio.dirty) {
    return;
  }

  let inner = document.getElementById(radio.getAttribute('data-inner'));
  let target = document.getElementById(radio.getAttribute('data-target'));

  inner.classList.remove('invisible');
  target.checked = true;
  radio.dirty = true;

  validateOrdCreateForm(document.getElementById('oppo-pop-form'));
};

// Validate order creation form
const validateOrdCreateForm = function(form) {
  let valid = true;
  let submitBtn;

  for (let i = 0; i < form.length; ++i) {
    let fe = form[i];

    if (fe.type === 'submit') {
      submitBtn = fe;
    } else if (fe.id === 'id_ord_name') {
      if (fe.required && !fe.value) {
        valid = false;
      }
    } else if (fe.id === 'id_ord_secret') {
      if (fe.required && !fe.value) {
        valid = false;
      }
    } else if (fe.id === 'id_ord_agree') {
      if (fe.required && !fe.checked) {
        valid = false;
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

  if (e.target.form.id === 'oppo-pop-form') {
    validateOrdCreateForm(e.target.form);
  } else if (e.target.form.id === '') {
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

// Radio button function
allRadios.forEach((radio) => {
  radio.addEventListener('click', () => {
    checkRadio(radio);
  })
});

// Initially unselect all radio buttons
allRadioDots.forEach((dot) => {
  dot.classList.add('invisible');
});

// Initially disable all submit buttons
allButtons.forEach((button) => {
  if (button.type === 'submit') {
    button.disabled = true;
    button.classList.add('form-btn-dis');
  }
});
