// Main script used in catalog app

console.log('Catalog app is launching...');

// Remove catalog product
const rmProduct = function(productId) {
  let form = document.getElementById('ctg-pr-rm-form');
  let field = document.getElementById('ctg-pr-rm-field');

  field.value = productId;
  form.submit();
};
