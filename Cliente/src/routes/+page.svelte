<script>
	import { goto } from '$app/navigation';

  if (typeof navigator !== 'undefined') {
    goto('/login');
  }
</script>

<h1 class="text-3xl font-bold underline">Hello world!</h1>

<style lang="postcss">
	:global(html) {
		background-color: theme(colors.gray.100);
	}
</style>
