// All validation utilities

// Generic validation error messages
const VE_REQUIRED = 'Field is required';
const VE_EMAIL = 'Invalid email format';
const VE_PHONE = 'Invalid phone number';
const VE_USERNAME = 'Username is too short or invalid';
const VE_PSWEAK = 'Password is too weak';
const VE_PSCONFIRM = 'Passwords do not match';
const VE_NOFILE = 'No file selected';
const VE_PIN = 'Must be between 1000 and 9999';

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
};

// Validate if an input meets length requirement
const isSuffLength = function(input, length) {
  return input.length >= length;
};

// Validate an email address
const isValidEmail = function(input) {
  // Email pattern
  let emlRegex = new RegExp(`^[\\w\\.]+@\\w+\\.[\\w]+$`);

  // Double dots
  let ddRegex = new RegExp(`\\.\\.`);
  if (ddRegex.test(input)) {
    return false;
  }

  return emlRegex.test(input);
};

// Validate a U.S. phone number
const isValidPhone = function(input) {
  // Non-digit
  let ndRegex = new RegExp(`\\D`);

  if (input.length !== 10) {
    return false;
  }
  if (ndRegex.test(input)) {
    return false;
  }

  try {
    input = parseInt(input, 10);
    return true;
  } catch (e) {
    return false;
  }
};

// Validate a PIN number
const isValidPin = function(input) {
  try {
    input = parseInt(input, 10);

    if (input < 1000 || input > 9999) {
      return false;
    }
  } catch (e) {
    return false;
  }

  return true;
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

// Validate basic credentials
const isValidCredentials = function(input) {
  // White spaces
  let spaRegex = new RegExp(`\\s`);

  if (input.length < 6) {
    return false;
  }
  if (spaRegex.test(input)) {
    return false;
  }

  return true;
};
