<script>
	import { onMount } from 'svelte';
	import { v4 as uuidv4 } from 'uuid';
	import { Autocomplete } from '@skeletonlabs/skeleton';
	import { RadioGroup, RadioItem } from '@skeletonlabs/skeleton';
	import { TabGroup, Tab } from '@skeletonlabs/skeleton';
	import { makeLocationKey, makeLocationLabel } from '$lib/routeHelpers';
	import RouteList from '../lib/components/RouteList.svelte';

	let map;
	let directionsService;
	let directionsRenderer;

	let mapEl;
	let mapBounds;

	let markerLibrary;

	let options = [];
	let plantLocations = [];

	let routeType = 'Outbound';
	let routeFromLabel = '';
	let routeToLabel = '';
	let routeFromValue = '';
	let routeToValue = '';

	let tabSet = 0;

	const markers = new Map();

	let outboundRoutes = [];
	let inboundRoutes = [];

	let selectedRoute;

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

		directionsService = new google.maps.DirectionsService();
		directionsRenderer = new google.maps.DirectionsRenderer();

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
					map: selectedRoute ? null : map,
					content: new markerLibrary.PinElement({
						scale: 0.75
					}).element
				});

				markers.set(makeLocationKey(l), marker);
			});
	}

	$: {
		options = plantLocations.map((l) => ({
			value: l.code ? makeLocationKey(l) : l.name,
			label: makeLocationLabel(l)
		}));
	}

	$: {
		if (selectedRoute) {
			const { from, to } = selectedRoute;

			const request = {
				origin: { lat: from.lat, lng: from.lng },
				destination: { lat: to.lat, lng: to.lng },
				travelMode: 'DRIVING'
			};

			directionsService.route(request, function (result, status) {
				if (status === 'OK') {
					directionsRenderer.setDirections(result);
					directionsRenderer.setMap(map);
				}
			});
		} else if (directionsRenderer) {
			directionsRenderer.setMap(null);
		}
	}

	$: {
		if (selectedRoute) {
			markers.forEach((v) => v.setMap(null));
		} else {
			markers.forEach((v) => v.setMap(map));
		}
	}
</script>

<div class="h-full w-full relative">
	<div bind:this={mapEl} class="h-full w-full z-0" />
	<div class="absolute top-4 left-4 z-10 bg-primary-backdrop-token p-4 card">
		<TabGroup>
			<Tab bind:group={tabSet} name="tab1" value={0}>Add</Tab>
			<Tab bind:group={tabSet} name="tab2" value={1}>Outbound</Tab>
			<Tab bind:group={tabSet} name="tab3" value={2}>Inbound</Tab>
			<svelte:fragment slot="panel">
				{#if tabSet === 0}
					<div class="flex flex-col">
						<div>
							<input
								class="input"
								type="search"
								name="demo"
								bind:value={routeFromLabel}
								placeholder="Search..."
							/>
							<div class="card w-full max-w-sm max-h-48 p-4 overflow-y-auto" tabindex="-1">
								<Autocomplete
									bind:input={routeFromLabel}
									{options}
									on:selection={(event) => {
										routeFromLabel = event.detail.label;
										routeFromValue = event.detail.value;
									}}
								/>
							</div>
						</div>
						<div>
							<input
								class="input"
								type="search"
								name="demo"
								bind:value={routeToLabel}
								placeholder="Search..."
							/>
							<div class="card w-full max-w-sm max-h-48 p-4 overflow-y-auto" tabindex="-1">
								<Autocomplete
									bind:input={routeToLabel}
									{options}
									on:selection={(event) => {
										routeToLabel = event.detail.label;
										routeToValue = event.detail.value;
									}}
								/>
							</div>
						</div>
						<RadioGroup>
							<RadioItem bind:group={routeType} name="justify" value={'Outbound'}>
								Outbound
							</RadioItem>
							<RadioItem bind:group={routeType} name="justify" value={'Inbound'}>Inbound</RadioItem>
						</RadioGroup>
						<button
							class="btn"
							disabled={!routeFromValue || !routeToValue}
							on:click={() => {
								// TODO: add map and remove find
								const from = plantLocations.find((l) => routeFromValue === makeLocationKey(l));
								const to = plantLocations.find((l) => routeToValue === makeLocationKey(l));
								const id = uuidv4();

								if (routeType === 'Outbound') {
									outboundRoutes.push({ from, to, id });
								} else {
									inboundRoutes.push({ from, to, id });
								}

								routeFromLabel = '';
								routeToLabel = '';
								routeFromValue = '';
								routeToValue = '';
							}}>Add</button
						>
					</div>
				{:else if tabSet === 1}
					<RouteList
						bind:routes={outboundRoutes}
						onSelect={(route) => {
							if (selectedRoute && selectedRoute.id === route.id) {
								selectedRoute = undefined;
							} else {
								selectedRoute = route;
							}
						}}
					/>
				{:else if tabSet === 2}
					<RouteList
						bind:routes={inboundRoutes}
						onSelect={(route) => {
							if (selectedRoute && selectedRoute.id === route.id) {
								selectedRoute = undefined;
							} else {
								selectedRoute = route;
							}
						}}
					/>
				{/if}
			</svelte:fragment>
		</TabGroup>
	</div>
</div>
