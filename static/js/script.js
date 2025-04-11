document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const symptomsInput = document.getElementById('symptomsInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsContainer = document.getElementById('resultsContainer');
    const diagnosisOutput = document.getElementById('diagnosisOutput');
    const recommendationsOutput = document.getElementById('recommendationsOutput');
    const emptyState = document.getElementById('emptyState');
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');

    // Event listeners
    analyzeBtn.addEventListener('click', analyzeSymptoms);

    // Function to analyze symptoms
    async function analyzeSymptoms() {
        const symptoms = symptomsInput.value.trim();
        
        // Validate input
        if (!symptoms) {
            showError('Please enter your symptoms before analyzing.');
            return;
        }

        // Show loading state
        showLoading();
        
        try {
            // Send symptoms to backend
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symptoms }),
            });

            // Check if response is ok
            if (!response.ok) {
                const errorData = await response.json();
                
                // If we have a fallback response, display it
                if (errorData && errorData.fallback_response) {
                    displayResults(errorData.fallback_response[0], errorData.fallback_response[1]);
                    showError('An error occurred with our AI service. Showing results from fallback system.');
                } else {
                    throw new Error(errorData.error || 'An error occurred while analyzing symptoms.');
                }
            } else {
                // Parse and display results
                const data = await response.json();
                displayResults(data.diagnosis, data.recommendations);
                hideError(); // Make sure any previous errors are hidden
            }
        } catch (error) {
            console.error('Error:', error);
            showError('An error occurred while communicating with the server. Please try again later.');
        } finally {
            hideLoading();
        }
    }

    // Function to display results
    function displayResults(diagnosis, recommendations) {
        // Update diagnosis
        diagnosisOutput.innerHTML = `<p>${diagnosis}</p>`;
        
        // Update recommendations
        let recommendationsHTML = '';
        if (Array.isArray(recommendations)) {
            recommendationsHTML = recommendations.map(rec => `<li>${rec}</li>`).join('');
        } else {
            recommendationsHTML = `<li>${recommendations}</li>`;
        }
        recommendationsOutput.innerHTML = recommendationsHTML;
        
        // Show results and hide empty state
        resultsContainer.classList.remove('d-none');
        emptyState.classList.add('d-none');
    }

    // Function to show loading indicator
    function showLoading() {
        loadingIndicator.classList.remove('d-none');
        resultsContainer.classList.add('d-none');
        emptyState.classList.add('d-none');
        analyzeBtn.disabled = true;
    }

    // Function to hide loading indicator
    function hideLoading() {
        loadingIndicator.classList.add('d-none');
        analyzeBtn.disabled = false;
    }

    // Function to show error message
    function showError(message) {
        errorMessage.textContent = message;
        errorContainer.classList.remove('d-none');
    }

    // Function to hide error message
    function hideError() {
        errorContainer.classList.add('d-none');
    }
});
