/* Data Section */
function create_table(data) {
    body = document.getElementById("table_body");
    data.forEach(element => {
        var html = "<tr><td>" + element.name + "</td><td>" + element.url + "</td></tr>"
        body.innerHTML += html;
    });
}

/* document.getElementById("create_table").addEventListener("click", () => {
    value = document.getElementById("customRange2").value;
    fetch("/notebook", {
        method: "GET",
    });
}); */

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

async function create_playlist() {
    const response = await fetch("/create_playlist", { method: "POST" });
    const id = await response.json();
    return id;
}

let playlistId = "";
document.getElementById("make_playlist").addEventListener("click", () => {
    create_playlist().then((id) => {
        playlistId = id;
        document.addEventListener("DOMContentLoaded", cargarAPI());
        console.log(playlistId)
    });
});
/* Youtube Section */
var prevTrackBtn = document.getElementById("prev");
var nextTrackBtn = document.getElementById("next");
var actual_track_name = document.getElementById("song-name");
var actual_track_author = document.getElementById("song-author");
var track_img = document.getElementById("track-img");
var playBtn = document.getElementById("play");

function playTrack() {
    player.playVideo();
}

function pauseTrack() {
    player.pauseVideo();
}

function nextVideo() {
    player.nextVideo();
}

function prevVideo() {
    player.previousVideo();
}

playBtn.addEventListener("click", () => {
    playBtn.classList.toggle("running");
    toggleFunction(playBtn.classList.contains("running"));

    function toggleFunction(isRunning) {
        if (isRunning) {
            playTrack();
        } else {
            pauseTrack();
        }
    }
});

var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '0',
        width: '0',
        playerVars: {
            listTyoe: 'playlist',
            list: playlistId
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
    document.getElementById("reproductor").style.display = "block";
}

function cargarAPI() {
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}

function getTrackData() {
    return new Promise((resolve, reject) => {
        var videoData = player.getVideoData();
        console.log(videoData)
        var videoTitle = videoData.title;
        var videoId = videoData.video_id;
        var thumbnailUrl = "https://img.youtube.com/vi/" + videoId + "/maxresdefault.jpg";
        actual_track_name.textContent = videoTitle;
        actual_track_author.textContent = videoData.author;
        track_img.src = thumbnailUrl;
        resolve();
    });
}

function onPlayerReady() {
    getTrackData().then(() => {
        prevTrackBtn.addEventListener("click", () => {
            prevVideo();
        });
        nextTrackBtn.addEventListener("click", () => {
            nextVideo();
        });
    });
}

function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.PLAYING) {
        getTrackData();
    }
}