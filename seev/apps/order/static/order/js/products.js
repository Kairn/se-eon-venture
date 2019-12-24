// Handle functionalities related to build products page

var allSitePills = document.querySelectorAll('.site-pill.ord-pill');
var addPrBtn = document.getElementById('ord-add-ctg-btn');
var allCtgPills = document.querySelectorAll('.ord-ctg-item-pill');
var pendingCartData = {};

const isSelectedSite = function(siteEle) {
  if (!siteEle) {
    return false;
  }

  let refEle = document.getElementById('site-selId');
  if (refEle.innerHTML === siteEle.getAttribute('data-id')) {
    return true;
  }

  return false;
};

const navToSite = function(event) {
  let siteEle = event.target;

  if (siteEle.classList.contains('selected')) {
    return;
  } else {
    let sid = siteEle.getAttribute('data-id').replace(/\-/g, '');
    window.location.href = `/order/build-pr/?site_id=${sid}`;
  }
};

const navToConfig = function(svcId) {
  let bid = svcId.replace(/\-/g, '');
  window.location.href = `/order/edit-svc/?svc_id=${bid}`;
};

// Initialize cart
const initCart = function() {
  if (!allCtgPills || !allCtgPills.length || !pendingCartData) {
    return;
  }

  allCtgPills.forEach((ctgItem) => {
    let ctgId = ctgItem.getAttribute('data-id');
    pendingCartData[ctgId] = 0;
  });
};

// Check if cart has item
const cartHasItem = function() {
  if (!pendingCartData) {
    return false;
  }

  for (let i in pendingCartData) {
    let count = pendingCartData[i];

    if (count > 0) {
      return true;
    } else {
      continue;
    }
  }

  return false;
};

// Add/remove an item
const updateCart = function(ctgId, isAdd) {
  if (!pendingCartData || !ctgId) {
    return;
  }

  for (let i in pendingCartData) {
    if (i === ctgId) {
      if (isAdd) {
        ++pendingCartData[i];
      } else if (pendingCartData[i] > 0) {
        --pendingCartData[i];
      }

      updateCountUi(ctgId, pendingCartData[i]);
      break;
    }
  }

  updateAddBtn();
};

// Update item count in template
const updateCountUi = function(ctgId, value) {
  if (!allCtgPills || !allCtgPills.length || !ctgId) {
    return;
  }

  for (let ctgItem of allCtgPills) {
    if (ctgId === ctgItem.getAttribute('data-id')) {
      let countEle = ctgItem.querySelector('.ctg-item-count');
      countEle.innerHTML = value ? value : 0;
      break;
    }
  }
};

// Update add button
const updateAddBtn = function() {
  if (!addPrBtn) {
    return;
  }

  if (cartHasItem()) {
    addPrBtn.disabled = false;
    addPrBtn.classList.remove('form-btn-dis');
  } else {
    addPrBtn.disabled = true;
    addPrBtn.classList.add('form-btn-dis');
  }
};

// Submit cart to back-end
const submitCart = function() {
  let data = {};

  if (!pendingCartData) {
    return;
  } else {
    Object.assign(data, pendingCartData);
  }

  // Delete empty items
  for (let i in data) {
    if (data[i] < 1) {
      delete data[i];
    }
  }

  let form = document.getElementById('ord-add-ctg-form');
  let dataField = document.getElementById('ctg-add-data');

  dataField.value = JSON.stringify(data);
  form.submit();
};

// Delete existing product
const delBasketItem = function(bid) {
  if (!bid) {
    return;
  }

  let form = document.getElementById('ord-rm-pr-form');
  let bidField = document.getElementById('bi-rm-id');

  bidField.value = bid;
  form.submit();
};

// Runtime
// Apply selected site
if (allSitePills && allSitePills.length > 0) {
  allSitePills.forEach((pill) => {
    if (isSelectedSite(pill)) {
      pill.classList.add('selected');
    }
  });
};

// Load cart
initCart();
updateAddBtn();
