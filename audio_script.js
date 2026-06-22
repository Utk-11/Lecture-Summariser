// Grab DOM elements exactly matching the HTML IDs
const audioInput = document.getElementById('audioFile');
const languageSelect = document.getElementById('langSelect');
const generateBtn = document.getElementById('submitBtn');
const outputDiv = document.getElementById('output');
const resultBox = document.getElementById('resultBox');

// Listen for a direct click on the "Generate Notes" button
generateBtn.addEventListener('click', async () => {
    
    // Quick validation check
    if (!audioInput.files || audioInput.files.length === 0) {
        alert('Please select an audio file first!');
        return;
    }

    const file = audioInput.files[0];
    const selectedLanguage = languageSelect.value;

    console.log("Selected file:", file.name);
    console.log("Selected language:", selectedLanguage);

    // Prepare data to send to Flask backend
    const formData = new FormData();
    formData.append('audio', file);
    formData.append('language', selectedLanguage);

    // Update UI state to loading
    generateBtn.disabled = true;
    generateBtn.innerText = 'Processing Lecture...';
    
    // Unhide the result box and show a loading message
    resultBox.classList.remove('hidden');
    outputDiv.innerHTML = '<p style="color: gray;">Analyzing audio and compiling notes. Please wait...</p>';

    try {
        console.log("Sending request to backend server...");
        
        // Fetching from our local Flask server running on port 5001
        const response = await fetch('http://127.0.0.1:5001/process_audio', {
            method: 'POST',
            body: formData
        });

        // Parse response JSON
        const data = await response.json();
        console.log("Received data from backend:", data);

        if (response.ok) {
            // Use Marked.js to parse the Markdown content returned by Gemini
            if (typeof marked !== 'undefined') {
                outputDiv.innerHTML = marked.parse(data.analysis);
                
                // Trigger KaTeX math rendering for engineering formulas
                if (typeof renderMathInElement === 'function') {
                    renderMathInElement(outputDiv, {
                        delimiters: [
                            {left: '$$', right: '$$', display: true},
                            {left: '$', right: '$', display: false}
                        ]
                    });
                }
            } else {
                // Fallback if marked library didn't load properly
                outputDiv.innerText = data.analysis;
            }
        } else {
            // Show error message from backend
            outputDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${data.error || 'Failed to process audio'}</p>`;
        }

    } catch (error) {
        console.error("Fetch error details:", error);
        outputDiv.innerHTML = '<p style="color: red;"><strong>Error:</strong> Could not connect to the backend server. Make sure your Python Flask script is running on port 5001!</p>';
    } finally {
        // Reset button state
        generateBtn.disabled = false;
        generateBtn.innerText = 'Generate Notes';
    }
});