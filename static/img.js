// Función para mostrar la imagen de guía según el tipo (proyecto o sprint)
function mostrarImagen(tipo) {
    let imageUrl = '';
    
    if (tipo === 'proyecto') {
        imageUrl = '/data/img/guia1.png'; // Ruta a la imagen del proyecto
    } else if (tipo === 'sprint') {
        imageUrl = '/data/img/guia2.png'; // Ruta a la imagen del sprint
    }

    // Asignamos la ruta de la imagen al src del img
    document.getElementById('imagenGuia').src = imageUrl;

    // Mostramos el modal con la imagen
    document.getElementById('modalImagen').style.display = 'block';
}

// Función para cerrar el modal
function cerrarModal() {
    document.getElementById('modalImagen').style.display = 'none';
}
