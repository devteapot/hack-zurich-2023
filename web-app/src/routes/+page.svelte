<script lang="ts">
	import initMap from '$lib/map/initMap';
	import { onMount } from 'svelte';

	let mapEl: HTMLElement;

	onMount(async () => {
		const map = initMap(mapEl);

		const data = [
			{ lat: -34.606, lng: -58.363 },
			{ lat: -34.605, lng: -58.362 },
			{ lat: -34.604, lng: -58.361 },
			{ lat: -34.603, lng: -58.36 },
			{ lat: -34.602, lng: -58.364 },
			{ lat: -34.601, lng: -58.365 }
		];

		data.forEach((entry) => {
			new google.maps.Marker({
				position: entry,
				map: map
			});
		});
	});
</script>

<div bind:this={mapEl} class="h-full w-full" />
