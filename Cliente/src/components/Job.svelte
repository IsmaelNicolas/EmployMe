<script>
	import image from '$lib/media/work.jpg';
	import { onMount } from 'svelte';
	import { API_ENDPOINTI } from '../Utils/Config';

	export let job = {
		job_id: '1205dad8-5a33-45cd-a35e-984bbadc3f74',
		neighborhood: 'Carcelen alto',
		job_tittle: 'Profesor de nivelacion escolar para ingles',
		job_description: 'Profesor de nivelacion escolar para ingles',
		publish_date: '2023-08-14'
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

	onMount(fetchImages);
</script>

<div class="card w-3/4 bg-base-100 shadow-xl">
	<figure class="px-10 pt-10">
		<img src={avatarSrc} alt="Shoes" class="rounded-xl" />
	</figure>
	<div class="card-body items-center text-center">
		<h2 class="card-title">{job.job_tittle}</h2>
		<p>{job.job_description}</p>
		<div class="card-actions">
			<button class="btn btn-primary">Revisar</button>
		</div>
	</div>
</div>
