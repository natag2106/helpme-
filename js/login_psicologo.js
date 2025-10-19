document.addEventListener('DOMContentLoaded', () => {
  const formLogin = document.getElementById('login-form');

  formLogin.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value.trim();

    if (!email || !password) {
      alert('Por favor, completa todos los campos.');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/login-psicologo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (data.status === 'ok') {
        alert('✅ Inicio de sesión exitoso.');
        
        // Guarda el ID del usuario en localStorage para mantener sesión
        localStorage.setItem('psicologo_id', data.usuario_id);

        // Redirige al panel del psicólogo (ajusta la ruta según tu estructura)
        window.location.href = '/html/dashboard_prueba.html';
      } else {
        alert('⚠️ ' + data.mensaje);
      }

    } catch (error) {
      console.error('Error al iniciar sesión:', error);
      alert('❌ Error en la conexión con el servidor.');
    }
  });
});
