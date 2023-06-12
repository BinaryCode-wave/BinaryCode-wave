/* Data Section */
function create_table(data) {
    body = document.getElementById("table_body");
    data.forEach(element => {
        var html = "<tr><td>" + element.name + "</td><td>" + element.url + "</td></tr>"
        body.innerHTML += html;
    });
}

document.getElementById("create_table").addEventListener("click", () => {
    value = document.getElementById("customRange2").value;
    fetch("/data?value=" + value, {
        method: "POST",
    }).then(response => response.json()).
        then((data) => {
            document.getElementById("no_data").style.display = "none";
            create_table(data);
            var table = document.getElementById("data");
            table.style.display = "block";

        });
});

/* Create Playlist */

var player;

async function create_playlist() {
    const response = await fetch("/create_playlist", { method: "POST" });
    const id = await response.json();
    return id;
}
let playlistId = "";
document.getElementById("make_playlist").addEventListener("click", () => {
    create_playlist().then((id) => {
        playlistId = id;
        document.addEventListener("DOMContentLoaded", cargarAPI);

        player = new YT.Player('player', {
            height: '150px',
            width: '150px',
            playerVars: {
                listTyoe: 'playlist',
                list: playlistId,
            }
        });

        document.getElementById("reproductor").style.display = "block";
    });
});

/* Youtube Section */
function cargarAPI() {
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}

function reproducirVideo() {
    player.playVideo();
}

function pausarVideo() {
    player.pauseVideo();
}

function nextVideo() {
    player.nextVideo();
}

function previousVideo() {
    player.previousVideo();
}

document.getElementById("reproducir").addEventListener("click", reproducirVideo);
document.getElementById("pausar").addEventListener("click", pausarVideo);
document.getElementById("siguiente").addEventListener("click", nextVideo);