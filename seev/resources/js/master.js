// General runtime script for the entire app

var formPostFlag = false;
var allPostForms = document.querySelectorAll('form');

// Force a form submittion
const forceSubmit = function(form) {
  if (!form) {
    return;
  }

  let e = new Event('submit');
  e.target = form;
  e.force = true;

  form.dispatchEvent(e);
}

// Attempt to submit form (checked)
const softSubmit = function(form) {
  if (!form) {
    return;
  }

  form.dispatchEvent(new Event('submit'));
}

// Prevent user from submitting post forms more than once
allPostForms.forEach((form) => {
  if (form.method !== 'post' || form.id === 'psr-form') {
    return;
  }

  form.addEventListener('submit', (e) => {
    let f = e.target;
    if (!e.force) {
      e.preventDefault();
    } else {
      f.submit();
    }

    // Check flag
    if (!formPostFlag) {
      formPostFlag = true;
      forceSubmit(f);
    }
  })
});
