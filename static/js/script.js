/*=========================================================
    SIS-UNETI
    script.js
    Versión 3.0
=========================================================*/

/*=========================================================
    CONFIGURACIÓN GENERAL
=========================================================*/

const CONFIG = {

    zonaHoraria: "America/Caracas",

    idioma: "es-VE",

    ajusteSegundos: 0

};

/*=========================================================
    RELOJ DEL SISTEMA
=========================================================*/

function iniciarReloj(){

    const hora = document.getElementById("hora");

    const fecha = document.getElementById("fecha");

    if(!hora || !fecha){

        return;

    }

    function actualizar(){

        let ahora = new Date();

        ahora.setSeconds(
            ahora.getSeconds() + CONFIG.ajusteSegundos
        );

        hora.textContent = ahora.toLocaleTimeString(

            CONFIG.idioma,

            {

                timeZone: CONFIG.zonaHoraria,

                hour:"2-digit",

                minute:"2-digit",

                second:"2-digit",

                hour12:true

            }

        );

        fecha.textContent = ahora.toLocaleDateString(

            CONFIG.idioma,

            {

                timeZone: CONFIG.zonaHoraria,

                weekday:"long",

                year:"numeric",

                month:"long",

                day:"numeric"

            }

        );

    }

    actualizar();

    const ahora = new Date();

    const espera = 1000 - ahora.getMilliseconds();

    setTimeout(()=>{

        actualizar();

        setInterval(actualizar,1000);

    },espera);

}

/*=========================================================
    CHART.JS
=========================================================*/

function iniciarGrafico(){

    const canvas = document.getElementById("graficoSolicitudes");

    if(!canvas){

        return;

    }

    if(typeof Chart==="undefined"){

        console.warn("Chart.js no está cargado.");

        return;

    }

    if(typeof DATOS_GRAFICO==="undefined"){

        console.warn("No existen datos para el gráfico.");

        return;

    }

    new Chart(canvas,{

        type:"doughnut",

        data:{

            labels:[

                "Pendientes",

                "Aprobadas",

                "Rechazadas"

            ],

            datasets:[{

                data:[

                    DATOS_GRAFICO.pendientes,

                    DATOS_GRAFICO.aprobadas,

                    DATOS_GRAFICO.rechazadas

                ],

                backgroundColor:[

                    "#FFC107",

                    "#198754",

                    "#DC3545"

                ],

                borderColor:"#FFFFFF",

                borderWidth:3,

                hoverOffset:15

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                legend:{

                    position:"bottom",

                    labels:{

                        padding:20,

                        font:{

                            size:14,

                            weight:"bold"

                        }

                    }

                }

            }

        }

    });

}

/*=========================================================
    SIDEBAR
=========================================================*/

function iniciarSidebar(){

    const enlaces = document.querySelectorAll(".sidebar a");

    enlaces.forEach(enlace=>{

        enlace.addEventListener("mouseenter",()=>{

            enlace.style.transition=".30s";

        });

    });

}

/*=========================================================
    TARJETAS DASHBOARD
=========================================================*/

function iniciarDashboard(){

    const tarjetas = document.querySelectorAll(".dashboard-card");

    tarjetas.forEach(card=>{

        card.addEventListener("mouseenter",()=>{

            card.style.transform="translateY(-8px)";

        });

        card.addEventListener("mouseleave",()=>{

            card.style.transform="translateY(0px)";

        });

    });

}

/*=========================================================
    NOTIFICACIONES
=========================================================*/

function iniciarNotificaciones(){

    const alertas=document.querySelectorAll(".alerta");

    alertas.forEach(alerta=>{

        setTimeout(()=>{

            alerta.style.opacity="0";

            alerta.style.transition=".5s";

        },5000);

    });

}

/*=========================================================
    INICIO GENERAL
=========================================================*/

document.addEventListener(

    "DOMContentLoaded",

    ()=>{

        iniciarReloj();

        iniciarGrafico();

        iniciarSidebar();

        iniciarDashboard();

        iniciarNotificaciones();

        iniciarMostrarPassword();

    }

);
 
/*=========================================================
    LOGIN
=========================================================*/

function iniciarLogin(){

    const usuario=document.getElementById("usuario");

    if(usuario){

        usuario.focus();

    }

}

document.addEventListener(

    "DOMContentLoaded",

    ()=>{

        iniciarLogin();

    }

);

/*=========================================================
    MOSTRAR / OCULTAR CONTRASEÑA
=========================================================*/

function iniciarMostrarPassword(){

    const boton = document.getElementById("togglePassword");

    const password = document.getElementById("password");

    if(!boton || !password){

        return;

    }

    boton.addEventListener("click",()=>{

        if(password.type==="password"){

            password.type="text";

            boton.textContent="🙈";

        }

        else{

            password.type="password";

            boton.textContent="👁️";

        }

    });

}

function confirmarEliminar(){

    return confirm(
        "¿Está seguro que desea eliminar esta solicitud?"
    );

}
