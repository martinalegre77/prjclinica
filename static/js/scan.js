
function onScanSuccess(qrCodeMessage) {
    // Manejar el resultado del escaneo
    console.log("Código QR escaneado:", qrCodeMessage);

    // Verificar si el código QR tiene exactamente 8 números
    const regex = /^[0-9]{8}$/;
    if (!regex.test(qrCodeMessage)) {
        // Redirigir a la página 'no-encontrado.html'
        window.location.href = '/no-encontrado.html';
        return;
    }

    // Redirigir a la página 'consulta-deportista.html' y agregar el número escaneado o 0
    window.location.href = `/municipalidad/consulta-deportista/${qrCodeMessage}`;

    // document.getElementById('result').innerHTML = `Código QR Escaneado: ${qrCodeMessage}`;
    // // Detener el escaneo una vez se ha escaneado el código QR
    // html5QrcodeScanner.clear();
}

function onScanError(errorMessage) {
    // Manejar los errores del escaneo
    console.error("Error en el escaneo:", errorMessage);
}

// Asegúrate de que Html5QrcodeScanner esté definido
if (typeof Html5QrcodeScanner !== 'undefined') {
    const html5QrcodeScanner = new Html5QrcodeScanner(
        "reader", { fps: 10, qrbox: 250 });

    // Personalizar los textos de los botones
    html5QrcodeScanner.textResources = {
        startScanning: "Leer QR",  // Personalizar el texto del botón "Start Scanning"
        stopScanning: "Parar",  // Dejar vacío para no mostrar texto en el botón "Stop Scanning"
        scanImageFile: ""          // Dejar vacío para no mostrar texto en el botón "Scan an Image File"
    };

    html5QrcodeScanner.render(onScanSuccess, onScanError);
} else {
    console.error("Html5QrcodeScanner no está definido. Verifica que la biblioteca html5-qrcode se haya cargado correctamente.");
}