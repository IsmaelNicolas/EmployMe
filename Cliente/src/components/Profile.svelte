<script>
	import EditField from './EditField.svelte';
	import avatar from '$lib/media/userexample.jpeg';
	import Stat from './Stat.svelte';
	import logo from '$lib/media/employme.svg';
	export let user = {
		name: 'John Doe',
		email: 'johndoe@example.com',
		score: 3,
		avatar: avatar
	};
</script>

<div class="flex flex-row justify-between align-middle items-center">
	<div class="w-1/3 flex flex-col ml-20">
		<div class="w-full justify-between h-max items-center flex">
			<img src={user.avatar} alt="User Avatar" class="rounded-3xl w-full h-full mb-4" />
		</div>
		<EditField description={'Nombre'} value={user.name} />
		<EditField description={'Email'} value={user.email} />
		<Stat score={user.score} />
        <div class="flex w-full justify-between mt-10">
            <button class="btn btn-info w-1/2">Ver estaditicas</button>
            <div class="divider divider-horizontal">OR</div>
            <button class="btn btn-error w-1/2">Eliminar cuenta</button>
        </div>
	</div>
	<div class="w-1/6 rounded-full mr-72">
		<!-- svelte-ignore a11y-missing-attribute -->
		<img src={logo} />
	</div>
</div>
