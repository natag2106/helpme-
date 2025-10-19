document.addEventListener("DOMContentLoaded", async () => {
  const usuarioInfo = document.getElementById("usuario-info");
  const usuarioCorreo = document.getElementById("usuario-correo");
  const btnCerrarSesion = document.getElementById("cerrar-sesion");

  // Recuperar el ID del paciente desde localStorage
  const pacienteId = localStorage.getItem("paciente_id");

  // Si no hay ID guardado, redirige al login
  if (!pacienteId) {
    alert("Debes iniciar sesión para acceder a esta página.");
    window.location.href = "/html/acceso.html";
    return;
  }

  try {
    // Validar que el usuario aún exista
    const validarResp = await fetch("http://127.0.0.1:5000/validar_usuario", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ paciente_id: pacienteId })
    });

    const validarData = await validarResp.json();

    if (validarData.status === "ok") {
      // Obtener los datos del usuario
      const usuarioResp = await fetch("http://127.0.0.1:5000/obtener_usuario", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ paciente_id: pacienteId })
      });

      const usuarioData = await usuarioResp.json();

      if (usuarioData.status === "ok") {
        // 👇 Aquí cambiamos "correo" por "nombre"
        usuarioCorreo.textContent = usuarioData.nombre + " 👋";
        usuarioInfo.style.display = "flex";
      } else {
        alert("No se pudo obtener la información del usuario.");
        window.location.href = "/html/acceso.html";
      }
    } else {
      alert("Tu sesión ya no es válida. Inicia sesión nuevamente.");
      localStorage.removeItem("paciente_id");
      window.location.href = "/html/acceso.html";
    }
  } catch (error) {
    console.error("Error al verificar sesión:", error);
    alert("Error de conexión con el servidor.");
    window.location.href = "/html/acceso.html";
  }

  // Cerrar sesión
  btnCerrarSesion.addEventListener("click", () => {
    localStorage.removeItem("paciente_id");
    alert("Has cerrado sesión correctamente.");
    window.location.href = "/html/acceso.html";
  });
});
