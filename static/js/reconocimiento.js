

document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('videoElement');
    const habilitarCam = document.getElementById('habilitar');
    const camContainer = document.getElementById('cam-container');
    const grabarBtn = document.getElementById('grabar-btn');

    habilitarCam.addEventListener('click', function (event) {
        event.preventDefault();
        habilitarCamara();
        camContainer.style.display = 'block';  // Mostrar el contenedor del video y el formulario
        setTimeout(function () {
            grabarBtn.style.display = 'block';  // Mostrar el botón de grabar después de 3 segundos
        }, 3000);
    });
});

function habilitarCamara() {
    // canvas.style.display = 'none';
    navigator.mediaDevices.getUserMedia({ audio: false,
                                            video: {
                                                facingMode: 'user',
                                                width: 200,
                                                height: 200,
                                                }})
        .then(
            (stream) => {
                video.srcObject = stream;
                console.log(stream);
                }
            )
}
