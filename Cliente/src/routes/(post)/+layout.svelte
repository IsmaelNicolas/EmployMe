<script>
	import Footer from '../../components/Footer.svelte';
	import ServiceNotAvalible from '../../components/SNA.svelte';
	import Navbar from '../../components/Navbar.svelte';
	import { checkToken } from '../../Utils/Utils';
	import { goto } from '$app/navigation';
	import Loader from '../../components/Loader.svelte';
	import { setContext } from 'svelte';
	import { API_ENDPOINT } from '../../Utils/Config';

	async function checKAccess() {
		let access_token = checkToken();

		if (!access_token) {
			goto('/login');
		}

		const response = await fetch(API_ENDPOINT + '/user/me', {
			headers: {
				Authorization: `Bearer ${access_token}`
			}
		});

		if (response.ok) {
			return response.json();
		} else {
			goto('/login');
		}
	}

	// Verificar la autenticación al cargar la página
	const accessPromise = checKAccess();

	// @ts-ignore
	function setUserId(user_id) {
		setContext('user_id', user_id);
	}
</script>

{#await accessPromise}
	<div class="h-screen">
		<Loader />
	</div>
{:then data}
	{#if data.user_id}
		<div class="hidden">
			{setUserId(data.user_id)}
		</div>
	{/if}
	<Navbar user_id={data.user_id} />
	<slot />
	<Footer />
{:catch}
	<div class="h-screen">
		<ServiceNotAvalible />
	</div>
{/await}
