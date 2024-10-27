// Asegúrate de que el script se ejecute después de que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {
    const recordTable = document.getElementById('latest-record'); // Cambié 'tableBody' por 'latest-record'

    fetch('http://34.229.43.58:5000/status')
        .then(response => response.json())
        .then(data => {
            const latestRecord = data[0]; // Accedemos al primer (y único) objeto del array

            // Limpiar el contenido existente
            recordTable.innerHTML = '';

            // Crear una nueva fila con los datos obtenidos
            const newRow = document.createElement('tr');

            newRow.innerHTML = `
                <td>${latestRecord.codigo}</td>
                <td>${latestRecord.usuario}</td>
                <td>${latestRecord.ip_cliente}</td>
                <td>${latestRecord.estado}</td>
                <td>${latestRecord.fecha_hora}</td>
                <td>${latestRecord.identificador_dispositivo}</td>
            `;

            // Insertar la nueva fila en el cuerpo de la tabla
            recordTable.appendChild(newRow);
        })
        .catch(error => {
            console.error('Error al obtener el registro más reciente:', error);
            recordTable.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-danger">Error al cargar los datos</td>
                </tr>
            `;
        });
});
