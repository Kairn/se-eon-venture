// Main script used in catalog app

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
  softSubmit(form);
};

// Navigate to specification config page
const goSpecConfig = function(docId) {
  if (!docId) {
    return;
  }

  docId = replaceAllInString(docId, '-', '');
  window.location.href = `/catalog/sp-config/?doc_id=${docId}`;
};

// Navigate to feature config page
const goFetConfig = function(docId) {
  if (!docId) {
    return;
  }

  docId = replaceAllInString(docId, '-', '');
  window.location.href = `/catalog/fet-config/?doc_id=${docId}`;
};

// Remove product specification
const rmPrSpec = function(specificationId) {
  let form = document.getElementById('pr-spec-rm-form');
  let flag = document.getElementById('pr-spec-rm-flag');
  let field = document.getElementById('pr-spec-rm-field');

  flag.value = 'PR';
  field.value = specificationId;
  softSubmit(form);
};

// Remove feature specification
const rmFetSpec = function(specificationId) {
  let form = document.getElementById('fet-spec-rm-form');
  let flag = document.getElementById('fet-spec-rm-flag');
  let field = document.getElementById('fet-spec-rm-field');

  flag.value = 'FET';
  field.value = specificationId;
  softSubmit(form);
};

// Remove catalog feature
const rmFeature = function(featureId) {
  let form = document.getElementById('ctg-fet-rm-form');
  let field = document.getElementById('ctg-fet-rm-field');

  field.value = featureId;
  softSubmit(form);
};

// Remove spec value
const rmSpecVal = function(valueId) {
  let form = document.getElementById('ctg-val-rm-form');
  let field = document.getElementById('ctg-val-rm-field');

  field.value = valueId;
  softSubmit(form);
};

// Populate base spec
const populateBase = function() {
  let form = document.getElementById('ctg-add-spec-form');

  if (form) {
    let codeFi = form.querySelector('#id_leaf_name');
    let labelFi = form.querySelector('#id_spec_label');
    let dtFi = form.querySelector('#id_data_type');
    let dvFi = form.querySelector('#id_default_value');

    codeFi.value = 'SP_BASE';
    labelFi.value = 'Base Spec';
    dtFi.selectedIndex = 0;
    dvFi.value = '1';

    validateAddSpForm(form);
  }
};
