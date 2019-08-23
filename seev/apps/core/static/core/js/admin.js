// For controlling cpadmin page related functionalities

// Attribute constants
const PE = 'Pending';
const AP = 'Approved';
const DE = 'Denied';
const RV = 'Revoked';

const ACT_AP = 'AP';
const ACT_DE = 'DE';
const ACT_RV = 'RV';
const ACT_RI = 'RI';

const CLIENT_NAME = 'client-name';
const CATALOG_NAME = 'ctg-name';
const COUNTRY = 'country';
const CONTACT_EMAIL = 'contact-email';
const CONTACT_PHONE = 'contact-phone';
const SUMMARY = 'summary';
const STATUS = 'status';
const ALL_DATA_ATTRIBUTES = [
  CLIENT_NAME,
  CATALOG_NAME,
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
const SAVE_BTN = document.getElementById('admin-save-btn');
const CLIENT_CTG = document.getElementById('client-ctg');

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

// Validate approval form
const triggerFormValidation = function(form) {
  let valid = true;
  let cn = null;
  let isAp = false;

  for (let i = 0; i < form.length; ++i) {
    let field = form[i];

    if (field.name === 'ctg_name') {
      cn = field.value;
    }

    if (field.name === 'action') {
      isAp = field.value === ACT_AP ? true : false;

      if (!currentStatus) {
        return false;
      } else if (currentStatus === PE && (field.value === ACT_RV || field.value === ACT_RI)) {
        valid = false;
      } else if (currentStatus === DE) {
        valid = false;
      } else if (currentStatus === RV && field.value !== ACT_RI) {
        valid = false;
      } else if (currentStatus == AP && field.value !== ACT_RV) {
        valid = false;
      }
    }
  }

  if (isAp && !cn) {
    valid = false;
  }

  disEnaButton(SAVE_BTN, valid);
};

var formToggled = false;
var currentStatus = null;

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

      if (ALL_DATA_ATTRIBUTES[j] === CATALOG_NAME) {
        CLIENT_CTG.value = dataCell.innerHTML;
      } else {
        targetCell.innerHTML = dataCell.innerHTML;
      }

      // Set status
      if (ALL_DATA_ATTRIBUTES[j] === STATUS) {
        currentStatus = targetCell.innerHTML;
      }
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

// Disable save button on approval form initially
SAVE_BTN.disabled = true;
SAVE_BTN.classList.add('form-btn-dis');

// Detect approval form change
FORM_SECT.addEventListener('change', (e) => {
  triggerFormValidation(e.target.form);
});
