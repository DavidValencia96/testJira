// Global variable to store the sprint data
let sprintsData = [];

// Función para obtener el archivo JSON y cargar los datos
async function cargarSprints() {
    try {
        const response = await fetch('/data/data_sprint.json');
        if (!response.ok) {
            throw new Error('No se pudo cargar el archivo JSON');
        }
        sprintsData = await response.json();
        llenarSelect(sprintsData);
    } catch (error) {
        console.error('Error al cargar los sprints:', error);
    }
}



// Función para llenar el select con los nombres de los sprints
function llenarSelect(sprints) {
    const select = document.getElementById('sprintSelect');
    select.innerHTML = '<option value="">Seleccione un sprint</option>';

    sprints.forEach(sprint => {
        const option = document.createElement('option');
        option.value = sprint.id;
        option.textContent = sprint.name;
        select.appendChild(option);
    });
}

// Función para consultar y actualizar los sprints desde Jira
async function consultarSprint() {
    const proyectoId = document.getElementById('proyecto2').value;  // ID del proyecto corregido

    if (!proyectoId) {
        alert('Por favor, ingrese el ID del proyecto.');
        return;
    }

    // Realizamos una solicitud POST para actualizar los sprints
    try {
        const response = await fetch('/actualizar_sprints', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ proyecto_id: proyectoId })  // Enviamos el ID del proyecto
        });

        const result = await response.json();

        if (response.ok) {
            console.log('Sprints actualizados correctamente');
            cargarSprints();  // Recargamos los sprints del archivo JSON actualizado
        } else {
            console.error('Error al actualizar los sprints:', result.error);
            alert('Error al actualizar los sprints. Intente nuevamente.');
        }
    } catch (error) {
        console.error('Error al realizar la solicitud:', error);
    }
}

// Función para actualizar los campos cuando se selecciona un sprint del select
function actualizarCamposSprint() {
    const sprintId = document.getElementById('sprintSelect').value;
    const sprint = sprintsData.find(s => s.id == sprintId);

    if (sprint) {
        document.getElementById('sprintId').value = sprint.id;
        document.getElementById('sprintName').value = sprint.name;
        document.getElementById('sprintState').value = sprint.state;
        document.getElementById('sprintGoal').value = sprint.goal;
    } else {
        document.getElementById('sprintId').value = '';
        document.getElementById('sprintName').value = '';
        document.getElementById('sprintState').value = '';
        document.getElementById('sprintGoal').value = '';
    }
}

// // Llamada a la función cuando la página cargue
// window.onload = cargarSprints;
