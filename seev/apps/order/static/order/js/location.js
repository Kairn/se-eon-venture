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
    toggleSiteBtn(true);
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

    // Fill address form
    if (place.address_components) {
      let comps = getAddrComps(place.address_components);

      let addr1 = document.getElementsByName('address_line_1')[0];
      let city = document.getElementsByName('address_city')[0];
      let state = document.getElementsByName('address_state')[0];
      let zip = document.getElementsByName('address_postal')[0];
      let country = document.getElementsByName('address_country')[0];

      addr1.value = `${comps['street_number']} ${comps['route']}`;
      city.value = comps['neighborhood'] ? comps['locality'] ? `${comps['neighborhood']}, ${comps['locality']}` : comps['neighborhood'] : comps['locality'];
      state.value = comps['administrative_area_level_1'];
      zip.value = comps['postal_code'];
      country.value = comps['country'];

      // Enable submit button
      toggleSiteBtn(false);
    }
  });
};

// Populate address components
const getAddrComps = function(data) {
  if (!data) {
    return null;
  }

  let comps = {};

  for (let comp of data) {
    comps[comp.types[0]] = comp.long_name;
  }

  return comps;
};

// Toggle site submit button
const toggleSiteBtn = function(disable) {
  let siteBtn = document.getElementById('ord-add-site-btn');
  if (!siteBtn) {
    return;
  }

  if (disable) {
    siteBtn.disabled = true;
    siteBtn.classList.add('form-btn-dis');
  } else {
    siteBtn.disabled = false;
    siteBtn.classList.remove('form-btn-dis');
  }
};
