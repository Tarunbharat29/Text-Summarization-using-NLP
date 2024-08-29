function summarizeText() {
    const text = document.getElementById('input-text').value;
    fetch('/summarize', {
        method: 'POST',
        body: new URLSearchParams(`text=${text}`),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('summary-output').innerText = data.summary;
    })
    .catch(error => console.error('Error:', error));
}

