// Main script used in order app

console.log('Order app is launching...');

// Display create order popup
const showCreateOrdPop = function() {
  let overlay = document.querySelector('.black-overlay');
  let popup = document.getElementById('oppo-popup');
  let form = document.getElementById('oppo-pop-form');
  let idData = document.getElementById('oppo-id-row');
  let idField = document.getElementById('id_oppo_id');

  form.reset();
  idField.value = idData.getAttribute('data-oppo');

  overlay.classList.remove('no-show');
  popup.classList.remove('no-show');
}

// Dismiss create order popup
const dismissOppoPop = function() {
  let overlay = document.querySelector('.black-overlay');
  let popup = document.getElementById('oppo-popup');

  overlay.classList.add('no-show');
  popup.classList.add('no-show');
};
