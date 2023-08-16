<script>
	import logo from '$lib/media/userexample.jpeg';

	function handleLogout() {
		// Eliminar el token de acceso del almacenamiento local
		localStorage.removeItem('access_token');
	}
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
					<img src={logo} />
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
