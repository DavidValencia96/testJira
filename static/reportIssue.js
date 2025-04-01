function generarReporte2() {
    var proyecto = document.getElementById("proyecto2").value;
    var sprint = document.getElementById("sprintId").value; 

    if (!proyecto || !sprint) {
        alert("Por favor, ingresa tanto el ID del proyecto como el del sprint.");
        return;
    }

    document.getElementById("loader").style.display = "block";
    document.getElementById("loader-text").style.display = "block"; 

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
    .then(response => {
        if (!response.ok) {
            throw new Error("Error en la solicitud: " + response.statusText);
        }
        return response.json();  
    })
    .then(data => {
        document.getElementById("loader").style.display = "none";
        document.getElementById("loader-text").style.display = "none";

        alert("Reporte generado correctamente: " + data.archivo);
        document.getElementById("execution-time").textContent = "Tiempo de ejecución: " + data.tiempo.toFixed(2) + " segundos.";
        document.getElementById("execution-time").style.display = "block";

        var fileLink = document.getElementById("file-link");
        fileLink.innerHTML = `Tus datos están listos, puedes revisarlos dando clic <a href="${data.archivo}" target="_blank">aquí</a>.`;
        fileLink.style.display = "block"; 
    })
    .catch(error => {
        document.getElementById("loader").style.display = "none";
        document.getElementById("loader-text").style.display = "none";
        alert("Hubo un error al generar el reporte: " + error.message);
    });
}
