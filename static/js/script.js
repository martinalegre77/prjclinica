// Insertar fecha actual en páginas
const $fecha = document.querySelector('.fecha');

function Relojdigital(){
    let f = new Date(),
    dia = f.getDate(),
    mes = f.getMonth(),
    anio = f.getFullYear(),
    diaSemana = f.getDay();

    dia = ('0' + dia).slice(-2);

    let semana = ['DOMINGO','LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO'];
    let nom_mes = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];

    let showSemana = (semana[diaSemana]);
    let showMes = (nom_mes[mes]);
    $fecha.innerHTML = `${showSemana}, ${dia} de ${showMes} de ${anio}.-`;
}

Relojdigital();