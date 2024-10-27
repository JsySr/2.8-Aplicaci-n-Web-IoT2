// Importa la función para obtener la dirección IP
import { getClientIP } from './GET-IP-CLIENT.js';  

// Variables globales
let clientIP = '';
let userName = '';

// Obtener la IP al cargar la página
getClientIP().then(ip => {
    if (ip) {
        clientIP = ip;
    } else {
        console.error('No se pudo recuperar la dirección IP');
    }
});

// Función para generar un token en base al nombre usando jsSHA
function createTokenFromName(userName) {
    const shaInstance = new jsSHA("SHA-256", "TEXT");
    shaInstance.update(userName);
    const tokenHash = shaInstance.getHash("HEX");
    return tokenHash;
}

// Función para enviar datos a la API
async function submitData(state) {
    // Obtener el nombre desde el input
    userName = document.getElementById('username').value;

    if (userName.trim() === '') {
        alert('Por favor, escribe tu nombre antes de continuar.');
        return;
    }

    // Generar un token basado en el nombre del usuario
    const deviceID = createTokenFromName(userName);

    const payload = {
        id: '',  // Genera un ID aleatorio
        name: userName,  // Nombre proporcionado por el usuario
        ip_client: clientIP,  // IP pública obtenida
        status: state,  // El estado correspondiente al botón
        date: new Date().toISOString(),  // Fecha actual en formato ISO
        id_device: deviceID  // Token generado a partir del nombre
    };

    // Enviar los datos a la API
    fetch('http://34.229.43.58:5000/status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta de la red');
        }
        return response.json();
    })
    .then(result => {
        console.log('Datos enviados exitosamente:', result);
    })
    .catch(error => {
        console.error('Error al enviar los datos:', error);
    });
}

// Manejador de eventos para los botones
document.getElementById('move-up').addEventListener('click', () => submitData(1));         // Adelante
document.getElementById('move-down').addEventListener('click', () => submitData(2));       // Atrás
document.getElementById('move-left').addEventListener('click', () => submitData(3));       // Izquierda
document.getElementById('move-right').addEventListener('click', () => submitData(4));      // Derecha
document.getElementById('pause').addEventListener('click', () => submitData(0));           // Parar
