// Scripts used in config home page

// Control the button accessibility in config home
const checkConfigAccess = function() {
  let dataSnap = document.getElementById('ord-snap-data');
  if (!dataSnap) {
    return;
  }

  // Buttons
  let scBtn = document.getElementById('ord-sc-btn');
  let bpBtn = document.getElementById('ord-bp-btn');
  let esBtn = document.getElementById('ord-es-btn');

  if (!isOrderEditable()) {
    scBtn.disabled = true;
    scBtn.classList.add('penta-btn-dis');
  }
  if (dataSnap.getAttribute('data-ns') === '0' || !isOrderEditable()) {
    bpBtn.disabled = true;
    bpBtn.classList.add('penta-btn-dis');
  }
  if (dataSnap.getAttribute('data-np') === '0' || !isOrderEditable()) {
    esBtn.disabled = true;
    esBtn.classList.add('penta-btn-dis');
  }
};

// Navigate to site config page
const navToSiteConfig = function() {
  if (isOrderEditable()) {
    window.location.href = '/order/config-site/';
  }
};

// Navigate to build products page
const navToBuildPr = function() {
  if (isOrderEditable()) {
    window.location.href = '/order/build-pr/';
  }
};

// Navigate to service config page
const navToSvcConfig = function() {
  if (isOrderEditable()) {
    window.location.href = '/order/edit-svc/';
  }
}

// Runtime
checkConfigAccess();
