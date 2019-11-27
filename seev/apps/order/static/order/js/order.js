// Handle order related utilities

// Check if the order is editable in session
window.isOrderEditable = function() {
  let osElem = document.getElementById('ord-data-order-status');
  console.log(osElem);

  if (!osElem || osElem.innerHTML === 'FL' || osElem.innerHTML === 'FZ' || osElem.innerHTML === 'EX' || osElem.innerHTML === 'VD') {
    return false;
  }

  return true;
}
