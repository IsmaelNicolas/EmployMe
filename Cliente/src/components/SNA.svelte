<script>
	import { goto } from '$app/navigation';
</script>

<div class="hero min-h-screen bg-base-200">
	<div class="hero-content text-center">
		<div class="max-w-md">
			<h1 class="text-5xl font-bold">Servicio no disponible</h1>
			<p class="py-6">
				Lamentablemente, el servicio no se encuentra disponible en este momento. Estamos trabajando
				para corregir el error y restablecerlo a la brevedad posible. Agradecemos tu paciencia y
				comprensión.
			</p>
			<button class="btn btn-primary" on:click={() => {goto("/login")}}>Volver al inicio</button>
		</div>
	</div>
</div>
