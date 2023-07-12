<script>
    import UserProfile from '../../components/Profile.svelte';
    import image from "$lib/media/userexample.jpeg"
  
    let user = {
      name: 'John Doe',
      email: 'johndoe@example.com',
      score: 3,
      avatar: image ,
    };
  </script>
  
  <div class="h-screen">
    <h1 class="text-3xl font-bold text-center mb-6 bg-transparent">Perfil de Usuario</h1>
    <UserProfile {user} />
  </div>
  