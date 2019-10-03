// All validation utilities

// Generic validation error messages
const VE_REQUIRED = 'Field is required';
const VE_EMAIL = 'Invalid email format';
const VE_PHONE = 'Invalid phone number';
const VE_USERNAME = 'Username is too short or invalid';
const VE_PSWEAK = 'Password is too weak';
const VE_PSCONFIRM = 'Passwords do not match';
const VE_NOFILE = 'Only .txt file is supported';
const VE_PIN = 'Must be between 1000 and 9999';
const VE_BAD_DEAL_LIMIT = 'Must be between 1 and 32';
const VE_CTG_PR = 'Invalid product code format';
const VE_CTG_SPEC = 'Invalid specification code format';
const VE_CTG_FET = 'Invalid feature code format';
const VE_INV_BOOL = 'Invalid boolean value';
const VE_INV_QUAN = 'Invalid quantity value';
const VE_INV_LMT = 'Invalid limit';

// Dynamic error messages
const VE_MIN = min => `Minimum of ${min} characters required`;
const VE_MAX = max => `Maximum length of ${max} characters exceeded`;

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

// Show field error message after validation
const displayValidationError = function(name, errMsg) {
  let errId = `ie_${name}`;
  let me = document.getElementById(errId);
  me.innerText = errMsg;
  me.classList.remove('ie-hide-up');
};

// Remove field error message
const removeValidationError = function(name) {
  let errId = `ie_${name}`;
  let me = document.getElementById(errId);
  me.innerText = '';
  me.classList.add('ie-hide-up');
};

// Validate if an input meets length requirement
const isSuffLength = function(input, length) {
  return input.length >= length;
};

// Validate if an input has exceeded length limit
const isOverLength = function(input, length) {
  return input.length <= length;
};

// Validate an email address
const isValidEmail = function(input) {
  // Email pattern
  let emlRegex = new RegExp(`^[^_\\W][\\w\\.]*@\\w+\\.\\w+$`);

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
  let speRegex = new RegExp(`[\\W_]`);

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

// Validate amount unit
const isValidAmount = function(input, min, max) {
  let amount;

  if (!input || !parseInt(input)) {
    return false;
  } else {
    amount = parseInt(input);
  }

  if (!min || !parseInt(min)) {
    min = Number.NEGATIVE_INFINITY;
  } else {
    min = parseInt(min);
  }

  if (!max || !parseInt(max)) {
    max = Number.POSITIVE_INFINITY;
  } else {
    max = parseInt(max);
  }

  if (amount >= min && amount <= max) {
    return true;
  }

  return false;
};

// Validate product code format
const isValidPrCode = function(input) {
  if (!input) {
    return false;
  }

  let prRegex = new RegExp(`^PR(_[A-Z0-9]+)+$`);

  return prRegex.test(input);
};

// Validate specification code format
const isValidSpecCode = function(input) {
  if (!input) {
    return false;
  }

  let specRegex = new RegExp(`^SP(_[A-Z0-9]+)+$`);

  return specRegex.test(input);
};

const isValidFetCode = function(input) {
  if (!input) {
    return false;
  }

  let fetRegex = new RegExp(`^FET(_[A-Z0-9]+)+$`);

  return fetRegex.test(input);
};

// Validate boolean value
const isValidBoolean = function(value) {
  if ((!value && value !== 0) || parseFloat(value) === NaN) {
    return false;
  }

  if (value.length !== 1) {
    return false;
  }

  value = parseFloat(value);
  if (!Number.isInteger(value)) {
    return false;
  }

  value = parseInt(value);
  if (value === 0 || value === 1) {
    return true;
  } else {
    return false;
  }
}

// Validate quantity value
const isValidQuantity = function(value) {
  let nonDigRegex = new RegExp(`\\D`);

  if ((!value && value !== 0) || parseFloat(value) === NaN) {
    return false;
  }

  if (value.length > 1 && value[0] === '0') {
    return false;
  }

  if (value.includes('_') || nonDigRegex.test(value)) {
    return false;
  }

  value = parseFloat(value);
  if (Number.isInteger(value) && value >= 0) {
    return true;
  } else {
    return false;
  }
}
