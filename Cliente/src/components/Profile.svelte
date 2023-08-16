<script>
	import EditField from './EditField.svelte';
	import Stat from './Stat.svelte';
	// @ts-ignore
	import logo from '$lib/media/employme.svg';
	import { goto } from '$app/navigation';
	import avatar from '$lib/media/upload.png';
	import Job from './Job.svelte';
	import InputForm from './InputForm.svelte';
	import { checkToken } from '../Utils/Utils';
	import Loader from './Loader.svelte';

	export let user = {
		user_id: '',
		name: '',
		email: '',
		score: 5,
		avatar: undefined
	};

	$: avatarSrc = user.avatar || avatar;

	async function deleteUser() {
		console.log('Borrando usuario...');
		let userid = user.user_id;

		const accessToken = localStorage.getItem('access_token');
		try {
			const response = await fetch(
				`http://localhost:8000/api/deleteuser/{user_id}?param=${userid}`,
				{
					method: 'DELETE',
					headers: {
						Authorization: `Bearer ${accessToken}`
					}
				}
			);

			if (response.ok) {
				console.log('Usuario eliminado exitosamente');
				goto('/login');
			} else {
				console.log('Error al eliminar el usuario');
			}
		} catch (error) {
			console.log('Error en la solicitud', error);
		}
	}

	async function updateUser() {
		console.log(user);

		const requestData = {
			user_id: user.user_id,
			user_name: user.name,
			user_score: user.score,
			user_email: user.email
		};

		const accessToken = localStorage.getItem('access_token');

		try {
			const response = await fetch('http://localhost:8000/api/updateuser', {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${accessToken}`
				},
				body: JSON.stringify(requestData)
			});

			if (response.ok) {
				console.log('Usuario actualizado exitosamente');
			} else {
				console.log('Error al actualizar el usuario');
			}
		} catch (error) {
			console.log('Error en la solicitud', error);
		}
	}

	let job_title = '';
	function handleInput() {}

	console.log(user);

	async function fetchJobs() {
		let access_token = checkToken();

		if (!access_token) {
			goto('/login');
		}

		const response = await fetch(
			`http://localhost:8000/api/posts/{user_id}?param=${user.user_id}`,
			{
				headers: {
					Authorization: `Bearer ${access_token}`
				}
			}
		);

		if (response.ok) {
			return response.json();
		} else {
			goto('/login');
		}
	}

	const jobsPromise = fetchJobs();

	/**
	 * @type {Promise<any>}
	 */
	let response;

	$: if (job_title.length >= 2) {
		const search = {
			user_id: user.user_id,
			job_tittle: job_title
		};
		let access_token = checkToken();

		response = fetch('http://localhost:8000/api/posts/search', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${access_token}`
			},
			body: JSON.stringify(search)
		}).then((res) => res.json());
	}
</script>

<div class="h-fit flex flex-row justify-center align-middle items-center">
	<div class="w-1/3 h-full flex flex-col ml-20 mb-20">
		<h1 class="text-3xl font-bold text-center mb-6 bg-transparent">Perfil de Usuario</h1>

		<div class="h-1/6">
			<div class="w-full justify-center h-1/2 items-center flex relative mb-5">
				<div class="relative">
					<img
						src={avatarSrc}
						alt="User Avatar"
						class="rounded-3xl w-full h-1/2 transition-opacity duration-300 hover:opacity-10"
					/>
					<div
						class=" rounded-3xl absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 hover:bg-black hover:bg-opacity-25 transition-opacity duration-300"
					>
						<button
							class="text-white btn btn-lg w-1/3 bg-gray-800 px-3 py-1 rounded-lg hover:bg-gray-900 transition-colors duration-300"
						>
							Editar
						</button>
					</div>
				</div>
			</div>
		</div>

		<EditField description={'Nombre'} bind:value={user.name} />
		<EditField description={'Email'} bind:value={user.email} />
		<div class="flex justify-center items-center">
			<Stat score={user.score} />
		</div>
		<div class="flex w-full justify-between mt-10">
			<button class="btn btn-info w-1/4">Ver estadísticas</button>
			<button class="btn btn-neutral w-1/4" on:click={updateUser}>Guardar cambios</button>
			<button class="btn btn-error w-1/4" on:click={deleteUser}>Eliminar cuenta</button>
		</div>
	</div>

	<div class="w-1/3 h-[75vh] ml-20 rounded-md shadow-md">
		<div class="overflow-x-auto h-full rounded-md">
			<table class="table table-pin-rows">
				<thead>
					<tr class="flex justify-center align-middle">
						<InputForm
							text="Titulo del trabajo"
							label="Trabajos publicados"
							clase="w-3/4 "
							bind:value={job_title}
							on:input={handleInput}
						/>
					</tr>
				</thead>
				<tbody class="flex flex-col items-center justify-center">
					{#if job_title.length >= 2}
						{#await response}
							<Loader />
						{:then jobs}
							{#each jobs as job}
								<tr><td class="flex flex-col items-center justify-center"><Job {job} /></td></tr>
							{/each}
						{/await}
					{:else}
						{#await jobsPromise}
							<Loader />
						{:then jobs}
							{#each jobs as job}
								<tr><td class="flex flex-col items-center justify-center"><Job {job} /></td></tr>
							{/each}
						{/await}
					{/if}
				</tbody>
			</table>
		</div>
	</div>
</div>
