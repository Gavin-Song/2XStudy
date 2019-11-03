const video = document.getElementById('main-vid');
const SPEEDS = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3];

let base_speed = 1.0;
let time_speed = 1.0;

function videoSpeed(amount) {
    for (let s of SPEEDS)
        document.getElementById('video-speed-' + s).classList.remove('active');
    document.getElementById('video-speed-' + amount).classList.add('active');
    base_speed = amount;
    video.playbackRate = base_speed * time_speed;
}

function togglePlaybackSound(id, button) {
    let sound = document.getElementById('audio-' + id);
    sound.paused ? sound.play() : sound.pause();
    button.innerHTML = '<i class="material-icons">' + 
        (sound.paused ? 'volume_up' : 'pause') + '</i>';
}

// Set time
setInterval(() => {
    let t = x => +Object.keys(x)[0]; // Temp to get key as float
    time_speed = Object.values(BREAKS[BREAKS.length - 1])[0] === "" ? 1 : 5;
    for (let i = 0; i < BREAKS.length - 1; i++) {
        let a = t(BREAKS[i]);
        let b = t(BREAKS[i + 1]);

        if (video.currentTime >= a && video.currentTime < b) {
            time_speed = Object.values(BREAKS[i])[0] === "" ? 1 : 5;
            break;
        }
    }
    video.playbackRate = base_speed * time_speed
}, 100);