document.addEventListener('DOMContentLoaded', () => {
  const selectPsicologo = document.getElementById('psicologo');

  // Llamar al backend para obtener los psicólogos
  fetch('http://127.0.0.1:5000/obtener_psicologos')
    .then(response => response.json())
    .then(data => {
      if (data.status === 'ok' && Array.isArray(data.psicologos)) {
        data.psicologos.forEach(psicologo => {
            const option = document.createElement('option');
            option.value = psicologo.id;
            option.textContent = `${psicologo.nombre} - ${psicologo.especialidad}`;
            selectPsicologo.appendChild(option);
        });
      } else {
        console.error('No se pudieron cargar los psicólogos.');
      }
    })
    .catch(error => console.error('Error al obtener psicólogos:', error));
});