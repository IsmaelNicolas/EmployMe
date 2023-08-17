<script>
	import image from '$lib/media/work.jpg';
	import { getContext, onMount } from 'svelte';
	import { API_ENDPOINT, API_ENDPOINTI } from '../Utils/Config';
	import { FlatToast, ToastContainer, toasts } from 'svelte-toasts';
	import { checkToken } from '../Utils/Utils';

	let user_id = getContext('user_id');
	export let job = {
		job_id: '1205dad8-5a33-45cd-a35e-984bbadc3f74',
		neighborhood: 'Carcelen alto',
		job_tittle: 'Profesor de nivelacion escolar para ingles',
		job_description: 'Profesor de nivelacion escolar para ingles',
		publish_date: '2023-08-14',
		skill_names: ''
	};

	let images = [];

	$: avatarSrc = image;
	async function fetchImages() {
		try {
			const response = await fetch(API_ENDPOINTI + '/jobs/images?job_id=' + job.job_tittle);
			console.log('response' + response);
			if (response.ok) {
				images = await response.json();
				avatarSrc = images[0].url;
			} else {
				console.error('Error fetching images');
			}
		} catch (error) {
			console.error('Error fetching images:', error);
		}
	}

	function showToast() {
		const toast = toasts.add({
			title: 'Job Apply',
			description: 'Aplicacion realizada correctamente',
			duration: 3000, // 0 or negative to avoid auto-remove
			placement: 'top-right',
			type: 'success',
			theme: 'light',
			showProgress: false,
			onClick: () => {},
			onRemove: () => {}
			// component: BootstrapToast, // allows to override toast component/template per toast
		});
	}

	async function apply() {
		let access_token = checkToken();
		let applyRequest = {
			job_id: job.job_id,
			user_id: user_id
		};
		console.log('job', applyRequest.job_id);
		console.log('user', applyRequest.user_id);
		const response = await fetch(API_ENDPOINT + '/jobs/apply', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${access_token}`
			},
			body: JSON.stringify(applyRequest)
		});

		if (response.ok) {
			showToast();
			console.log(response.status);
			return response.json();
		}
	}

	let applyPromise;
	async function handleApply() {
		applyPromise = apply();
	}

	onMount(fetchImages);
</script>

<div class="card w-96 bg-base-100 shadow-xl mt-5">
	<figure class="h-60"><img src={avatarSrc} alt="Shoes" class="object-fill" /></figure>
	<div class="card-body">
		<h2 class="card-title">
			{job.job_tittle}
		</h2>
		<p>{job.job_description}</p>

		<div class="card-actions justify-end">
			{#each job.skill_names.split(',') as skill}
				<div class="badge badge-outline">{skill}</div>
			{/each}
		</div>
		<button on:click={handleApply} class="btn btn-primary">Aplicar</button>
	</div>
	<ToastContainer let:data>
		<FlatToast {data} />
	</ToastContainer>
</div>
