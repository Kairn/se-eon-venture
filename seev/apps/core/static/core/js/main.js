// Main script used in core app

console.log('Core app is launching...');

const maxOffsetXAbs = 45;
const maxOffsetYAbs = 30;
const baseCloudSize = 160;

const map = document.getElementsByTagName('body')[0];
const cloudIconList = document.getElementsByClassName('cloud-icon');
const sideIconList = document.getElementsByClassName('side-icon');

const isSmallWindow = function() {
  return window.innerWidth <= 600;
};

const makeTranslate2D = function(offsetX, offsetY) {
  return `translate(${offsetX}px, ${offsetY}px)`;
};

const applyTranslate = function(element, style) {
  element.style.transform = style;
};

let translateUpdate = true;
setInterval(() => {
  translateUpdate = true;
}, 100);

window.onresize = () => {
  if (isSmallWindow()) {
    for (let i = 0; i < cloudIconList.length; ++i) {
      applyTranslate(cloudIconList[i], makeTranslate2D(0, 0));
    }
    for (let i = 0; i < sideIconList.length; ++i) {
      applyTranslate(sideIconList[i], makeTranslate2D(0, 0));
    }
  }
};

map.addEventListener('mousemove', (e) => {
  if (!translateUpdate || isSmallWindow()) {
    return;
  }
  let height = window.innerHeight;
  let width = window.innerWidth;
  let offsetX = Math.min(((e.pageX - width / 2) / width) * maxOffsetXAbs, maxOffsetXAbs);
  let offsetY = Math.min(((e.pageY - height / 2) / height) * maxOffsetYAbs, maxOffsetYAbs);

  for (let i = 0; i < cloudIconList.length; ++i) {
    let cloudSize = cloudIconList[i].getBoundingClientRect().bottom - cloudIconList[i].getBoundingClientRect().top;
    let coef = cloudSize / baseCloudSize;
    applyTranslate(cloudIconList[i], makeTranslate2D(offsetX * 0.25 * coef, offsetY * 0.25 * coef));
  }
  for (let i = 0; i < sideIconList.length; ++i) {
    applyTranslate(sideIconList[i], makeTranslate2D(offsetX, offsetY));
  }
  translateUpdate = false;
});
