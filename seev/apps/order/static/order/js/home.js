// Scripts used in config home page

// Control the button accessibility in config home
const checkConfigAccess = function() {
  let dataSnap = document.getElementById('ord-snap-data');
  if (!dataSnap) {
    return;
  }

  // Buttons
  let bpBtn = document.getElementById('ord-bp-btn');
  let esBtn = document.getElementById('ord-es-btn');

  if (dataSnap.getAttribute('data-ns') === '0') {
    bpBtn.disabled = true;
    bpBtn.classList.add('penta-btn-dis');
  }
  if (dataSnap.getAttribute('data-np') === '0') {
    esBtn.disabled = true;
    esBtn.classList.add('penta-btn-dis');
  }
};

// Navigate to site config page
const navToSiteConfig = function() {
  window.location.href = '/order/config-site/';
};

// Runtime
checkConfigAccess();
