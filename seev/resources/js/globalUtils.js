// All constants and shared functions used by the application

window.onload = () => {
  console.log('Running application in DEBUG mode...');
  showSnackMessage('Testing snack bar', 2500);
}

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
}

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
}
