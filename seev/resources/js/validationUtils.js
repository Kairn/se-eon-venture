// All validation utilities

// Generic validation error messages
const VE_REQUIRED = 'Field is required';
const VE_EMAIL = 'Invalid email format';
const VE_PHONE = 'Invalid phone number';
const VE_PSWEAK = 'Need at least 6 characters';
const VE_PSCONFIRM = 'Passwords do not match';
const VE_NOFILE = 'File upload is required';

// Disbale or enable a button
const disEnaButton = function(button, valid) {
  if (!button) {
    return;
  }

  if (valid) {
    button.disabled = false;
    button.classList.remove('form-btn-dis');
  } else {
    button.disabled = true;
    button.classList.add('form-btn-dis');
  }
}
