document.addEventListener("DOMContentLoaded", () => {
  const psicologoId = localStorage.getItem("psicologo_id");
  const pacienteId = localStorage.getItem("paciente_id");
  const usuarioInfo = document.getElementById("usuario-info");
  const usuarioCorreo = document.getElementById("usuario-correo");
  const navLinks = document.getElementById("nav-links");
  const navbar = document.getElementById("navbar");

  if(psicologoId){
    // Mostrar links de psicologo, ocultar resto
    document.querySelectorAll('.no-login, .paciente-only').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.psicologo-only').forEach(el => el.style.display = 'inline');
    
    usuarioInfo.style.display = 'flex';
    usuarioCorreo.textContent = "Psicólogo 👋";

    // Info a la izquierda, links a la derecha
    navbar.style.justifyContent = 'space-between';
  }
  else if(pacienteId){
    // Mostrar links de paciente, ocultar resto
    document.querySelectorAll('.no-login, .psicologo-only').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.paciente-only').forEach(el => el.style.display = 'inline');
    
    usuarioInfo.style.display = 'flex';
    usuarioCorreo.textContent = "Paciente 👋";

    // Info a la izquierda, links a la derecha
    navbar.style.justifyContent = 'space-between';
  }
  else{
    // Nadie logueado: mostrar solo links de no-login centrados
    document.querySelectorAll('.paciente-only, .psicologo-only').forEach(el => el.style.display = 'none');
    usuarioInfo.style.display = 'none';
    document.querySelectorAll('.no-login').forEach(el => el.style.display = 'inline');

    // Centrar todo
    navbar.style.justifyContent = 'center';
  }

  // Cerrar sesión
  const btnCerrar = document.getElementById('cerrar-sesion');
  btnCerrar?.addEventListener('click', () => {
    localStorage.removeItem('paciente_id');
    localStorage.removeItem('psicologo_id');
    window.location.href = 'index.html';
  });
});
