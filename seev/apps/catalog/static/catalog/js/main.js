// Main script used in catalog app

console.log('Catalog app is launching...');

// Navigate to catalog home
const goCtgHome = function() {
  window.location.href = '/catalog/';
};

// Navigate to product config page
const goPrConfig = function(docId) {
  if (!docId) {
    return;
  }

  docId = replaceAllInString(docId, '-', '');
  window.location.href = `/catalog/pr-config/?doc_id=${docId}`;
};

// Remove catalog product
const rmProduct = function(productId) {
  let form = document.getElementById('ctg-pr-rm-form');
  let field = document.getElementById('ctg-pr-rm-field');

  field.value = productId;
  form.submit();
};

// Navigate to specification config page
const goSpecConfig = function(docId) {
  //
};

// Remove product specification
const rmPrSpec = function(specificationId) {
  let form = document.getElementById('pr-spec-rm-form');
  let flag = document.getElementById('pr-spec-rm-flag');
  let field = document.getElementById('pr-spec-rm-field');

  flag.value = 'PR';
  field.value = specificationId;
  form.submit();
};

// Remove catalog feature
const rmFeature = function(featureId) {
  let form = document.getElementById('ctg-fet-rm-form');
  let field = document.getElementById('ctg-fet-rm-field');

  field.value = featureId;
  form.submit();
};
