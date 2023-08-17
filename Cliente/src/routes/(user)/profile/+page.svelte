<script>
	import UserProfile from '../../../components/Profile.svelte';
	import Loader from '../../../components/Loader.svelte';
	import { goto } from '$app/navigation';
	import { API_ENDPOINT } from '../../../Utils/Config';

	// @ts-ignore
	function parseUser(userData) {
		return {
			user_id: userData.user_id,
			name: userData.user_name,
			email: userData.user_email,
			score: userData.user_score,
			avatar: undefined
		};
	}

	async function fetchUserProfile() {
		const accessToken = localStorage.getItem('access_token');
		if (accessToken) {
			try {
				const response = await fetch(API_ENDPOINT+'/user/me', {
					headers: {
						Authorization: `Bearer ${accessToken}`
					}
				});

				if (response.ok) {
					return response.json();
				} else if (response.status === 401) {
					goto('/login');
				} else {
					console.log('Error al obtener los datos del usuario');
					return false;
				}
			} catch (error) {
				console.log('Error de conexión:', error);
				return false;
			}
		}
	}

	const userDataPromise = fetchUserProfile();
</script>

<div class="h-fit">
	{#await userDataPromise}
		<Loader />
	{:then userData}
		{#if userData}
			<UserProfile user={parseUser(userData)} />
		{:else}
			<p>No se pudieron cargar los datos del usuario.</p>
		{/if}
	{:catch error}
		<p>Error: {error.message}</p>
	{/await}
</div>
