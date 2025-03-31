function showForm(formNumber) {
    // Ocultamos ambos formularios
    document.getElementById('formulario1').classList.remove('active');
    document.getElementById('formulario2').classList.remove('active');

    // Activamos el formulario correspondiente
    if (formNumber === 1) {
        document.getElementById('formulario1').classList.add('active');
    } else if (formNumber === 2) {
        document.getElementById('formulario2').classList.add('active');
    }

    // Cambiar el estado activo de las pestañas
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));

    tabs[formNumber - 1].classList.add('active');
}