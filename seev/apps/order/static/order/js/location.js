// Controls the site configuration with google maps API integration

console.log('site loading');

// Initialize the map
window.initGoogleSearchMap = function() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: { lat: 40.762656, lng: -73.973826 },
    zoom: 10,
    mapTypeId: 'roadmap'
  });
};
