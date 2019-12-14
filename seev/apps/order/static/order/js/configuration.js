// Handle service configuration related functions

var svcDataStruct = [];
var masterSpecs = document.getElementsByClassName('fsp-master');

// Disable or enable feature spec fields
const toggleFeature = function(fetId, disable) {
  if (!fetId) {
    return;
  }

  let fetBlock = document.querySelector(`#id_fet_${fetId}`);
  if (!fetBlock) {
    return;
  }

  let head = fetBlock.querySelector('.ft-head');
  let spFields = fetBlock.querySelectorAll('.fsp-child');

  if (disable) {
    head.classList.add('name-dis');
  } else {
    head.classList.remove('name-dis');
  }

  for (let sp of spFields) {
    if (disable) {
      sp.classList.add('fsp-dis');
      sp.disabled = true;
    } else {
      sp.classList.remove('fsp-dis');
      sp.disabled = false;
    }
  }
};

// Runtime
for (let ms of masterSpecs) {
  ms.addEventListener('change', (event) => {
    let mfi = event.target;
    let fid = mfi.getAttribute('data-master-id');
    if (mfi.value === 'Y') {
      toggleFeature(fid, false);
    } else {
      toggleFeature(fid, true);
    }
  });
};
