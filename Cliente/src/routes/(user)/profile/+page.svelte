<script>
  import { onMount } from 'svelte';
  import UserProfile from '../../../components/Profile.svelte';
  import image from "$lib/media/userexample.jpeg";

  let user = {
    user_id:'',
    name: '',
    email: '',
    score: 0,
    avatar: image,
  };

  async function fetchUserProfile() {
    // Obtener el access token del localStorage
    const accessToken = localStorage.getItem('access_token');

    if (accessToken) {
      try {
        const response = await fetch('http://localhost:8000/api/user/me', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (response.ok) {
          const userData = await response.json();
          console.log(userData)
          // Actualizar los datos del usuario
          user = {
            user_id: userData.user_id,
            name: userData.user_name,
            email: userData.user_email,
            score: userData.user_score,
            avatar: image,
          };
        } else {
          console.log('Error al obtener los datos del usuario');
        }
      } catch (error) {
        console.log('Error de conexión:', error);
      }
    }
  }

  // Realizar la petición al cargar el componente
  onMount(fetchUserProfile);
</script>

<div class="h-screen">
  
  <UserProfile {user} />
</div>
