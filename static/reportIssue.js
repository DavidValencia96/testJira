function generarReporte2() {
    var proyecto = document.getElementById("proyecto2").value;
    var sprint = document.getElementById("sprint2").value;  // Obtener el ID del sprint

    // Verificar que ambos valores (proyecto y sprint) están presentes
    if (!proyecto || !sprint) {
        alert("Por favor, ingresa tanto el ID del proyecto como el del sprint.");
        return;
    }

    // Recoger los tipos de issue seleccionados del formulario 2
    var issueTypes = [];
    var checkboxes = document.querySelectorAll('input[name="issueTypes2"]:checked');
    checkboxes.forEach((checkbox) => {
        issueTypes.push(checkbox.value); // Guardar los tipos seleccionados
    });

    // Mostrar el loader y el texto de carga mientras se realiza la solicitud
    document.getElementById("loader").style.display = "block";
    document.getElementById("loader-text").style.display = "block"; // Mostrar el mensaje de carga

    // Hacer la solicitud al servidor Flask para obtener los HUs, pasando los IDs de proyecto y sprint
    fetch('/obtener_hus', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            proyecto_id: proyecto,
            sprint_id: sprint
        })
    })
    .then(response => response.json())
    .then(data => {
        // Ocultar el loader y el texto de carga
        document.getElementById("loader").style.display = "none";
        document.getElementById("loader-text").style.display = "none"; // Ocultar el mensaje de carga

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
        document.getElementById("loader-text").style.display = "none"; // Ocultar el mensaje de carga
        alert("Hubo un error al generar el reporte.");
    });
}
