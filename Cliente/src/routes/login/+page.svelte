<script>
    import logo from '$lib/media/employme.svg';
    let username = '';
    let password = '';
  
    function handleSubmit() {
      // Lógica para procesar los datos del formulario aquí
      console.log('Usuario:', username);
      console.log('Contraseña:', password);
    }
  </script>
  
  <div class="flex flex-col justify-center items-center h-screen">
    <div class="flex flex-row justify-center items-center">
      <img src={logo} alt="Logo" class="w-16 h-16" />
      <p class="ml-2">EmployME</p>
    </div>
    <form
      class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 mt-5 flex flex-col items-center"
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
        <a href="/createaccount" class="text-blue-500 underline">Crea una cuenta</a>
    </p>
      </div>
    </form>
  </div>
  