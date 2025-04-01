// Función para cargar los proyectos desde el archivo JSON
function cargarProyectos() {
    fetch('/data/projects.json')  // Cambia la ruta a /data/projects.json
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar el archivo JSON');
            }
            return response.json();
        })
        .then(proyectos => {
            console.log('Proyectos cargados:', proyectos);  // Imprime los proyectos cargados para depuración

            const select = document.getElementById("proyecto");

            // Limpiamos las opciones existentes (si las hay)
            select.innerHTML = '';

            // Agregamos una opción por defecto
            const option = document.createElement("option");
            option.value = '';
            option.text = 'Selecciona un Proyecto';
            select.appendChild(option);

            // Iteramos sobre los proyectos y creamos un option para cada uno
            proyectos.forEach(project => {
                const option = document.createElement("option");
                option.value = project.key; // Usamos la clave del proyecto
                option.text = `${project.name} (${project.key})`; // Nombre del proyecto y clave
                select.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error cargando el archivo JSON:', error);
            alert('Hubo un error al cargar los proyectos.');
        });
}

function generarReporte() {
    var proyecto = document.getElementById("proyecto").value;
    if (!proyecto) {
        alert("Seleccione un proyecto.");
        return;
    }

    // Recoger los tipos de issue seleccionados
    var issueTypes = [];
    var checkboxes = document.querySelectorAll('input[name="issueTypes"]:checked');
    checkboxes.forEach((checkbox) => {
        issueTypes.push(checkbox.value); // Guardar los tipos seleccionados
    });
    // Verificar en la consola del navegador

    // Si no se selecciona ningún tipo de issue, se muestra una alerta
    if (issueTypes.length === 0) {
        alert("Por favor selecciona al menos un tipo de issue.");
        return;
    }

    // Construir el nombre del archivo basado en el nombre del proyecto
    var archivo = "issues_" + proyecto + "_jira.xlsx";

    // Mostrar el loader y el texto de carga mientras se realiza la solicitud
    document.getElementById("loader").style.display = "block";
    document.getElementById("loader-text").style.display = "block"; // Mostrar el mensaje de carga

    // Hacer la solicitud al servidor Flask para generar el reporte
    fetch('/generar_reporte', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            proyecto: proyecto,
            issueTypes: issueTypes,  // Enviar los tipos de issue seleccionados
            archivo: archivo
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


// Llamamos a la función para cargar los proyectos al cargar la página
window.onload = cargarProyectos;
