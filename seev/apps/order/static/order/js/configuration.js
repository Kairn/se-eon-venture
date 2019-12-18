// Handle service configuration related functions

var masterSpecs = document.getElementsByClassName('fsp-master');
var basketItemId = document.getElementById('id-svc-data').getAttribute('data-id');

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

// Trigger config submission
const submitConfig = function() {
  let svcDataStruct = {};
  let pspList = [];

  svcDataStruct['svcId'] = basketItemId;
  svcDataStruct['pspList'] = pspList;

  // Populate product level specs
  let pspElements = document.getElementsByClassName('psp-child');
  for (let pse of pspElements) {
    pspList.push(buildSpec(pse));
  }

  let fetList = [];
  svcDataStruct['fetList'] = fetList;

  // Populate features
  let fetElements = document.querySelectorAll('.svc-form-line.ft-line');
  for (let fte of fetElements) {
    let fetObj = {};
    let fspList = [];
    fetObj['id'] = getIdInElement(fte);
    fetObj['fspList'] = fspList;

    if (!isfetEnabled(fte)) {
      fetObj['addFlag'] = false;
      fetList.push(fetObj);
      continue;
    } else {
      fetObj['addFlag'] = true;
    }

    // Populate feature specs
    let fspElements = fte.querySelectorAll('.fsp-child');
    for (let fse of fspElements) {
      fspList.push(buildSpec(fse));
    }
    fetList.push(fetObj);
  }

  console.log(svcDataStruct);

  // Submit json form
  let form = document.getElementById('svc-json-form');
  let field = document.getElementById('json-field');
  field.value = JSON.stringify(svcDataStruct);

  console.log(field.value);
  form.submit();
};

// Get ID from tagged element
const getIdInElement = function(ele) {
  if (ele) {
    let rawId = ele.id;
    if (rawId) {
      return rawId.split('_')[2];
    }
  }
};

// Build a spec object
const buildSpec = function(specEle) {
  if (specEle) {
    let specObj = {};
    specObj['id'] = getIdInElement(specEle);
    specObj['value'] = specEle.value;
    return specObj;
  }
};

// Check if a feature needs to be enabled
const isfetEnabled = function(fetEle) {
  if (!fetEle) {
    return false;
  }

  // Check master spec
  let masterSp = fetEle.querySelector('.fsp-master');
  if (masterSp) {
    return masterSp.value === 'Y';
  }

  // Check children
  let subSpecs = fetEle.querySelectorAll('.fsp-child');
  if (subSpecs && subSpecs.length > 0) {
    for (sps of subSpecs) {
      if (sps.value) {
        return true;
      }
    }
  }

  return false;
};

// Runtime
// Turn on feature toggler
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
