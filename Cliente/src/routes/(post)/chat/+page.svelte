<script>
	import InputForm from '../../../components/InputForm.svelte';

	let mesg = '';
</script>

<div class="h-screen">
	<div class="flex align-middle justify-center flex-row mt-5">
		<div class="join">
			<input class="input input-bordered join-item" placeholder="Mensaje" />
			<button class="btn join-item rounded-r-full">Enviar</button>
		</div>
	</div>
	<div class="chat chat-start">
		<div class="chat-bubble">It's over Anakin, <br />I have the high ground.</div>
	</div>
	<div class="chat chat-end">
		<div class="chat-bubble">You underestimate my power!</div>
	</div>
	<div class="chat chat-start">
		<div class="chat-bubble">It's over Anakin, <br />I have the high ground.</div>
	</div>
	<div class="chat chat-end">
		<div class="chat-bubble">You underestimate my power!</div>
	</div>
</div>
