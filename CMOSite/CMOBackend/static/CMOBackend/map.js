var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 1.290270, lng: 103.851959},
    zoom: 15
  });
  addMarker(location, map);
}

function addMarker(location, label) {
  $.ajax({url: "https://maps.googleapis.com/maps/api/geocode/json?address="+location+"&key="+'AIzaSyAxmNbmdGzDgu_sdi7Je0ENXOmDm80P7wU', success: function(result){
    var marker = new google.maps.Marker({
            position: result.results[0].geometry.location,
            map: map,
            label: label
          });
    map.panTo(result.results[0].geometry.location)
    }});
}
