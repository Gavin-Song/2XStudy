const form = document.getElementById('form');
form.submit = function(e){
    e.preventDefault()
    console.log("HELLO")
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/download', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.send(JSON.stringify({
        videoUrl: document.getElementById('videoUrl').value
    }));
}