function generarReporte2() {
    var proyecto = document.getElementById("proyecto2").value;
    var sprint = document.getElementById("sprintId").value; // Aquí obtienes el valor del Sprint

    // Verificar que ambos valores (proyecto y sprint) están presentes
    if (!proyecto || !sprint) {
        alert("Por favor, ingresa tanto el ID del proyecto como el del sprint.");
        return;
    }

    // Mostrar el loader y el texto de carga mientras se realiza la solicitud
    document.getElementById("loader").style.display = "block";
    document.getElementById("loader-text").style.display = "block"; // Mostrar el mensaje de carga

    // Hacer la solicitud para obtener los HUs del sprint
    fetch('/obtener_hus', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            proyecto_id: proyecto,  // Enviar el proyecto_id
            sprint_id: sprint       // Enviar el sprint_id
        })
    })
    .then(response => {
        // Verificar si la respuesta fue exitosa
        if (!response.ok) {
            throw new Error("Error en la solicitud: " + response.statusText);
        }
        return response.json();  // Si la respuesta es correcta, procesar JSON
    })
    .then(data => {
        // Ocultar el loader y el texto de carga
        document.getElementById("loader").style.display = "none";
        document.getElementById("loader-text").style.display = "none";

        // Mostrar el archivo generado y el tiempo de ejecución
        alert("Reporte generado correctamente: " + data.archivo);
        document.getElementById("execution-time").textContent = "Tiempo de ejecución: " + data.tiempo.toFixed(2) + " segundos.";
        document.getElementById("execution-time").style.display = "block"; // Mostrar el tiempo de ejecución

        // Mostrar el enlace para descargar el archivo
        var fileLink = document.getElementById("file-link");
        fileLink.innerHTML = `Tus datos están listos, puedes revisarlos dando clic <a href="${data.archivo}" target="_blank">aquí</a>.`;
        fileLink.style.display = "block"; // Mostrar el enlace
    })
    .catch(error => {
        // Ocultar el loader y el texto de carga en caso de error
        document.getElementById("loader").style.display = "none";
        document.getElementById("loader-text").style.display = "none";
        alert("Hubo un error al generar el reporte: " + error.message);
    });
}
