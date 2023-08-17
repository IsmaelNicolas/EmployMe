<script lang="ts">
	import InputForm from '../../../components/InputForm.svelte';
	import { goto } from '$app/navigation';
	import Loader from '../../../components/Loader.svelte';
	import Layout from '../+layout.svelte';
	import { getContext } from 'svelte';
	import { checkToken } from '../../../Utils/Utils';
	import { FlatToast, ToastContainer, toasts } from 'svelte-toasts';
	import { API_ENDPOINT, API_ENDPOINTI } from '../../../Utils/Config';

	let selectedImage: File | null = null;
	let response: { skill_id: string; skill_name: string }[] = [];
	let selectedSkills: { skill_id: string; skill_name: string }[] = [];

	let user_id: string = getContext('user_id');
	//console.log('user_id:', user_id);

	interface Job {
		user_id: string;
		job_title: string;
		job_description: string;
		secondary_street: string;
		main_street: string;
		neighborhood: string;
		job_skills?: string[]; // Definir job_skills como una propiedad opcional
	}

	function handleFileInput(event: Event) {
		const input = event.target as HTMLInputElement;
		const file = input.files?.[0];

		if (file && file.type.startsWith('image/')) {
			selectedImage = file;
		} else {
			selectedImage = null;
			alert('Por favor, selecciona un archivo de imagen válido.');
		}
	}

	let job: Job = {
		user_id: user_id,
		job_title: '',
		job_description: '',
		secondary_street: '',
		main_street: '',
		neighborhood: ''
	};

	async function submitFunction() {
		let skills_ids = selectedSkills.map((skill) => skill.skill_id);
		let jobRequest: Job = { ...job, job_skills: skills_ids };
		let access_token = checkToken();

		const response = await fetch(API_ENDPOINT + '/createpost', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${access_token}`
			},
			body: JSON.stringify(jobRequest)
		});

		if (response.ok) {
			showToast();
			return response.json();
		}
	}

	let submitPromise: any;

	function handleSubmit() {
		submitPromise = submitFunction();
		handleUpload()
		cleanForm();
	}

	let skill_name: string = '';

	function handleInput(event: Event) {
		const target = event.target as HTMLInputElement;
		skill_name = target.value;
	}

	$: if (skill_name.length >= 2) {
		const accessToken = localStorage.getItem('access_token');
		// @ts-ignore
		response = fetch(`http://localhost:8000/api/skills/{skill_name}?param=${skill_name}`, {
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		}).then((res) => {
			if (res.status === 401) {
				goto('/login');
			}

			return res.json();
		});
	}

	function handleCheckboxChange(skill_id: string, skill_name: string) {
		const selectedSkillIndex = selectedSkills.findIndex((skill) => skill.skill_id === skill_id);
		if (selectedSkillIndex !== -1) {
			selectedSkills.splice(selectedSkillIndex, 1);
		} else {
			selectedSkills = [...selectedSkills, { skill_id, skill_name }];
		}
	}

	function removeSkill(skill_id: string) {
		selectedSkills = selectedSkills.filter((skill) => skill.skill_id !== skill_id);
	}

	function cleanForm() {
		job = {
			user_id: user_id,
			job_title: '',
			job_description: '',
			secondary_street: '',
			main_street: '',
			neighborhood: ''
		};

		// Restablecer selectedSkills
		selectedSkills = [];
	}

	function showToast() {
		const toast = toasts.add({
			title: 'Job Post',
			description: 'Publicacion realizada correctamente',
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

	const handleUpload = async () => {
		if (!selectedImage) {
			console.error('Please select an image');
			return;
		}

		const formData = new FormData();
		formData.append('image', selectedImage);
		formData.append('job_id', job.job_title); // Cambia esto con el valor correcto

		const response = await fetch(API_ENDPOINTI + '/jobs/upload', {
			method: 'POST',
			body: formData
		});

		if (response.ok) {
			const data = await response.json();
			selectedImage=null;
			console.log('Image uploaded:', data);
		} else {
			console.error('Error uploading image');
		}
	};
</script>

<div class="h-screen flex flex-col justify-start align-middle">
	<div class="w-full flex">
		<div
			class="w-1/2 m-10 h-fit rounded-lg border shadow-xl bg-blue-50 flex flex-col justify-center align-middle"
		>
			<div class="m-4">
				<input
					type="file"
					accept="image/*"
					class="file-input file-input-bordered file-input-secondary w-full"
					on:change={handleFileInput}
				/>
			</div>
			<div class="m-4">
				{#if selectedImage}
					<img src={URL.createObjectURL(selectedImage)} alt="Imagen seleccionada" />
				{/if}
			</div>
		</div>
		<div class="w-1/2 h-fit flex flex-col align-middle justify-center">
			<form
				class=" m-10 h-fit p-5 rounded-lg border shadow-xl bg-blue-50 flex flex-col justify-center align-middle"
				on:submit|preventDefault={handleSubmit}
			>
				<InputForm text="Titulo" label="Titulo" bind:value={job.job_title} />
				<InputForm
					text="Descripcion"
					label="Descripcion"
					type="textarea"
					bind:value={job.job_description}
				/>
				<InputForm text="Sector / barrio" label="Ubicacion" bind:value={job.neighborhood} />
				<InputForm text="Calle principal" label="Calle principal" bind:value={job.main_street} />
				<InputForm
					text="Calle secundaria"
					label="Calle secundaria"
					bind:value={job.secondary_street}
				/>
			</form>
			<div
				class="m-10 mt-0 h-fit p-5 flex flex-col justify-center align-middle mb-5 rounded-lg border shadow-xl bg-blue-50"
			>
				<label for="my_modal_7" class="btn">Agregar habilidades</label>
				<div class="grid grid-cols-2 auto-cols-min gap-4 p-4">
					{#each selectedSkills as { skill_id, skill_name }}
						<div class="badge badge-accent badge-outline">
							<button class="mr-2" on:click={() => removeSkill(skill_id)}>X</button>
							{skill_name}
						</div>
					{/each}
				</div>

				<!-- Put this part before </body> tag -->
				<input type="checkbox" id="my_modal_7" class="modal-toggle" />
				<div class="modal">
					<div class="modal-box">
						<h3 class="text-lg font-bold">Habilidades necesarias</h3>
						<InputForm
							text="ej: Diseño"
							label="Skills"
							bind:value={skill_name}
							on:input={handleInput}
						/>
						{#await response}
							<div class="mt-5 flex justify-center align-middle h-fit">
								<p>Cargando habilidades...</p>
								<Loader />
							</div>
						{:then skills}
							{#each skills as { skill_id, skill_name }}
								<label>
									<input
										type="checkbox"
										value={skill_id}
										on:change={() => handleCheckboxChange(skill_id, skill_name)}
										checked={selectedSkills.includes({ skill_id, skill_name })}
									/>
									{skill_name}
								</label>
								<br />
							{/each}
						{/await}
						<div class="modal-action">
							<label for="my_modal_7" class="btn btn-info">Aceptar</label>
							<!-- svelte-ignore a11y-no-noninteractive-element-to-interactive-role -->
							<!-- svelte-ignore a11y-click-events-have-key-events -->
							<label
								for="my_modal_7"
								role="button"
								class="btn btn-error"
								on:click={() => {
									selectedSkills = [];
								}}>Cancelar</label
							>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class=" w-full flex align-middle justify-center h-fit">
		{#if selectedImage}
			<InputForm text="Publicar" type="submit" clase="w-1/4" on:clickInput={handleSubmit} />
		{/if}
		{#await submitPromise}
			<Loader />
		{/await}
	</div>

	<ToastContainer let:data>
		<FlatToast {data} />
	</ToastContainer>
</div>
