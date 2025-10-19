document.addEventListener("DOMContentLoaded", async () => {
  const usuarioInfo = document.getElementById("usuario-info");
  const usuarioCorreo = document.getElementById("usuario-correo");
  const btnCerrarSesion = document.getElementById("cerrar-sesion");

  // Recuperar el ID del psicólogo desde localStorage
  const psicologoId = localStorage.getItem("psicologo_id");

  // Si no hay ID guardado, redirige al login
  if (!psicologoId) {
    alert("Debes iniciar sesión para acceder a esta página.");
    window.location.href = "/html/psicologo.html";
    return;
  }

  try {
    // Validar que el psicólogo aún exista
    const validarResp = await fetch("http://127.0.0.1:5000/validar_usuario_psicologo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ psicologo_id: psicologoId }) // 
    });

    const validarData = await validarResp.json();

    if (validarData.status === "ok") {
      // Obtener los datos del psicólogo
      const usuarioResp = await fetch("http://127.0.0.1:5000/obtener_usuario_psicologo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ psicologo_id: psicologoId }) 
      });

      const usuarioData = await usuarioResp.json();

      if (usuarioData.status === "ok") {
        usuarioCorreo.textContent = usuarioData.nombre + " 👋";
        usuarioInfo.style.display = "flex";
      } else {
        alert("No se pudo obtener la información del usuario.");
        window.location.href = "/html/psicologo.html";
      }
    } else {
      alert("Tu sesión ya no es válida. Inicia sesión nuevamente.");
      localStorage.removeItem("psicologo_id");
      window.location.href = "/html/psicologo.html";
    }
  } catch (error) {
    console.error("Error al verificar sesión:", error);
    alert("Error de conexión con el servidor.");
    window.location.href = "/html/psicologo.html";
  }

  // Cerrar sesión
  btnCerrarSesion.addEventListener("click", () => {
    localStorage.removeItem("psicologo_id"); // 
    alert("Has cerrado sesión correctamente.");
    window.location.href = "/index.html";
  });
});
