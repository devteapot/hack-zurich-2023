<script>
	import { makeLocationLabel } from '$lib/routeHelpers';

	export let routes;
	export let onSelect;
</script>

{#if routes.length === 0}
	<p>No entries 🥲</p>
{:else}
	{#each routes as route}
		<div class="flex items-center justify-between mb-2">
			<button
				class="btn"
				on:click={() => {
					onSelect(route);
				}}>{makeLocationLabel(route.from)} - {makeLocationLabel(route.to)}</button
			>
			<button
				class="btn bg-error-backdrop-token rounded-md"
				on:click={() => {
					routes = routes.filter((or) => or.id !== route.id);
				}}
			>
				🗑️
			</button>
		</div>
	{/each}
{/if}
