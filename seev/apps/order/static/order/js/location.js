// Controls the site configuration with google maps API integration

var map;
var autoComplete;
var marker;
var place;
var acControl = document.getElementById('ac-input');

// Initialize the map
window.initGoogleSearchMap = function() {
  // U.S. Boundaries
  const usBounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(49.3457868, -124.7844079),
    new google.maps.LatLng(-66.9513812, 24.7433195)
  );

  // Search options
  var acOptions = {
    bounds: usBounds,
    types: ['address']
  };

  // Center
  const originCenter = { lat: 40.762656, lng: -73.973826 };

  // Initialize maps
  map = new google.maps.Map(document.getElementById('map'), {
    center: originCenter,
    zoom: 10,
    mapTypeId: 'roadmap'
  });

  // Initialize auto-complete and marker
  autoComplete = new google.maps.places.Autocomplete(acControl, acOptions);
  autoComplete.setFields(['address_components', 'geometry', 'name']);
  marker = new google.maps.Marker({
    position: originCenter,
    map: map
  });

  // Auto-complete function
  autoComplete.addListener('place_changed', () => {
    marker.setVisible(false);
    place = autoComplete.getPlace();

    if (!place.geometry) {
      showSnackMessage('Invalid location input', 1500);
      return;
    }

    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(17);
    }

    marker.setPosition(place.geometry.location);
    marker.setVisible(true);
  });
};
