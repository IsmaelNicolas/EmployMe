<script>
  import logo from '$lib/media/employme.svg';
  import { goto } from '$app/navigation';
  import {fade } from 'svelte/transition'

  let username = '';
  let password = '';

  let error = "";
  let flag = false;

  async function handleSubmit() {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const response = await fetch('http://localhost:8000/api/login', {
    method: 'POST',
    body: formData,
    credentials: 'include'
  });

  if (response.ok) {
    const { access_token } = await response.json();

    // Guardar el access token en el localStorage
    localStorage.setItem('access_token', access_token);
    goto("/home");
  } else {
	flag = true;
    if (response.status === 404) {
		error = 'Usuario no registrado';
    } else if (response.status === 401) {
		error = 'Credenciales incorrectas';
    } else if (response.status === 422) {
		error = 'Campos vacios';
    } else {
		console.log(response.status); 
		error = 'Servicio no disponible';
    }
  }
}
</script>



<div class="flex flex-col justify-center items-center h-screen bg-gray-50">
	<div class="flex flex-row justify-center items-center">
		<img src={logo} alt="Logo" class="w-16 h-16" />
		<p class="ml-2">EmployME</p>
	</div>
	
	<form
		class="bg-white shadow-lg rounded px-8 pt-6 pb-8 mb-4 mt-5 flex flex-col items-center"
		on:submit|preventDefault={handleSubmit}
	>
		<div class="mb-4">
			<label class="block text-gray-700 text-sm font-bold mb-2" for="username">Usuario</label>
			<input
				class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
				id="username"
				type="text"
				placeholder="Ingrese su usuario"
				bind:value={username}
			/>
		</div>
		<div class="mb-6">
			<label class="block text-gray-700 text-sm font-bold mb-2" for="password">Contraseña</label>
			<input
				class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
				id="password"
				type="password"
				placeholder="Ingrese su contraseña"
				bind:value={password}
			/>
		</div>
		<div class="flex items-center justify-between">
			<button
				class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
				type="submit"
			>
				Iniciar sesión
			</button>
		</div>
		<div class="mt-4">
			<p>
				No tienes cuenta?
				<a href="/register" class="text-blue-500 underline">Crea una cuenta</a>
			</p>
		</div>
	</form>
	{#if flag}
	<div transition:fade class="alert alert-error w-1/4 mt-2">
		<svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
		<span>{error}</span>
	</div>
	{/if}
</div>
