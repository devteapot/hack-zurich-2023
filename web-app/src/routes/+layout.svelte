<script>
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';

	let loadingGoogleMaps = true;

	window.loadedGoogleMaps = () => {
		loadingGoogleMaps = false;
	};
</script>

<svelte:head>
	<script
		defer
		async
		src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAHMnz118xRAj130zJXl9S09mlcepfoUfY&libraries=places&callback=loadedGoogleMaps"
	>
	</script>
</svelte:head>

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<strong class="text-xl uppercase">🚛 Truckathon</strong>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	{#if !loadingGoogleMaps}
		<slot />
	{/if}
</AppShell>
