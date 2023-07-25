<script>
	// @ts-ignore
	import Icon from '@iconify/svelte';


	export let value = '';
	export let description = '';
	let editMode = false;
	let editedValue = '';

	function toggleEditMode() {
		editMode = !editMode;
		editedValue = value; // Asignar el valor actual a editedValue
	}

	function saveChanges() {
		value = editedValue;
		toggleEditMode();
	}
</script>

<div class="mb-4">
	<div class="flex items-center">
		{#if editMode}
			<div class="flex items-center">
				<span class="mr-2 text-2xl">{description}:</span>
				<input type="text" bind:value={editedValue} class="input input-bordered" />
				<button class="ml-2" on:click={saveChanges}><Icon icon="material-symbols:check" height={32} color="green"/></button>
			</div>
		{:else}
			<p class="mr-2 text-2xl">{description}: {value}</p>
			<button class="ml-2" on:click={toggleEditMode}><Icon icon="material-symbols:edit" height={24}  color="#2B4162"/></button>
		{/if}
	</div>
</div>
