document.getElementById("form-solicitar").addEventListener("submit", function (e) {
    e.preventDefault();

    const correo = document.getElementById("correo").value.trim().toLowerCase();

    fetch("http://127.0.0.1:5000/solicitar_recuperacion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correo: correo }),
    })
        .then(res => res.json())
        .then(data => {
        mostrarModal(data.mensaje);
        if (data.status === 'ok') {
            window.location.href = '/html/cambio_contra.html';  
        }
    })
        .catch(err => {
            console.error("Error:", err);
            mostrarModal("Error al solicitar recuperación.");
        });
    });
