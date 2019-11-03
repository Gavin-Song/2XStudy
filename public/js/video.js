const video = document.getElementById('main-vid');
const SPEEDS = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3];

function videoSpeed(amount) {
    for (let s of SPEEDS)
        document.getElementById('video-speed-' + s).classList.remove('active');
    document.getElementById('video-speed-' + amount).classList.add('active');
    video.playbackRate = amount;
}