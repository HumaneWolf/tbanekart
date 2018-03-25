const mapsApiKey = '';
const apiBase = '/';

var gmaps = document.createElement('script');
gmaps.src = 'https://maps.googleapis.com/maps/api/js?key=' + mapsApiKey + '&callback=initMap';
document.head.appendChild(gmaps);
