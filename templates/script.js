// script.js
const chatEndpoint = "{% url 'companieroVirtual:chat' %}";
const protocol = "{{ request.scheme }}"; // 'http' o 'https'
const domain = "{{ request.get_host }}"; // Dominio o localhost
const fullUrl = `${protocol}://${domain}${chatEndpoint}`;

function sendMessage() {
    const message = document.getElementById("user-input").value;
    const chatBox = document.getElementById("chat-box");

    // Mostrar mensaje del usuario
    chatBox.innerHTML += `<p class="user-message"><strong>Usuario:</strong> ${message}</p>`;

    // Mostrar cargando mientras espera respuesta de Gemini
    chatBox.innerHTML += `<p class="gemini-message"><strong>Gemini:</strong> <span class="loading"></span></p>`;

    // Limpiar campo de entrada
    document.getElementById("user-input").value = "";

    // Retraso aleatorio entre 1 y 2 segundos
    setTimeout(() => {
        // Realizar la petición
        fetch(fullUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        })
        .then(response => response.json())
        .then(data => {
            const responseMessage = data.response || data.error;

            // Actualizar la conversación con la respuesta de Gemini
            chatBox.innerHTML += `<p class="gemini-message"><strong>Gemini:</strong> ${responseMessage}</p>`;
            chatBox.scrollTop = chatBox.scrollHeight; // Hacer scroll hacia el final
        })
        .catch(error => console.error("Error:", error));
    }, Math.floor(Math.random() * 1000) + 1000); // Retraso aleatorio entre 1 y 2 segundos
}
