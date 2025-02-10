function sendEmergencyAlert() {
    const location = { lat: 37.7749, lon: -122.4194 }; // Example coordinates

    fetch('/emergency', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ location: location })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => alert('Failed to send alert.'));
}
