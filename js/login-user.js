document.addEventListener('DOMContentLoaded', () => {
  // 🔹 Referencias a elementos
  const btnLogin = document.getElementById('btn-login');
  const btnRegister = document.getElementById('btn-register');
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const loginMsg = document.getElementById('login-msg');
  const registerMsg = document.getElementById('register-msg');

  // 🔹 Cambiar entre formularios
  btnLogin.addEventListener('click', () => {
    btnLogin.classList.add('active');
    btnRegister.classList.remove('active');
    loginForm.classList.add('active');
    registerForm.classList.remove('active');
  });

  btnRegister.addEventListener('click', () => {
    btnRegister.classList.add('active');
    btnLogin.classList.remove('active');
    registerForm.classList.add('active');
    loginForm.classList.remove('active');
  });

  // 🔹 Registro de usuario (paciente)
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      nombre: document.getElementById('register-name').value.trim(),
      email: document.getElementById('register-email').value.trim().toLowerCase(),
      password: document.getElementById('register-password').value.trim()
    };

    if (!data.nombre || !data.email || !data.password) {
      registerMsg.textContent = "Por favor completa todos los campos.";
      registerMsg.className = "msg error";
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/registro-paciente', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      registerMsg.textContent = result.mensaje;
      registerMsg.className = 'msg ' + (result.status === 'ok' ? 'success' : 'error');

      if (result.status === 'ok') {
        setTimeout(() => {
          btnLogin.click();
          registerForm.reset();
        }, 1500);
      }
    } catch (error) {
      console.error("Error al registrar:", error);
      registerMsg.textContent = "Ocurrió un error al registrar. Intenta más tarde.";
      registerMsg.className = "msg error";
    }
  });

// login
    loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      email: document.getElementById('login-email').value.trim().toLowerCase(),
      password: document.getElementById('login-password').value.trim()
    };

    if (!data.email || !data.password) {
      registerMsg.textContent = "Por favor completa todos los campos.";
      registerMsg.className = "msg error";
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/login-usuario', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      registerMsg.textContent = result.mensaje;
      registerMsg.className = 'msg ' + (result.status === 'ok' ? 'success' : 'error');

      if (result.status === 'ok') {
          localStorage.setItem("paciente_id", result.paciente_id);
          setTimeout(() => {
          window.location.href = "/html/dashboard.html";
      }, 1500);
}
    } catch (error) {
      console.error("Error al iniciar sesión:", error);
      registerMsg.textContent = "Ocurrió un error al intentar iniciar sesión. Intenta más tarde.";
      registerMsg.className = "msg error";
    }
  });
});