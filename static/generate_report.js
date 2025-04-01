function generarReporte() {
    var proyecto = document.getElementById("proyecto").value;
    if (!proyecto) {
        alert("Seleccione un proyecto.");
        return;
    }

    var issueTypes = [];
    var checkboxes = document.querySelectorAll('input[name="issueTypes"]:checked');
    checkboxes.forEach((checkbox) => {
        issueTypes.push(checkbox.value);
    });

    if (issueTypes.length === 0) {
        alert("Por favor selecciona al menos un tipo de issue.");
        return;
    }

    var archivo = "issues_" + proyecto + "_jira.xlsx";

    document.getElementById("loader").style.display = "block";
    document.getElementById("loader-text").style.display = "block";

    fetch('/generar_reporte', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            proyecto: proyecto,
            issueTypes: issueTypes, 
            archivo: archivo
        })
    })
    .then(response => response.json())
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
        alert("Hubo un error al generar el reporte.", error);
    });
}