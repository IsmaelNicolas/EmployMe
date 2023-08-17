<script lang="ts">
	import { goto } from '$app/navigation';
	import logo from '$lib/media/employme.svg';
	import { API_ENDPOINT } from '../../../Utils/Config';
	import InputForm from '../../../components/InputForm.svelte';
	import Loader from '../../../components/Loader.svelte';

	let username = '';
	let password = '';
	let email = '';
	let neighborhood = '';
	let skills = [];
	let skill_name = '';
	let selectedSkills: { skill_id: string; skill_name: string }[] = [];

	function handleCheckboxChange(skill_id: string, skill_name: string) {
		const selectedSkillIndex = selectedSkills.findIndex((skill) => skill.skill_id === skill_id);
		if (selectedSkillIndex !== -1) {
			selectedSkills.splice(selectedSkillIndex, 1);
		} else {
			selectedSkills = [...selectedSkills, { skill_id, skill_name }];
		}
	}

	async function handleSubmit() {
		let skills_ids = selectedSkills.map((skill) => skill.skill_id);
		const userData = {
			user_id: '',
			user_name: username,
			user_score: 0,
			user_email: email,
			user_password: password,
			neighborhood: neighborhood,
			skills: skills_ids
		};

		console.log(userData)

		try {
			const response = await fetch(API_ENDPOINT + '/createuser', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(userData)
			});

			if (response.ok) {
				// El usuario se creó exitosamente
				console.log('Usuario creado correctamente');
				goto('login');
			} else {
				// Error al crear el usuario
				console.log('Error al crear el usuario');
			}
		} catch (error) {
			console.log('Error de conexión:', error);
		}
	}

	function removeSkill(skill_id: string) {
		selectedSkills = selectedSkills.filter((skill) => skill.skill_id !== skill_id);
	}

	function handleInput(event: Event) {
		const target = event.target as HTMLInputElement;
		skill_name = target.value;
	}

	let response: { skill_id: string; skill_name: string }[] = [];

	$: if (skill_name.length >= 2) {
		const accessToken = localStorage.getItem('access_token');
		// @ts-ignore
		response = fetch(`http://localhost:8081/api/skills/${skill_name}`, {
			
		}).then((res) => {
			if (res.status === 401) {
				goto('/login');
			}

			return res.json();
		});
	}
</script>

<div class="flex flex-col justify-center items-center h-screen bg-gray-50">
	<div class="flex flex-row justify-center items-center">
		<img src={logo} alt="Logo" class="w-16 h-16" />
		<p class="ml-2">EmployME</p>
	</div>
	<form
		class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 mt-5 flex flex-col items-center"
		on:submit|preventDefault={handleSubmit}
	>
		<div class="mb-4">
			<label class="block text-gray-700 text-sm font-bold mb-2" for="username"> Usuario </label>
			<input
				class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
				id="username"
				type="text"
				placeholder="Ingrese su usuario"
				bind:value={username}
			/>
		</div>
		<div class="mb-4">
			<label class="block text-gray-700 text-sm font-bold mb-2" for="password"> Contraseña </label>
			<input
				class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
				id="password"
				type="password"
				placeholder="Ingrese su contraseña"
				bind:value={password}
			/>
		</div>
		<div class="mb-4">
			<label class="block text-gray-700 text-sm font-bold mb-2" for="email">
				Correo electrónico
			</label>
			<input
				class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
				id="email"
				type="email"
				placeholder="Ingrese su correo electrónico"
				bind:value={email}
			/>
		</div>

		<div class="mb-4">
			<label class="block text-gray-700 text-sm font-bold mb-2" for="email"> Ubicacion </label>
			<input
				class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
				id="neighborhood"
				type="text"
				placeholder="Ingresa tu barrio o ciudad"
				bind:value={neighborhood}
			/>
		</div>
		<div class="flex justify-center align-middle  flex-col">
			<label for="my_modal_7" class="btn">Agregar habilidades</label>
			<div class="grid grid-cols-2 auto-cols-min gap-4 p-4">
				{#each selectedSkills as { skill_id, skill_name }}
					<div class="badge badge-accent badge-outline">
						<button class="mr-2" on:click={() => removeSkill(skill_id)}>X</button>
						{skill_name}
					</div>
				{/each}
			</div>

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

		<div class="flex items-center justify-between">
			<button
				class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
				type="submit"
			>
				Registrarse
			</button>
		</div>
		<div class="mt-4">
			<p>
				Tienes cuenta?
				<a href="/login" class="text-blue-500 underline">Inicia sesion </a>
			</p>
		</div>
	</form>
</div>
