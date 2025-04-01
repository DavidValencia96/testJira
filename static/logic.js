function cargarProyectos() {
    fetch('/data/projects.json')  
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar el archivo JSON');
            }
            return response.json();
        })
        .then(proyectos => {
            const select = document.getElementById("proyecto");
            select.innerHTML = '';
            const option = document.createElement("option");
            option.value = '';
            option.text = 'Selecciona un Proyecto';
            select.appendChild(option);
            proyectos.forEach(project => {
                const option = document.createElement("option");
                option.value = project.key; 
                option.text = `${project.name} (${project.key})`;
                select.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error cargando el archivo JSON:', error);
            alert('Hubo un error al cargar los proyectos.');
        });
}

function cargarTableros() {
    fetch('/data/boards.json') 
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('proyecto2');
            data.forEach(board => {
                const option = document.createElement('option');
                option.value = board.id; 
                option.textContent = board.location.name || board.name;  
                select.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error al cargar los tableros:', error);
            alert('Hubo un error al cargar los tableros.');
        });
}

window.onload = function() {
    cargarProyectos(); 
    cargarTableros();  
}

