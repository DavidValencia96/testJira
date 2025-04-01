function mostrarImagen(tipo) {
    let imageUrl = '';
    
    if (tipo === 'proyecto') {
        imageUrl = '/data/img/guia1.png'; 
    } else if (tipo === 'sprint') {
        imageUrl = '/data/img/guia2.png'; 
    }

    document.getElementById('imagenGuia').src = imageUrl;

    document.getElementById('modalImagen').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('modalImagen').style.display = 'none';
}
