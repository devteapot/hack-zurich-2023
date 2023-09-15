<script lang="ts">
	import { onMount } from 'svelte';
	import { Loader } from '@googlemaps/js-api-loader';

	let mapEl: HTMLElement;

	onMount(async () => {
		const loader = new Loader({
			apiKey: 'AIzaSyAHMnz118xRAj130zJXl9S09mlcepfoUfY',
			version: 'weekly'
		});

		const { Map } = await loader.importLibrary('maps');

		new Map(mapEl, {
			center: { lat: -34.606, lng: -58.363 },
			zoom: 8
		});
	});
</script>

<div bind:this={mapEl} class="h-full w-full" />
