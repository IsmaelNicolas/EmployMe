<!-- Home.svelte -->

<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	// Función para verificar la autenticación del usuario
	function checkAuthentication() {
		console.log('check localStorage');
		const accessToken = localStorage.getItem('access_token');
		console.log(accessToken);
		if (!accessToken) {
			// Redirigir al usuario a la página de inicio de sesión
			goto('/login');
			
		}
	}

	// Verificar la autenticación al cargar la página
	onMount(checkAuthentication);
</script>

<div class="h-screen">
	<h1>Bienvenido a la página de inicio</h1>
</div>
<!-- Resto del contenido de la página -->
