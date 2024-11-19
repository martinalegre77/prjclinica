
document.addEventListener('DOMContentLoaded', (event) => {

    // Limpiar localStorage si el método es GET
    const postMethodElement = document.getElementById('postMethod');
    if (postMethodElement && postMethodElement.getAttribute('data-method') === 'False') {
        localStorage.clear();  // Limpiar el localStorage
    }

    const video = document.getElementById('videoElement');
    let canvas = document.getElementById('canvasElement');
    const capturarButton = document.getElementById('capturar');
    const form = document.getElementById('registrationForm');
    const habilitarButton = document.getElementById('habilitar');
    const grabarBtn = document.getElementById('submit');
    const titulo = document.getElementById('user-info');
    let ctx = canvas.getContext('2d');

    if (grabarBtn) {
        grabarBtn.style.display = 'none'; 
    }

    // Para guardar el pass
    const passField = document.getElementById('newpass');


    // Para restaurar posición del mouse
    const savedScrollPosition = localStorage.getItem('scrollPosition');
    if (savedScrollPosition) {
        window.scrollTo(0, parseInt(savedScrollPosition));
        localStorage.removeItem('scrollPosition');
    }


    // Restaurar la imagen si existe en localStorage
    if (localStorage.getItem('capturedImage')) {
        let imageData = localStorage.getItem('capturedImage');
        let img = new Image();
        img.src = imageData;
        img.onload = () => {
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            canvas.style.display = 'inline-block';
            video.style.display = 'none'; // Ocultar el video
        };
        habilitarButton.style.display = 'none';
        grabarBtn.style.display = 'block'; // Mostrar el botón de enviar
    }


    // Ocultar el botón 'Cámara' y mostrar el video al hacer clic en 'Cámara'
    habilitarButton.addEventListener('click', (event) => {
        event.preventDefault();
        habilitarButton.style.display = 'none';
        habilitarCamara();
    });


    function habilitarCamara() {
        canvas.style.display = 'none';
        capturarButton.style.display = 'block';
        navigator.mediaDevices.getUserMedia({ 
            audio: false,
            video: {
                facingMode: 'user',
                width: 200,
                height: 200,
                }
            })
            .then((stream) => {
                video.srcObject = stream;
                setTimeout(function() {
                    capturarButton.style.display = 'inline-block';
                }, 1000); // Espera de 1 segundo
                })
            .catch((error) => {
                console.log(error);
            });
    }


    // Capturar la foto
    capturarButton.addEventListener('click', (event)=> {
        event.preventDefault();
        takePicture();
        video.style.display = 'none';
        capturarButton.style.display = 'none';
        canvas.style.display = 'inline-block';
    })


    function takePicture() {
        if (titulo) {
            titulo.style.display = 'none';
        }
        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
        grabarBtn.style.display = 'block';
        // Guardar la imagen capturada en localStorage
        let imageData = canvas.toDataURL('image/png');
        localStorage.setItem('capturedImage', imageData);
    }


    // Agregar foto al formulario
    form.addEventListener('submit', event => {
        // event.preventDefault(); // Prevenir el envío predeterminado

        const scrollPosition = window.scrollY; // Posición del mouse
        localStorage.setItem('scrollPosition', scrollPosition); // Guardar posición del mouse

        const formData = new FormData(form); // Crear un nuevo objeto FormData

        // Intentar con el contenido del canvas
        canvas.toBlob(blob => {  
            if (blob) {  
                // Si se obtuvo un Blob del canvas, agregarlo al FormData 
                formData.append('image', blob, 'foto.png');  
                enviarFormulario(formData); // Enviar el formulario 
            } else {  
            // Si el canvas está vacío, verificar si hay una imagen en localStorage
                const savedImage = localStorage.getItem('capturedImage');
                if (savedImage) {
                    // Convertir la imagen base64 a Blob
                    const blobFromStorage = dataURItoBlob(savedImage);
                    formData.append('image', blobFromStorage, 'foto.png');
                }
                // Enviar el formulario, se enviará sin imagen si no se encontró nada
            enviarFormulario(formData);
            }
        }, 'image/png');
    });

    // Función para enviar el formulario
    function enviarFormulario(formData) {
        fetch(form.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.redirected) {
                // Redirigir si el servidor lo indica 
                window.location.href = response.url;
                // Limpiar la imagen del localStorage 
                localStorage.removeItem('capturedImage');
            } else {  
                return response.json(); // Procesar la respuesta JSON 
            }  
        })
        .then(data => {
            if (data) {
                console.log('Datos registrados:', data); // Manejar la respuesta
            }
        })
        .catch(error => {
            console.error('Error al registrar los datos:', error); // Manejo de errores
        });
    };

    // Función para convertir base64 a Blob
    function dataURItoBlob(dataURI) {
        const byteString = atob(dataURI.split(',')[1]);
        const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ab], { type: mimeString });
    }

});