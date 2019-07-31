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

// Validate if an input meets length requirement
const isSuffLength = function(input, length) {
  return input.length >= length;
}

// Validate an email address
const isValidEmail = function(input) {
  //
};

// Validate a U.S. phone number
const isValidPhone = function(input) {
  //
};

// Validate a PIN number
const isValidPin = function(input) {
  //
};

// Validate a user password
const isPsStrong = function(input) {
  // Upper case letter
  let upRegex = new RegExp(`[A-Z]`);

  // Lower case letter
  let loRegex = new RegExp(`[a-z]`);

  // Digit
  let digRegex = new RegExp(`\\d`);

  // Special character
  let speRegex = new RegExp(`\\W`);

  // No space character allowed
  let spaRegex = new RegExp(`\\s`);

  input = input.trim();

  if (!isSuffLength(input, 8)) {
    return false;
  }

  if (!upRegex.test(input)) {
    return false;
  }
  if (!loRegex.test(input)) {
    return false;
  }
  if (!digRegex.test(input)) {
    return false;
  }
  if (!speRegex.test(input)) {
    return false;
  }
  if (spaRegex.test(input)) {
    return false;
  }

  return true;
};
