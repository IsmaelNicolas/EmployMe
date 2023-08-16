<script>
	import '../app.css';
	import { goto } from '$app/navigation';

	if (typeof navigator !== 'undefined') {
		goto('/login');
	}
</script>

<slot />
