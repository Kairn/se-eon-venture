// Handle functionalities related to build products page

var allSitePills = document.querySelectorAll('.site-pill.ord-pill');

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

// Runtime
// Apply selected site
if (allSitePills && allSitePills.length > 0) {
  allSitePills.forEach((pill) => {
    if (isSelectedSite(pill)) {
      pill.classList.add('selected');
    }
  })
};
