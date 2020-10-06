---
title: Video Player
...

<div id="playhere">Missing video name</div>

Playback speed: <input type="text" id="speed" value="1.0" oninput="respeed()"/>

<a href="" id="download"></a>

<script type="text/javascript">
function loadVid() {
    var vid = location.hash.replace('#','lectures/')
    var vtt = vid.replace(/[.][^.]*$/,'.vtt')
    if (vid) {
        document.getElementById('playhere').innerHTML = `
<video controls repload="metadata" style="max-width:100%">
<source src="${vid}" type="video/webm">
<track label="English (AI generated)" src="${vid}" kind="subtitles" srclang="en" default>
</video>
`;
        document.getElementById('download').innerHTML = 'download '+vid.replace(/.*\//g, '')
        document.getElementById('download').href = vid
    }
}
loadVid();

function respeed() {
    let vid = document.querySelector('video')
    if (vid) vid.playbackRate = document.querySelector('#speed').value
}
</script>
