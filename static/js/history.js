document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const loadingHistory = document.getElementById('loadingHistory');
    const emptyHistory = document.getElementById('emptyHistory');
    const historyTable = document.getElementById('historyTable');
    const historyTableBody = document.getElementById('historyTableBody');
    const errorHistory = document.getElementById('errorHistory');
    const errorHistoryMessage = document.getElementById('errorHistoryMessage');
    const refreshHistoryBtn = document.getElementById('refreshHistoryBtn');
    
    // Record detail modal elements
    const recordModalLoading = document.getElementById('recordModalLoading');
    const recordModalContent = document.getElementById('recordModalContent');
    const modalDate = document.getElementById('modalDate');
    const modalSymptoms = document.getElementById('modalSymptoms');
    const modalDiagnosis = document.getElementById('modalDiagnosis');
    const modalRecommendations = document.getElementById('modalRecommendations');
    const modalFallbackContainer = document.getElementById('modalFallbackContainer');
    
    // Modal instance
    const recordDetailModal = new bootstrap.Modal(document.getElementById('recordDetailModal'));
    
    // Event listeners
    refreshHistoryBtn.addEventListener('click', fetchHistory);
    
    // Fetch history on load
    fetchHistory();
    
    // Function to fetch history from the API
    function fetchHistory() {
        // Reset view state
        showHistoryLoading();
        
        fetch('/api/history')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.history && data.history.length > 0) {
                    displayHistory(data.history);
                } else {
                    showEmptyHistory();
                }
            })
            .catch(error => {
                console.error('Error fetching history:', error);
                showHistoryError(error.message || 'Failed to load headache history.');
            });
    }
    
    // Function to display history data
    function displayHistory(history) {
        // Clear existing table rows
        historyTableBody.innerHTML = '';
        
        // Add each record to the table
        history.forEach(record => {
            const row = document.createElement('tr');
            
            // Format date
            const date = new Date(record.created_at);
            const formattedDate = date.toLocaleString();
            
            // Truncate symptoms text if too long
            const symptomsPreview = record.symptoms.length > 50 
                ? record.symptoms.substring(0, 50) + '...' 
                : record.symptoms;
            
            // Add fallback indicator if needed
            const fallbackIndicator = record.used_fallback 
                ? '<span class="badge bg-warning text-dark ms-2"><i class="fas fa-exclamation-triangle me-1"></i> Fallback</span>' 
                : '';
            
            // Add diagnosis preview
            const diagnosisPreview = record.diagnosis.length > 100
                ? record.diagnosis.substring(0, 100) + '...'
                : record.diagnosis;
            
            row.innerHTML = `
                <td>${formattedDate}</td>
                <td>${symptomsPreview}</td>
                <td>
                    ${diagnosisPreview}
                    ${fallbackIndicator}
                </td>
                <td>
                    <button class="btn btn-sm btn-primary view-details" data-record-id="${record.id}">
                        <i class="fas fa-eye me-1"></i> View
                    </button>
                </td>
            `;
            
            // Add event listener to view button
            row.querySelector('.view-details').addEventListener('click', () => {
                showRecordDetails(record);
            });
            
            historyTableBody.appendChild(row);
        });
        
        // Show the history table
        loadingHistory.classList.add('d-none');
        emptyHistory.classList.add('d-none');
        errorHistory.classList.add('d-none');
        historyTable.classList.remove('d-none');
    }
    
    // Function to show record details in modal
    function showRecordDetails(record) {
        // Reset modal state
        recordModalLoading.classList.remove('d-none');
        recordModalContent.classList.add('d-none');
        
        // Show record details
        setTimeout(() => {
            // Format date
            const date = new Date(record.created_at);
            modalDate.textContent = date.toLocaleString();
            
            // Set symptoms and diagnosis
            modalSymptoms.textContent = record.symptoms;
            modalDiagnosis.textContent = record.diagnosis;
            
            // Show/hide fallback indicator
            if (record.used_fallback) {
                modalFallbackContainer.classList.remove('d-none');
            } else {
                modalFallbackContainer.classList.add('d-none');
            }
            
            // Add recommendations
            modalRecommendations.innerHTML = '';
            if (Array.isArray(record.recommendations)) {
                record.recommendations.forEach(recommendation => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item';
                    li.textContent = recommendation;
                    modalRecommendations.appendChild(li);
                });
            }
            
            // Show content
            recordModalLoading.classList.add('d-none');
            recordModalContent.classList.remove('d-none');
        }, 500); // Short delay for UX
        
        // Show the modal
        recordDetailModal.show();
    }
    
    // Function to show loading state
    function showHistoryLoading() {
        loadingHistory.classList.remove('d-none');
        emptyHistory.classList.add('d-none');
        historyTable.classList.add('d-none');
        errorHistory.classList.add('d-none');
    }
    
    // Function to show empty history state
    function showEmptyHistory() {
        loadingHistory.classList.add('d-none');
        emptyHistory.classList.remove('d-none');
        historyTable.classList.add('d-none');
        errorHistory.classList.add('d-none');
    }
    
    // Function to show error state
    function showHistoryError(message) {
        loadingHistory.classList.add('d-none');
        emptyHistory.classList.add('d-none');
        historyTable.classList.add('d-none');
        errorHistory.classList.remove('d-none');
        errorHistoryMessage.textContent = message;
    }
});