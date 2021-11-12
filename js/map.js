function sendData(event) {
    let contactForm = document.getElementById("contact-form");
    let formData = new FormData(contactForm);

    fetch("/cgi-bin/addnode", {
        method: 'POST',
        body: formData,
    })
        .then(result => {
            check_error = {};
            error_box = document.getElementById("address-error");
            if (result.body) {
                result.json()
		    .then(decode => {
            		if (decode.error) {
                		error_box.style.display = "block";
            		} else {
                contactForm.reset();
                error_box.style.display = "none";
                drawMarkers();
            }});
        }})
        .catch(error => {
            console.error("Form submit error: ", error);
        });

    event.preventDefault();
}

function drawMarkers() {
    fetch("/cgi-bin/getnodes")
        .then(response => response.json())
        .then(nodes => {
            nodes.forEach(node => {
                L.circleMarker([node[1], node[2]], {
                    color: "white",
                    weight: 2,
                    fillColor: node[3] ? "blue" : "grey",
                    fillOpacity: 0.7,
                    radius: 8,
                }).addTo(meshmap);
            });
        })
}

var meshmap = L.map('mapid').setView([38.8872, -77.0169], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(meshmap);

let contactForm = document.getElementById("contact-form");
contactForm.addEventListener('submit', sendData);

drawMarkers();
