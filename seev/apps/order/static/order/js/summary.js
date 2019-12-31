// Handles all summary and quoting related functionalities

// Go to svc config
const navToSvcConfig = function(svcId) {
  svcId = svcId.replace(/\-/g, '');
  window.location.href = `/order/edit-svc/?svc_id=${svcId}`;
};

// Price a site
const getSitePricing = function(siteId) {
  // 
};
