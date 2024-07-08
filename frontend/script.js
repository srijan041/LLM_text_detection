function sendRequest() {
    const inputText = document.getElementById('textInput').value;

    // Make a POST request to the API
    fetch('https://qjtm4xkw-8000.inc1.devtunnels.ms/ai/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: inputText })
    })
    .then(response => response.json())
    .then(data => {
        // Display the value from the JSON response
        document.getElementById('ai_output').textContent = data.isAi;
        document.getElementById('percent_output').textContent = data.percentage
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
