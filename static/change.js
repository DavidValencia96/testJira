function showForm(formNumber) {
    document.getElementById('formulario1').classList.remove('active');
    document.getElementById('formulario2').classList.remove('active');

    if (formNumber === 1) {
        document.getElementById('formulario1').classList.add('active');
    } else if (formNumber === 2) {
        document.getElementById('formulario2').classList.add('active');
    }

    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));

    tabs[formNumber - 1].classList.add('active');
}