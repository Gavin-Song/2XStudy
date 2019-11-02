const qr = new QRCode(document.getElementById('qrcode'));

function share() {
    let url = window.location;
    qr.makeCode(url); // Generate QR Code
    document.getElementById('url').innerHTML = url;

    // Show the modal
    document.getElementById('modal').style.display = 'block';
}