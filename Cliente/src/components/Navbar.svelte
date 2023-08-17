<script lang="ts">
	// @ts-ignore
	import logo from '$lib/media/userexample.jpeg';
	import { onMount } from 'svelte';
	import { API_ENDPOINTI } from '../Utils/Config';

	function handleLogout() {
		// Eliminar el token de acceso del almacenamiento local
		localStorage.removeItem('access_token');
	}

	export let user_id ='';
	let images = [];
	
	$: avatarSrc =  logo;
	async function fetchImages() {
		try {
			const response = await fetch(API_ENDPOINTI+'/user/images?user_id='+user_id);
			console.log('response' + response)
			if (response.ok) {
				images = await response.json();
				avatarSrc = images[0].url
			} else {
				console.error('Error fetching images');
			}
		} catch (error) {
			console.error('Error fetching images:', error);
		}
	}

	onMount(fetchImages)

</script>

<div class="navbar bg-accent">
	<div class="flex-1 navbar-start">
		<a href="/home" class="btn btn-ghost normal-case text-xl">EmployME</a>
	</div>
	<div class="navbar-center hidden lg:flex">
		<ul class="menu menu-horizontal px-1">
			<li><a href="/publicar">Publicar</a></li>
			<li><a href="/home">Buscar</a></li>
		</ul>
	</div>

	<div class="flex-none gap-2 navbar-end">
		<div class="dropdown dropdown-end">
			<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
			<div tabindex="0" class="btn btn-ghost btn-circle avatar">
				<div class="w-full rounded-full">
					<!-- svelte-ignore a11y-missing-attribute -->
					<img src={avatarSrc} />
				</div>
			</div>
			<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
			<ul
				tabindex="0"
				class="mt-3 z-[1] p-2 shadow-lg menu menu-sm dropdown-content bg-base-100 rounded-box w-52"
			>
				<li>
					<a href="/profile" class="justify-between">
						Profile
						<span class="badge">New</span>
					</a>
				</li>
				<li><a href="/home">Chat</a></li>
				<li><a href="/home">Settings</a></li>
				<li><a href="/login" on:click={handleLogout}>Logout</a></li>
			</ul>
		</div>
	</div>
</div>
