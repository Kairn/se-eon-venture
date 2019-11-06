// Main script used in order app

console.log('Order app is launching...');

// Clear radio field
const clearRadio = function(radio) {
  let inner = document.getElementById(radio.getAttribute('data-inner'));
  let target = document.getElementById(radio.getAttribute('data-target'));

  inner.classList.add('invisible');
  target.checked = false;
  radio.dirty = false;
}

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

// Display order details popup
const showOrdDetails = function() {
  let overlay = document.querySelector('.black-overlay');
  let popup = document.getElementById('ord-detail-popup');

  setTimeout(() => {
    overlay.classList.remove('no-show');
    popup.classList.remove('no-show');
  }, 150);
}

// Dismiss order details popup
const dismissOrdDetails = function() {
  let overlay = document.querySelector('.black-overlay');
  let popup = document.getElementById('ord-detail-popup');

  overlay.classList.add('no-show');
  popup.classList.add('no-show');
}
