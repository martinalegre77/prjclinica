document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('video_r');
    iniciarVideo(video);
    await esperar(2);
    enviarDatosFormulario()
});


function iniciarVideo(video) {
    navigator.mediaDevices.getUserMedia({ video: {} })
        .then(stream => {
            video.srcObject = stream;
        })
}


function enviarDatosFormulario() {
    const formData = new FormData();
    formData.append('deportista', deportista);

    for (const key in formulario) {
        if (formulario.hasOwnProperty(key)) {
            formData.append(key, formulario[key]);
        }
    }

    fetch('/clinica/guardado-success.html/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al enviar los datos del formulario.');
        }
        return response.json();
    })
    .then(data => {
        console.log('Datos guardados correctamente:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function esperar(segundos) {
    return new Promise(resolve => setTimeout(resolve, segundos * 1000));
}
