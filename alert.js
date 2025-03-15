document.getElementById("sosButton").addEventListener("click", function () {
    if (navigator.geolocation) {
        let attempts = 0; // Retry counter
        
        function getLocation() {
            navigator.geolocation.getCurrentPosition(function (position) {
                let lat = position.coords.latitude;
                let lon = position.coords.longitude;
                let accuracy = position.coords.accuracy; // Accuracy in meters
                
                if (accuracy > 50 && attempts < 3) { // Retry if accuracy is poor
                    attempts++;
                    setTimeout(getLocation, 500);  // Wait 500ms before retrying
                    return;
                }

                let locationLink = `https://www.google.com/maps?q=${lat},${lon}`;
                document.getElementById("locationInfo").innerHTML = 
                    `<p>📍 <strong>My Location:</strong> <a href="${locationLink}" target="_blank">${locationLink}</a></p>
                     <p>🎯 <strong>Accuracy:</strong> ±${accuracy.toFixed(2)} meters</p>`;

                // SOS Message for Email
                let message = `🚨 SOS Alert!\n\nI need urgent help!\n\n📍 My location: ${locationLink}\n\n🎯 Accuracy: ±${accuracy.toFixed(2)} meters`;

                let email = "pvm132004@gmail.com";
                let gmailURL = `https://mail.google.com/mail/?view=cm&fs=1&to=${email}&su=Emergency SOS&body=${encodeURIComponent(message)}`;

                // Open Gmail with pre-filled details
                window.open(gmailURL, "_blank");

            }, function (error) {
                let errorMessage = "❌ Location access denied!";
                
                if (error.code === 1) {
                    errorMessage += "\n👉 Please enable GPS and allow location access in browser settings.";
                } else if (error.code === 2) {
                    errorMessage += "\n👉 Unable to determine location. Move to an open area.";
                } else if (error.code === 3) {
                    errorMessage += "\n👉 Location request timed out. Try again.";
                }

                // Retry if possible
                if (attempts < 3) {
                    attempts++;
                    setTimeout(getLocation, 1000);  // Wait 1 second before retrying
                } else {
                    alert(errorMessage);
                }
                
            }, {
                enableHighAccuracy: true, // Use GPS instead of IP-based location
                timeout: 15000,  // Waits up to 15 seconds for GPS lock
                maximumAge: 0    // Always fetch a fresh location
            });
        }

        getLocation(); // Start location retrieval
    } else {
        alert("❌ Geolocation is not supported by your browser.");
    }
});
