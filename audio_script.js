const btn = document.getElementById('submitBtn');
const fileInput = document.getElementById('audioFile');
const langSelect = document.getElementById('langSelect');
const loader = document.getElementById('loader');
const resultBox = document.getElementById('resultBox');
const output = document.getElementById('output');

btn.addEventListener('click', async () => {
    if (fileInput.files.length === 0) {
        alert('Please choose an audio file first.');
        return;
    }

    const formData = new FormData();
    formData.append('audio', fileInput.files[0]);
    formData.append('language', langSelect.value);

    loader.classList.remove('hidden');
    resultBox.classList.add('hidden');

    try {
        const res = await fetch('http://127.0.0.1:5001/process_audio', {
            method: 'POST',
            body: formData
        });

        const data = await res.json();
        
        if (res.ok) {
            output.innerHTML = data.analysis;
            resultBox.classList.remove('hidden');
        } else {
            alert(data.error || 'Something went wrong.');
        }
    } catch (err) {
        alert('Could not connect to the backend server.');
    } finally {
        loader.classList.add('hidden');
    }
});