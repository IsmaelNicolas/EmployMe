<script>
	import EditField from './EditField.svelte';
	import avatar from '$lib/media/userexample.jpeg';
	import Stat from './Stat.svelte';
	import logo from '$lib/media/employme.svg';
	import { goto } from '$app/navigation';

	export let user = {
		user_id: '',
		name: '',
		email: '',
		score: 5,
		avatar: avatar
	};

	async function deleteUser() {
		console.log('Borrando usuario...');
		let userid = user.user_id;

		const accessToken = localStorage.getItem('access_token');
		try {
			const response = await fetch(`http://localhost:8000/api/deleteuser/${userid}`, {
				method: 'DELETE',
				headers: {
					'Authorization': `Bearer ${accessToken}`
				}
			});

			if (response.ok) {
				console.log('Usuario eliminado exitosamente');
				goto("/login")
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
					'Authorization': `Bearer ${accessToken}`
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
</script>

<div class="flex flex-row justify-between align-middle items-center">
	<div class="w-1/3 flex flex-col ml-20">
		<h1 class="text-3xl font-bold text-center mb-6 bg-transparent">Perfil de Usuario</h1>
		<div class="w-full justify-between h-max items-center flex">
			<img src={user.avatar} alt="User Avatar" class="rounded-3xl w-full h-full mb-4" />
		</div>
		<EditField description={'Nombre'} bind:value={user.name} />
		<EditField description={'Email'} bind:value={user.email} />
		<div class="flex justify-center  items-center">
			<Stat score={user.score} />
		</div>
		<div class="flex w-full justify-between mt-10">
			<button class="btn btn-info w-1/4">Ver estadísticas</button>
			<button class="btn btn-neutral w-1/4" on:click={updateUser}>Guardar cambios</button>
			<button class="btn btn-error w-1/4" on:click={deleteUser}>Eliminar cuenta</button>
		</div>
	</div>
	<div class="w-1/6 rounded-full mr-72">
		<!-- svelte-ignore a11y-missing-attribute -->
		<img src={logo} />
	</div>
</div>

