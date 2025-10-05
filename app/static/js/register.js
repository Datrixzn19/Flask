// register.js - Validaciones específicas solicitadas

document.addEventListener('DOMContentLoaded', function() {
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confPasswordInput = document.getElementById('conf_password');

    // Validación del nombre (mínimo 3 caracteres)
    nameInput.addEventListener('input', function() {
        const value = nameInput.value.trim();
        const errorElement = document.getElementById('name-error');
        
        if (value.length < 3 && value.length > 0) {
            errorElement.textContent = 'El nombre debe tener 3 o más caracteres';
            errorElement.style.display = 'block';
        } else {
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        }
    });

    // Validación del correo
    emailInput.addEventListener('input', function() {
        const value = emailInput.value.trim();
        const errorElement = document.getElementById('email-error');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (value.length > 0 && !emailRegex.test(value)) {
            errorElement.textContent = 'Por favor, introduce un email válido';
            errorElement.style.display = 'block';
        } else {
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        }
    });

    // Validación de contraseñas iguales en tiempo real
    passwordInput.addEventListener('input', checkPasswords);
    confPasswordInput.addEventListener('input', checkPasswords);

    function checkPasswords() {
        const passwordValue = passwordInput.value;
        const confPasswordValue = confPasswordInput.value;
        const errorElement = document.getElementById('conf_password-error');
        
        if (confPasswordValue.length > 0 && passwordValue !== confPasswordValue) {
            errorElement.textContent = 'Las contraseñas no coinciden';
            errorElement.style.display = 'block';
        } else if (confPasswordValue.length > 0 && passwordValue === confPasswordValue) {
            errorElement.textContent = '✓ Las contraseñas coinciden';
            errorElement.style.color = 'green';
            errorElement.style.display = 'block';
        } else {
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        }
    }
});