<script>
	import { onMount } from 'svelte';

	let map;
	let mapEl;
	let mapBounds;
	let markerLibrary;
	let plantLocations = [];

	const markers = new Map();

	onMount(async () => {
		map = new google.maps.Map(mapEl, {
			center: { lat: -34.606, lng: -58.363 },
			mapId: 'cd7f658b49dc952f',
			zoom: 8,
			zoomControl: true,
			mapTypeControl: false,
			streetViewControl: false,
			rotateControl: false,
			scaleControl: false,
			fullscreenControl: false
		});

		google.maps.event.addListener(map, 'idle', function () {
			const bounds = map.getBounds();

			const ne = bounds.getNorthEast();
			const sw = bounds.getSouthWest();

			mapBounds = {
				ne: { lat: ne.lat(), lng: ne.lng() },
				sw: { lat: sw.lat(), lng: sw.lng() }
			};
		});

		markerLibrary = await google.maps.importLibrary('marker');
	});

	$: {
		if (mapBounds) {
			fetch('/api/plants', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ mapBounds })
			}).then((res) => {
				res.json().then((data) => {
					plantLocations = data;
				});
			});
		}
	}

	const makeLocationKey = (loc) => `${loc.code}$${loc.lat}$${loc.lng}`;

	$: {
		const newKeys = new Set(plantLocations.map(makeLocationKey));

		[...markers.keys()]
			.filter((k) => !newKeys.has(k))
			.forEach((k) => {
				const marker = markers.get(k);
				marker.setMap(null);
				markers.delete(k);
			});

		plantLocations
			.filter((l) => !markers.has(makeLocationKey(l)))
			.forEach((l) => {
				const marker = new markerLibrary.AdvancedMarkerElement({
					position: { lat: l.lat, lng: l.lng },
					map: map,
					content: new markerLibrary.PinElement({
						scale: 0.75
					}).element
				});

				markers.set(makeLocationKey(l), marker);
			});
	}
</script>

<div class="h-full w-full relative">
	<div bind:this={mapEl} class="h-full w-full z-0" />
	<div class="absolute top-4 left-4 z-10 bg-primary-900">FLOATING SHIT</div>
</div>
