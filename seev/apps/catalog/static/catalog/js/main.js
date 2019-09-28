// Main script used in catalog app

console.log('Catalog app is launching...');

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
