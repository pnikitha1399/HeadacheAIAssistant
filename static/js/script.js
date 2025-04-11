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
            // Log the symptoms being sent to help with debugging
            console.log('Sending symptoms:', symptoms);
            
            // Send symptoms to backend
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symptoms }),
            });

            // Parse response data
            const data = await response.json();
            
            console.log('Response data:', data);
            
            // Check if using fallback (this comes from our API)
            if (data.using_fallback === true) {
                // Display fallback results
                displayResults(data.diagnosis, data.recommendations, true);
                showError(data.error || 'Using fallback analysis system.');
            } else if (!response.ok) {
                // General error from server but no fallback
                throw new Error(data.error || 'An error occurred while analyzing symptoms.');
            } else {
                // Display normal results
                displayResults(data.diagnosis, data.recommendations, false);
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
    function displayResults(diagnosis, recommendations, isFallback = false) {
        // Update diagnosis with a fallback indicator if needed
        if (isFallback) {
            diagnosisOutput.innerHTML = `
                <div class="alert alert-warning mb-2" role="alert">
                    <small><i class="fas fa-exclamation-triangle me-1"></i> Using simplified analysis (AI service unavailable)</small>
                </div>
                <p>${diagnosis}</p>
            `;
            diagnosisOutput.classList.add('border-warning', 'border-start');
        } else {
            diagnosisOutput.innerHTML = `<p>${diagnosis}</p>`;
            diagnosisOutput.classList.remove('border-warning', 'border-start');
        }
        
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
