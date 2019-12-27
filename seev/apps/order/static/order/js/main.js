// Main script used in order app

console.log('Order app is launching...');

// Static functions
// Clear radio field
const clearRadio = function(radio) {
  let inner = document.getElementById(radio.getAttribute('data-inner'));
  let target = document.getElementById(radio.getAttribute('data-target'));

  inner.classList.add('invisible');
  target.checked = false;
  radio.dirty = false;
};

// Display create order popup
const showCreateOrdPop = function() {
  let overlay = document.querySelector('.black-overlay');
  let popup = document.getElementById('oppo-popup');
  let form = document.getElementById('oppo-pop-form');
  let idData = document.getElementById('oppo-id-row');
  let idField = document.getElementById('id_oppo_id');
  let radio = document.getElementById('oppo-radio');
  let submit = document.getElementById('oppo-create-btn');

  form.reset();
  clearRadio(radio);
  submit.disabled = true;
  submit.classList.add('form-btn-dis');
  idField.value = idData.getAttribute('data-oppo');

  setTimeout(() => {
    overlay.classList.remove('no-show');
    popup.classList.remove('no-show');
  }, 250);
};

// Dismiss create order popup
const dismissOppoPop = function() {
  let overlay = document.querySelector('.black-overlay');
  let popup = document.getElementById('oppo-popup');

  overlay.classList.add('no-show');
  popup.classList.add('no-show');
};

// Display order popup
const showOrderPopup = function(eleId) {
  if (!eleId) {
    return;
  }

  let overlay = document.querySelector('.black-overlay');
  let popup = document.getElementById(eleId);

  if (popup) {
    setTimeout(() => {
      overlay.classList.remove('no-show');
      popup.classList.remove('no-show');
    }, 150);
  }
};

// Dismiss order popup
const dismissOrderPopup = function(eleId) {
  if (!eleId) {
    return;
  }

  let overlay = document.querySelector('.black-overlay');
  let popup = document.getElementById(eleId);

  if (popup) {
    overlay.classList.add('no-show');
    popup.classList.add('no-show');
  }
};

// Exit order and clear session
const exitOrder = function() {
  let form = document.getElementById('exit-ord-form')
  form.submit();
};

// Navigate to order config home
const navToConfigHome = function() {
  window.location.href = '/order/config-home/';
};

// Navigate to order summary
const navToSummary = function() {
  let flagDiv = document.getElementById('ord-is-valid');

  if (flagDiv && flagDiv.innerHTML === 'True') {
    window.location.href = '/order/ord-summ/';
  } else {
    showSnackMessage('Order needs to be validated first', 3000);
  }
};

// Submit dummy form
const submitOrderForm = function(formId) {
  if (!formId) {
    return;
  }

  let form = document.getElementById(formId);
  if (form) {
    form.submit();
  }
};

// Runtime
showOrderPopup('ord-valid-msg');