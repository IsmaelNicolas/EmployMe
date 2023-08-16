<script>
	import image from '$lib/media/work.jpg';

  export let job = {
    job_id: "1205dad8-5a33-45cd-a35e-984bbadc3f74",
    neighborhood: "Carcelen alto",
    job_tittle: "Profesor de nivelacion escolar para ingles",
    job_description: "Profesor de nivelacion escolar para ingles",
    publish_date: "2023-08-14"
  }
  

</script>

<div class="card w-3/4 bg-base-100 shadow-xl">
    <figure class="px-10 pt-10">
      <img src={image} alt="Shoes" class="rounded-xl" />
    </figure>
    <div class="card-body items-center text-center">
      <h2 class="card-title">{job.job_tittle}</h2>
      <p>{job.job_description}</p>
      <div class="card-actions">
        <button class="btn btn-primary">Revisar</button>
      </div>
    </div>
  </div>