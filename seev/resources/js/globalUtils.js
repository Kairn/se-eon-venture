// All constants and shared functions used by the application

// All global variables
var snackBarTimer;

// Function to toggle the snack-bar message
const showSnackMessage = function(message, duration) {
  var snackBar = document.getElementById('gsb');
  var sbMsg = document.getElementById('sb-msg');

  if (!message) {
    return;
  }
  if (!duration) {
    duration = 1500;
  }

  sbMsg.innerText = message;
  snackBar.classList.remove('invisible');
  snackBar.classList.add('visible');
  dismissSnackMessage(duration);
};

// Function to dismiss snack-bar message
const dismissSnackMessage = function(delay, force) {
  var snackBar = document.getElementById('gsb');

  if (force && snackBarTimer) {
    clearTimeout(snackBarTimer);
  }
  if (!delay) {
    snackBar.classList.remove('visible');
    snackBar.classList.add('invisible');
  } else {
    snackBarTimer = setTimeout(() => {
      snackBar.classList.remove('visible');
      snackBar.classList.add('invisible');
    }, delay);
  }
};

// Function to replace all substrings with another one in a string
const replaceAllInString = function(source, target, desired) {
  if (!source) {
    return source;
  }

  if (!target) {
    target = '';
  }

  if (!desired) {
    desired = '';
  }

  return source.split(target).join(desired);
};

// Grab snack bar data
const getSnackData = function() {
  let snackEle = document.getElementById('snack-data');
  let text = snackEle.innerText;

  if (text) {
    text = text.trim();
  }

  if (text) {
    return text;
  } else {
    return null;
  }
};

// Onload behavior
window.onload = () => {
  console.log('Running application in DEBUG mode...');
  showSnackMessage(getSnackData(), 2500);
};
