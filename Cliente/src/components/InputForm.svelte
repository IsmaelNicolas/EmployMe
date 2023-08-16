<script lang="ts">

	import { createEventDispatcher } from 'svelte'
	const dispatch = createEventDispatcher()

	export let text = 'Input text';
	export let label = 'label';
	export let type = 'text';
	export let id: string | undefined = label;
	export let clase = '';
	export let accept = '*';
	export let value = '';
	//export let onClick: () => void = () => {};
	//export let onChange: () => void = () => {};

	function handleClick() {
		dispatch('clickInput')
	}

	function handleChange(event: Event) {
		dispatch('changeInput',event)
	}




</script>

{#if type === 'textarea'}
	<div class="form-control {clase}">
		<label class="label" for="">
			<span class="label-text">{label}</span>
		</label>
		<textarea class="textarea textarea-bordered h-24" placeholder={text} bind:value={value}/>
	</div>
{:else if type === 'submit'}
	<div class=" form-control {clase}">
		<input
			{type}
			value={text}
			class="bg-accent text-white font-semibold py-2 px-4 rounded-xl cursor-pointer hover:bg-primary w-full"
			on:change={handleChange}
			on:click={handleClick}
		/>
	</div>
{:else if type === 'file'}
	<div class="form-control {clase}">
		<input type="file" accept="{accept}" 
			on:change={handleChange}
			on:click={handleClick}
		/>
	</div>
{:else}
	<div class="form-control {clase}">
		<label class="label" for={id}>
			<span class="label-text">{label}</span>
		</label>
		<input type="text" id={id} placeholder={text} class="input input-bordered" bind:value={value} on:input/>
	</div>
{/if}
