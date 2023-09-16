<script>
	import { onMount } from 'svelte';

	let mapEl;
	let locations;

	onMount(async () => {
		const map = new google.maps.Map(mapEl, {
			center: { lat: -34.606, lng: -58.363 },
			zoom: 8
		});

		const res = await fetch('/api/plants', {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' }
		});
		const data = await res.json();

		data.forEach((entry) => {
			new google.maps.Marker({
				position: { lat: entry.lat, lng: entry.long },
				map: map
			});
		});
	});
</script>

<div bind:this={mapEl} class="h-full w-full" />
