function youtube_parser(url) {
    let regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
    let match = url.match(regExp);
    return (match && match[7].length == 11) ? match[7] : false;
}

function submit() {
    let content = document.getElementById('content');
    let content_list = document.getElementById('content-list');

    /* Verify if url is valid */
    let url = document.getElementById('videoUrl').value;
    let id = youtube_parser(url);
    if (!id) {
        dispError('Not a valid youtube url');
        return;
    }

    if (content_list) {
        let animationID = "content-animaton-" + Math.random();
        content_list.innerHTML = `<li id="${animationID}">
            <img src="/img/loading.gif">
        </li>` + content_list.innerHTML;
    }

    /* Send POST request and await response */
    errmsg.style.opacity = '0';
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/download', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let res = xhr.responseText;
            if (res.includes('pytube.exceptions.RegexMatchError'))
                dispError('Invalid youtube url');
            else if (res.includes('Video has no captions') || res.includes('IndexError') || res.includes('index out of'))
                dispError('Video has no captions');
            else if (res.includes('ERROR'))
                dispError(res);
            else if (res.startsWith('DONE')) {
                let json = '{' + res.split('{')[1];
                /* Set the youtube ID to local storage */
                window.localStorage.setItem(id, json);

                // Remove loading animation
                window.location.reload();
            }
        }
    };
    xhr.send(JSON.stringify({
        videoUrl: url
    }));
}

function loadStudySets() {
    let content = document.getElementById('content');
    let content_list = document.getElementById('content-list');

    content.innerHTML = '';
    let keys = Object.entries(localStorage).map(x => x[0]);

    /* Create list of study sets */
    if (keys.length > 0) {
        let newhtml = '';
        for (let key of keys) {
            let i = JSON.parse(window.localStorage.getItem(key));
            newhtml += `<li onclick="window.location.href='/saves/${key}/'">
            <img src="/saves/${key}/thumb.jpg"
                onerror="this.src='/img/loading.gif'">
            <p>
            ${i.video_title}
            <br>
            <small>${i.video_author} | ${i.video_length}</small></p>
            </li>`
            window.localStorage.getItem('user');
        }
        content.innerHTML = `<div class="grid">
                <ul id="content-list">
                    ${newhtml}
                </ul>
            </div>`;
        
    } else { // Empty state
        content.innerHTML = '<div style="text-align: center; color: #888">' +
                            '<img src="img/empty-state.png" class="empty-state"><br>' +
                            'Looks like you have no study sets :(</div>';
    }
}