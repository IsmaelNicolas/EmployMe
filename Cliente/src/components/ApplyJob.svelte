<script>
	import image from '$lib/media/work.jpg';
	import { onMount } from 'svelte';
	import { API_ENDPOINTI } from '../Utils/Config';

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
        <button
            on:click={() => {
                console.log(job.job_id);
            }}
            class="btn btn-primary">Aplicar</button
        >
	</div>
</div>
