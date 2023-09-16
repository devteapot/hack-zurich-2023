/* eslint-disable no-undef */
const initMap = (mapEl) => {
	return new google.maps.Map(mapEl, {
		center: { lat: -34.606, lng: -58.363 },
		zoom: 8
	});
};

export default initMap;
