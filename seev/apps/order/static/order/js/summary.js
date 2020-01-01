// Handles all summary and quoting related functionalities

const PY_TRUE = 'True';
const PY_FALSE = 'False';
const PY_NULL = 'None'

// Go to svc config
const navToSvcConfig = function(svcId) {
  svcId = svcId.replace(/\-/g, '');
  window.location.href = `/order/edit-svc/?svc_id=${svcId}`;
};

// Price a site
const getSitePricing = function(siteId) {
  let form = document.getElementById('ord-price-form');
  let field = document.getElementById('id_price_site_array');

  field.value = siteId.replace(/\-/g, '');
  form.submit();
};

// Price all sites (if not priced)
const priceAllSites = function() {
  let form = document.getElementById('ord-price-form');
  let field = document.getElementById('id_price_site_array');

  let siteIds = [];
  let locEles = document.querySelectorAll('.loc-summ');
  for (let i = 0; i < locEles.length; ++i) {
    let loc = locEles[i];
    if (loc.getAttribute('data-flag') === PY_FALSE) {
      siteIds.push(loc.getAttribute('data-id').replace(/\-/g, ''));
    }
  }

  if (siteIds && siteIds.length > 0) {
    field.value = siteIds.join(',');
    form.submit();
  } else {
    showSnackMessage('No site needs pricing', 2500);
  }
};
