<script>
	import Icon from 'svelte-icons-pack/Icon.svelte';
	import HiOutlinePencil from 'svelte-icons-pack/hi/HiOutlinePencil';
	import HiOutlineSave from 'svelte-icons-pack/hi/HiOutlineSave';

	export let value = '';
	export let description = '';
	let editMode = false;
	let editedValue = value;

	function toggleEditMode() {
		editMode = !editMode;
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
				<button class="ml-2" on:click={saveChanges}><Icon src={HiOutlineSave} /></button>
			</div>
		{:else}
			<p class="mr-2 text-2xl">{description}: {value}</p>
			<button class="ml-2" on:click={toggleEditMode}><Icon src={HiOutlinePencil} /></button>
		{/if}
	</div>
</div>
