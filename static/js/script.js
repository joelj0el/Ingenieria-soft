// static/js/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    // Esta función se ejecuta cuando el documento HTML ha sido completamente cargado

    // Validación del formulario de registro en el lado del cliente
    const registroForm = document.querySelector('form');
    
    if (registroForm) {
        registroForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validación básica de campos vacíos
            const requiredInputs = registroForm.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');
            
            requiredInputs.forEach(function(input) {
                if (input.value.trim() === '') {
                    isValid = false;
                    input.classList.add('is-invalid');
                    
                    // Si no existe ya un mensaje de error, crearlo
                    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorMsg = document.createElement('div');
                        errorMsg.classList.add('invalid-feedback');
                        errorMsg.textContent = 'Este campo es obligatorio';
                        input.parentNode.insertBefore(errorMsg, input.nextElementSibling);
                    }
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            
            // Validación específica del email
            const emailInput = registroForm.querySelector('input[type="email"]');
            if (emailInput && emailInput.value.trim() !== '') {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(emailInput.value)) {
                    isValid = false;
                    emailInput.classList.add('is-invalid');
                    
                    // Si no existe ya un mensaje de error, crearlo
                    if (!emailInput.nextElementSibling || !emailInput.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorMsg = document.createElement('div');
                        errorMsg.classList.add('invalid-feedback');
                        errorMsg.textContent = 'Por favor, introduce un email válido';
                        emailInput.parentNode.insertBefore(errorMsg, emailInput.nextElementSibling);
                    }
                }
            }
            
            // Validación de contraseñas coincidentes en el formulario de registro
            const password1 = registroForm.querySelector('input[name="password1"]');
            const password2 = registroForm.querySelector('input[name="password2"]');
            
            if (password1 && password2 && password1.value && password2.value) {
                if (password1.value !== password2.value) {
                    isValid = false;
                    password2.classList.add('is-invalid');
                    
                    // Si no existe ya un mensaje de error, crearlo
                    if (!password2.nextElementSibling || !password2.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorMsg = document.createElement('div');
                        errorMsg.classList.add('invalid-feedback');
                        errorMsg.textContent = 'Las contraseñas no coinciden';
                        password2.parentNode.insertBefore(errorMsg, password2.nextElementSibling);
                    }
                }
            }
            
            // Si hay errores, prevenir el envío del formulario
            if (!isValid) {
                event.preventDefault();
            }
        });
        
        // Eliminar mensaje de error al modificar un campo
        const allInputs = registroForm.querySelectorAll('input');
        allInputs.forEach(function(input) {
            input.addEventListener('input', function() {
                this.classList.remove('is-invalid');
            });
        });
    }
});