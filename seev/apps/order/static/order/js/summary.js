// Handles all summary and quoting related functionalities

const PY_TRUE = 'True';
const PY_FALSE = 'False';
const PY_NULL = 'None'

const dotBox = document.getElementById('wait-dots');
const allDots = document.querySelectorAll('.wait-dot');
var dotCount = 1;

// Go to svc config
const navToSvcConfig = function(svcId) {
  if (!isOrderEditable()) {
    return;
  }

  svcId = svcId.replace(/\-/g, '');
  window.location.href = `/order/edit-svc/?svc_id=${svcId}`;
};

// Price a site
const getSitePricing = function(siteId) {
  if (!isOrderEditable()) {
    return;
  }

  showWaitPopup();

  let form = document.getElementById('ord-price-form');
  let field = document.getElementById('id_price_site_array');

  field.value = siteId.replace(/\-/g, '');
  softSubmit(form);
};

// Price all sites (if not priced)
const priceAllSites = function() {
  if (!isOrderEditable()) {
    showSnackMessage('Locked', 1000);
    return;
  }

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
    showWaitPopup();

    field.value = siteIds.join(',');
    softSubmit(form);
  } else {
    showSnackMessage('No site needs pricing', 2500);
  }
};

// Populate spec price
const loadSpecPrice = function(specEle) {
  let mrcField = specEle.querySelector('.mrc.pl-spec');
  let nrcField = specEle.querySelector('.nrc.pl-spec');
  let spMrc = parseFloat(mrcField.getAttribute('data-price'));
  let spNrc = parseFloat(nrcField.getAttribute('data-price'));

  if (!spMrc) {
    spMrc = 0;
  }

  if (!spNrc) {
    spNrc = 0;
  }

  mrcField.innerHTML = `${spMrc.toFixed(0)}`;
  nrcField.innerHTML = `${spNrc.toFixed(0)}`;

  return [spMrc, spNrc];
};

// Populate feature price
const loadFetPrice = function(fetEle) {
  let fetMrc = 0;
  let fetNrc = 0;
  let mrcField = fetEle.querySelector('.mrc.pl-fet');
  let nrcField = fetEle.querySelector('.nrc.pl-fet');

  // Get aggregate spec prices
  let specs = fetEle.querySelectorAll('.summ-spec.summ-spec-fet');
  for (let i = 0; i < specs.length; ++i) {
    let spec = specs[i];
    let spPrice = loadSpecPrice(spec);
    if (spPrice && spPrice.length == 2) {
      fetMrc += parseFloat(spPrice[0]);
      fetNrc += parseFloat(spPrice[1]);
    }
  }

  mrcField.innerHTML = `${fetMrc.toFixed(2)}`;
  nrcField.innerHTML = `${fetNrc.toFixed(2)}`;

  return [fetMrc, fetNrc];
};

// Populate product price
const loadPrPrice = function(prEle) {
  let prMrc = 0;
  let prNrc = 0;
  let mrcField = prEle.querySelector('.mrc.pl-pr');
  let nrcField = prEle.querySelector('.nrc.pl-pr');

  // Get spec prices
  let specs = prEle.querySelectorAll('.summ-spec.summ-spec-pr');
  for (let i = 0; i < specs.length; ++i) {
    let spec = specs[i];
    let spPrice = loadSpecPrice(spec);
    if (spPrice && spPrice.length == 2) {
      prMrc += parseFloat(spPrice[0]);
      prNrc += parseFloat(spPrice[1]);
    }
  }

  // Get feature prices
  let features = prEle.querySelectorAll('.summ-fet-wrapper');
  for (let i = 0; i < features.length; ++i) {
    let feature = features[i];
    let fetPrice = loadFetPrice(feature);
    if (fetPrice && fetPrice.length === 2) {
      prMrc += parseFloat(fetPrice[0]);
      prNrc += parseFloat(fetPrice[1]);
    }
  }

  mrcField.innerHTML = `${prMrc.toFixed(2)}`;
  nrcField.innerHTML = `${prNrc.toFixed(2)}`;

  return [prMrc, prNrc];
};

// Populate site price
const loadSitePrice = function(siteEle) {
  let siteMrc = 0;
  let siteNrc = 0;
  let mrcField = siteEle.querySelector('.mrc.pl-site');
  let nrcField = siteEle.querySelector('.nrc.pl-site');

  // Get aggregate product prices
  let products = siteEle.querySelectorAll('.summ-pr-wrapper');
  for (let i = 0; i < products.length; ++i) {
    let product = products[i];
    let prPrice = loadPrPrice(product);
    if (prPrice && prPrice.length === 2) {
      siteMrc += parseFloat(prPrice[0]);
      siteNrc += parseFloat(prPrice[1]);
    }
  }

  mrcField.innerHTML = `\$${siteMrc.toFixed(2)}`;
  nrcField.innerHTML = `\$${siteNrc.toFixed(2)}`;

  return [siteMrc, siteNrc];
};

// Populate all price
const populatePriceSummary = function() {
  let totalMrc = null;
  let totalNrc = null;
  let mrcField = document.getElementById('ord-summ-tmrc');
  let nrcField = document.getElementById('ord-summ-tnrc');

  // Get aggregate site prices
  let sites = document.querySelectorAll('.summ-loc-wrapper');
  for (let i = 0; i < sites.length; ++i) {
    let site = sites[i];
    if (site.querySelector('.loc-summ').getAttribute('data-flag') === PY_TRUE) {
      if (totalMrc === null) {
        totalMrc = parseFloat('0');
      }
      if (totalNrc === null) {
        totalNrc = parseFloat('0');
      }

      let sitePrice = loadSitePrice(site);
      if (sitePrice && sitePrice.length === 2) {
        totalMrc += parseFloat(sitePrice[0]);
        totalNrc += parseFloat(sitePrice[1]);
      }
    }
  }

  // Get discounts
  let disEle = document.getElementById('ord-data-order-dis');
  let disMrc = parseFloat(disEle.getAttribute('data-mrc')) / 100;
  let disNrc = parseFloat(disEle.getAttribute('data-nrc')) / 100;

  if (totalMrc !== null) {
    mrcField.innerHTML = `\$${(totalMrc * (1 - disMrc)).toFixed(2)}`;
  } else {
    mrcField.innerHTML = `N/A`;
  }

  if (totalNrc !== null) {
    nrcField.innerHTML = `\$${(totalNrc * (1 - disNrc)).toFixed(2)}`;
  } else {
    nrcField.innerHTML = `N/A`;
  }
};

// Toggle wait dot
const toggleWaitDot = function(dotEle, hide) {
  if (dotEle) {
    if (hide) {
      dotEle.classList.add('invisible');
    } else {
      dotEle.classList.remove('invisible');
    }
  }
};

// Looping wait dots
const updateWaitDots = function() {
  let next = dotCount >= 5 ? 1 : dotCount + 1;

  allDots.forEach((dot) => {
    if (parseInt(dot.getAttribute('data-num')) > next) {
      toggleWaitDot(dot, true);
    } else {
      toggleWaitDot(dot, false);
    }
  })

  dotCount = next;
};

// Initialize wait dots
const initWaitDots = function() {
  dotCount = 1;

  allDots.forEach((dot) => {
    if (parseInt(dot.getAttribute('data-num')) > 1) {
      toggleWaitDot(dot, true);
    } else {
      toggleWaitDot(dot, false);
    }
  })
};

// Start waiting popup
const showWaitPopup = function() {
  let overlay = document.querySelector('.black-overlay');
  let popup = document.getElementById('ord-price-wait-popup');

  initWaitDots();

  if (popup) {
    setTimeout(() => {
      overlay.classList.remove('no-show');
      popup.classList.remove('no-show');

      setInterval(() => {
        updateWaitDots();
      }, 1000);
    }, 150);
  }
};

// Runtime
populatePriceSummary();
