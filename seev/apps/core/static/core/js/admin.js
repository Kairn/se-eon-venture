// For controlling cpadmin page related functionalities

// Attribute constants
const CLIENT_NAME = 'client-name';
const CATALOG_NAME = 'ctg_name';
const COUNTRY = 'country';
const CONTACT_EMAIL = 'contact-email';
const CONTACT_PHONE = 'contact-phone';
const SUMMARY = 'summary';
const STATUS = 'status';
const ALL_DATA_ATTRIBUTES = [
  CLIENT_NAME,
  COUNTRY,
  CONTACT_EMAIL,
  CONTACT_PHONE,
  SUMMARY,
  STATUS
];

// Elements
const ALL_CLIENT_TABS = document.getElementsByClassName('client-row-wrapper');
const POPUP = document.getElementById('admin-action-panel');
const OVERLAY = document.getElementById('admin-overlay');
const CLOSE_BTN = document.querySelector(`#admin-action-panel .seev-close`);
const SWITCH_BTN = document.querySelector(`#admin-action-panel .seev-switch`);
const DETAILS_SECT = document.getElementById('client-details');
const FORM_SECT = document.getElementById('approval-form');

// Show popup
const showPopup = function() {
  if (OVERLAY.classList.contains('no-show')) {
    OVERLAY.classList.remove('no-show');
    OVERLAY.classList.add('show');
  }
  if (POPUP.classList.contains('no-show')) {
    POPUP.classList.remove('no-show');
    POPUP.classList.add('show');
  }
};

// Hide popup
const hidePopup = function() {
  if (OVERLAY.classList.contains('show')) {
    OVERLAY.classList.remove('show');
    OVERLAY.classList.add('no-show');
  }
  if (POPUP.classList.contains('show')) {
    POPUP.classList.remove('show');
    POPUP.classList.add('no-show');
  }
};

// Switch popup content
const switchPopup = function() {
  if (formToggled) {
    FORM_SECT.classList.remove('show');
    FORM_SECT.classList.add('no-show');

    DETAILS_SECT.classList.remove('no-show');
    DETAILS_SECT.classList.add('show');
  } else {
    DETAILS_SECT.classList.remove('show');
    DETAILS_SECT.classList.add('no-show');

    FORM_SECT.classList.remove('no-show');
    FORM_SECT.classList.add('show');
  }

  formToggled = !formToggled;
};

var formToggled = false;

// Fill specific client data when clicked
for (let i = 0; i < ALL_CLIENT_TABS.length; ++i) {
  let tab = ALL_CLIENT_TABS[i];

  tab.addEventListener('click', () => {
    // Show details first
    if (formToggled) {
      switchPopup();
    }

    let _cid = tab.getAttribute('data-id');
    let cid = replaceAllInString(_cid, '-', '');

    // Populate data
    for (let j = 0; j < ALL_DATA_ATTRIBUTES.length; ++j) {
      let dataCell = document.querySelector(`#client_${_cid} .${ALL_DATA_ATTRIBUTES[j]}`);
      let targetCell = document.querySelector(`#client-details .${ALL_DATA_ATTRIBUTES[j]}`);
      targetCell.innerHTML = dataCell.innerHTML;
    }

    // Populate form ID
    document.getElementById('id_client_id').value = cid;

    showPopup();
  });
}

// Close popup trigger
CLOSE_BTN.addEventListener('click', () => {
  hidePopup();
});

// Switch popup trigger
SWITCH_BTN.addEventListener('click', () => {
  switchPopup();
});
