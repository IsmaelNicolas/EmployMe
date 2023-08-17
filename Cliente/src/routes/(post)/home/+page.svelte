<!-- Home.svelte -->
<script lang="ts">
	import { API_ENDPOINT } from '../../../Utils/Config';
	import { checkToken } from '../../../Utils/Utils';
	import { goto } from '$app/navigation';
	import Loader from '../../../components/Loader.svelte';
	import { getContext } from 'svelte';
	import InputForm from '../../../components/InputForm.svelte';
	import ApplyJob from '../../../components/ApplyJob.svelte';

	let user_id: string = getContext('user_id');

	async function fetchJobs() {
		let access_token = checkToken();
		const response = await fetch(API_ENDPOINT + `/jobs/{user_id}?param=${user_id}`, {
			headers: {
				Authorization: `Bearer ${access_token}`
			}
		});

		if (response.ok) {
			console.log(response);
			return response.json();
		} else if (response.status === 401) {
			goto('/login');
		} else {
			console.log('Error al obtener los datos del usuario');
			return false;
		}
	}

	const jobsPromise = fetchJobs();

	let job_title = '';

	function handleInput() {}

	let response: Promise<any>;

	$: if (job_title.length >= 2) {
		const search = {
			user_id: user_id,
			job_tittle: job_title
		};
		let access_token = checkToken();

		response = fetch(API_ENDPOINT + '/jobs/search', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${access_token}`
			},
			body: JSON.stringify(search)
		}).then((res) => res.json());
	}
</script>

<div class="h-screen flex flex-col bg-slate-100">
	<div class="w-full flex justify-center align-middle">
		<InputForm
			text="Titulo del trabajo"
			label="Buscar trabajo"
			clase="w-1/4"
			bind:value={job_title}
			on:input={handleInput}
		/>
	</div>
	<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
		{#if job_title.length >= 2}
			{#await response}
				<Loader />
			{:then jobs}
				{#each jobs as job}
					<ApplyJob {job} />
				{/each}
			{/await}
		{:else}
			{#await jobsPromise}
				<Loader />
			{:then jobs}
				{#each jobs as job}
					<ApplyJob {job} />
				{/each}
			{/await}
		{/if}
	</div>
</div>
