let sprintsData = [];

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

async function consultarSprint() {
    const proyectoId = document.getElementById('proyecto2').value; 

    if (!proyectoId) {
        alert('Por favor, ingrese el ID del proyecto.');
        return;
    }

    try {
        const response = await fetch('/actualizar_sprints', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ proyecto_id: proyectoId }) 
        });

        const result = await response.json();

        if (response.ok) {
            console.log('Sprints actualizados correctamente');
            cargarSprints();
        } else {
            console.error('Error al actualizar los sprints:', result.error);
            alert('Error al actualizar los sprints. Intente nuevamente.');
        }
    } catch (error) {
        console.error('Error al realizar la solicitud:', error);
    }
}

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