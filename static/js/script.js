// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result-container');
    const salaryResult = document.getElementById('salary-result');
    const buttonText = document.getElementById('button-text');
    const loader = document.getElementById('loader');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Show loading state
        buttonText.style.display = 'none';
        loader.style.display = 'block';
        resultContainer.style.display = 'none';

        // Create a FormData object from the form
        const formData = new FormData(form);

        // Use the fetch API to send the data to the /predict endpoint
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Server error'); });
            }
            return response.json(); // Parse the JSON from the response
        })
        .then(data => {
            loader.style.display = 'none';
            buttonText.style.display = 'block';

            if (data.salary_prediction) {
                // Directly show the text result without currency formatting
                salaryResult.textContent = data.salary_prediction;
                resultContainer.style.display = 'block';
            } else if (data.error) {
                salaryResult.textContent = `Error: ${data.error}`;
                resultContainer.style.display = 'block';
            }
        })
        .catch(error => {
            loader.style.display = 'none';
            buttonText.style.display = 'block';
            salaryResult.textContent = `Error: ${error.message}`;
            resultContainer.style.display = 'block';
        });
    });
});
