document.addEventListener('DOMContentLoaded', () => {
  const formRegistro = document.getElementById('register-form');

  formRegistro.addEventListener('submit', async (e) => {
    e.preventDefault();

    const nombre = document.getElementById('register-name').value.trim();
    const Tarjeta = document.getElementById('register-id').value.trim();
    const correo = document.getElementById('register-email').value.trim();
    const contrasena = document.getElementById('register-password').value.trim();
    const especialidad = document.getElementById('register-specialty').value.trim();

    if (!nombre || !Tarjeta || !correo || !contrasena || !especialidad) {
      alert('Por favor, completa todos los campos.');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/registro-psicologo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nombre,
          Tarjeta,
          correo,
          contrasena,
          especialidad
        })
      });

      const data = await response.json();

      if (data.status === 'ok') {
        alert('✅ Registro exitoso. Revisa tu correo para más detalles.');
        formRegistro.reset();
        // Opcional: cambiar automáticamente a formulario de login
        document.getElementById('btn-login').click();
      } else {
        alert('⚠️ ' + data.mensaje);
      }

    } catch (error) {
      console.error('Error en el registro:', error);
      alert('❌ Error al registrar. Intenta nuevamente.');
    }
  });
});
