document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const btnSubmit = document.querySelector(".submit-btn");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    btnSubmit.disabled = true;
    btnSubmit.textContent = "Reservando...";

    // Obtener los datos del formulario
    const fecha = document.getElementById("fecha").value;
    const hora = document.getElementById("hora").value;
    const psicologo_id = document.getElementById("psicologo").value;
    const tema = document.getElementById("tema").value.trim();

    // Recuperar el ID del usuario (guardado al iniciar sesión)
    const pacientes_id = localStorage.getItem("usuario_id");

    if (!pacientes_id) {
      alert("Debes iniciar sesión para hacer una reserva.");
      window.location.href = "/login.html";
      return;
    }

    // Enviar los datos al backend
    try {
      const respuesta = await fetch("/reservar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          pacientes_id,
          psicologo_id,
          fecha,
          hora,
          tema,
        }),
      });

      const data = await respuesta.json();

      if (data.status === "ok") {
        alert("✅ Reserva realizada con éxito. Revisa tu correo.");
        form.reset();
      } else {
        alert("⚠️ " + data.mensaje);
      }
    } catch (error) {
      console.error("Error al reservar:", error);
      alert("❌ Error de conexión con el servidor.");
    } finally {
      btnSubmit.disabled = false;
      btnSubmit.textContent = "Reservar sesión";
    }
  });
});
