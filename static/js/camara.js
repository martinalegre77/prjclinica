
const video = document.getElementById('videoElement');
let boton = document.getElementById('capturar');
let canvas = document.getElementById('canvasElement');
const form = document.getElementById('registrationForm');

document.getElementById('habilitar').addEventListener('click', ()=> {
    habilitarCamara();
})


function habilitarCamara() {
    canvas.style.display = 'none';
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


document.getElementById('capturar').addEventListener('click', ()=> {
    takePicture();
    boton.style.display = 'none';
    canvas.style.display = 'inline-block';
})


function takePicture() {
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