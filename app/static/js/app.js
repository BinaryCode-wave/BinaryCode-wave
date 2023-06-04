'use stric';
const swither = document.querySelector('.btn');
swither.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    document.body.classList.toggle('light-theme');
    const themeName = document.body.className;
    if (themeName == 'dark-theme') {
        swither.textContent = 'Light';
    } else {
        swither.textContent = 'Dark';
    }
    console.log('current theme: ', themeName);
});

// Carga la API de YouTube
function cargarAPI() {
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}

// Crea un reproductor de YouTube cuando se carga la API
var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '0px',
        width: '0px',
        //videoId: '4XnTqg_A3V0',
        playerVars: {
            listTyoe: 'playlist',
            list: "PLt6NLlIK8lVLGaVv1J1_Mka3wAGX0cIyf"
        },
        events: {
            'onReady': onPlayerReady
        }
    });
}

// Reproduce el video cuando se hace clic en el botón
function reproducirVideo() {
    player.playVideo();
}

function pausarVideo() {
    player.pauseVideo();
}

function nextVideo() {
    player.nextVideo();
}

// Ejecuta algunas acciones cuando el reproductor está listo
function onPlayerReady(event) {
    // Aquí puedes realizar acciones adicionales si es necesario
}

// Carga la API de YouTube cuando la página está lista
document.addEventListener("DOMContentLoaded", cargarAPI);

// Agrega un evento al botón para reproducir el video
document.getElementById("reproducir").addEventListener("click", reproducirVideo);
document.getElementById("pausar").addEventListener("click", pausarVideo);
document.getElementById("siguiente").addEventListener("click", nextVideo)