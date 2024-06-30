
const habilitarButton = document.getElementById('habilitar');
const capturarButton = document.getElementById('capturar');
const video = document.getElementById('videoElement');
let canvas = document.getElementById('canvasElement');
const form = document.getElementById('registrationForm');
const grabarBtn = document.getElementById('grabar-btn');
const titulo = document.getElementById('user-info')

// Ocultar el botón 'Cámara' y mostrar el video al hacer clic en 'Cámara'
habilitarButton.addEventListener('click', function(event) {
    event.preventDefault();
    habilitarButton.style.display = 'none';
    habilitarCamara();
});

function habilitarCamara() {
    canvas.style.display = 'none';
    capturarButton.style.display = 'block';
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
                    setTimeout(function() {
                        boton.style.display = 'inline-block';
                        }, 1000); // Espera de 1 segundo
                }
            )
        .catch((error) => {
            console.log(error);
        });
}


capturarButton.addEventListener('click', (event)=> {
    event.preventDefault();
    takePicture();
    video.style.display = 'none';
    capturarButton.style.display = 'none';
    canvas.style.display = 'inline-block';
    grabarBtn.style.display = 'block';
    
})


function takePicture() {
    titulo.style.display = 'none';
    let ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
}


// Enviar el formulario
form.addEventListener('submit', event => {
    event.preventDefault();

    canvas.toBlob(blob => {
        const formData = new FormData(form);
        formData.append('image', blob, 'foto.png');

        fetch(form.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data) {
                console.log('Datos registrados:', data);
            }
        })
        .catch(error => {
            console.error('Error al registrar los datos:', error);
        });
    }, 'image/png');
});