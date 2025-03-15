
// Speech-to-Text setup using Web Speech API
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US'; // Set language to English

// Event listener to start recording when the button is clicked
document.getElementById("startRecording").addEventListener("click", function() {
    recognition.start(); // Start the recognition process
});

// When speech is detected, send it to the backend
recognition.onresult = function(event) {
    const userQuestion = event.results[0][0].transcript; // Get recognized text
    document.getElementById("userQuestion").textContent = "You asked: " + userQuestion; // Display the question

    // Send the recognized question to the backend (Flask)
    fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "question": userQuestion })
    })
    .then(response => response.json())
    .then(data => {
        // Display the text answer
        document.getElementById("answer").textContent = data.answer;

        // Set the audio source to the path returned from the backend
        const audioElement = document.getElementById("audio");
        audioElement.src = data.audio_path;
        audioElement.load();  // Reload the audio element
        audioElement.play();  // Play the audio
    })
    .catch(error => {
        console.error("Error:", error);
    });
};

// Error handling for STT
recognition.onerror = function(event) {
    console.log("Error occurred in speech recognition: " + event.error);
};