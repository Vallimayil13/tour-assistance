let userLocation = { lat: null, lon: null };

// Request user location
function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            userLocation.lat = position.coords.latitude;
            userLocation.lon = position.coords.longitude;
            alert("Location enabled!");
            getNearbySites(userLocation.lat, userLocation.lon);  // Fetch nearby sites
        }, function() {
            alert("Location access denied. Some features may not work.");
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

// Fetch nearby sites from the backend
function getNearbySites(lat, lon) {
    fetch(`/nearby_sites?lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(data => {
            const nearbyList = document.getElementById('nearby-list');
            nearbyList.innerHTML = '';  // Clear any previous content
            data.forEach(site => {
                const siteDiv = document.createElement('div');
                siteDiv.innerHTML = `<strong>${site.name}</strong> <br> ${site.description}`;
                nearbyList.appendChild(siteDiv);
            });
        })
        .catch(error => console.error('Error fetching nearby sites:', error));
}

// Send emergency alert (post user location)
function sendEmergencyAlert() {
    if (userLocation.lat && userLocation.lon) {
        const location = { lat: userLocation.lat, lon: userLocation.lon };
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
    } else {
        alert("Please enable location first.");
    }
}

// Audio Guide button functionality
function startAudioGuide() {
    alert("Audio guide started for this heritage site.");
    // Implement actual audio guide functionality here.
}

// Ask Query functionality
function askQuery() {
    alert("Please ask your query here.");
    // You can implement speech-to-text or other query-related functionality here.
}
