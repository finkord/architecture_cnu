const API_BASE = 'http://localhost:8000';
const USER_ID = 'user_123';

// DOM Elements
const paymentForm = document.getElementById('payment-form');
const payBtn = document.getElementById('pay-btn');
const btnText = document.querySelector('.btn-text');
const loader = document.querySelector('.loader');
const alertBox = document.getElementById('payment-alert');
const historyBody = document.getElementById('history-body');
const refreshBtn = document.getElementById('refresh-btn');
const emptyState = document.getElementById('empty-history');

// Generate UUID v4 for Idempotency Key
function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

// Show Alert
function showAlert(message, type) {
    alertBox.textContent = message;
    alertBox.className = `alert ${type}`;
    alertBox.classList.remove('hidden');
    
    setTimeout(() => {
        alertBox.classList.add('hidden');
    }, 5000);
}

// Fetch and render history
async function fetchHistory() {
    try {
        const response = await fetch(`${API_BASE}/payments/history?user_id=${USER_ID}`);
        if (!response.ok) throw new Error('Failed to fetch history');
        
        const data = await response.json();
        renderHistory(data);
    } catch (error) {
        console.error('Error fetching history:', error);
    }
}

// Render history table
function renderHistory(historyData) {
    historyBody.innerHTML = '';
    
    if (historyData.length === 0) {
        emptyState.classList.remove('hidden');
        return;
    }
    
    emptyState.classList.add('hidden');
    
    historyData.forEach(item => {
        const tr = document.createElement('tr');
        
        const date = new Date(item.payment.created_at).toLocaleDateString(undefined, { 
            month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit' 
        });
        
        const amount = `${item.payment.amount.toFixed(2)} ${item.payment.currency}`;
        const card = item.payment_method?.maskedCard || '••••';
        const status = item.payment.status;
        
        tr.innerHTML = `
            <td>${date}</td>
            <td>${item.payment.course_id}</td>
            <td>${amount}</td>
            <td style="font-family: monospace;">${card}</td>
            <td><span class="status-badge status-${status}">${status}</span></td>
        `;
        
        historyBody.appendChild(tr);
    });
}

// Submit Payment
paymentForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Set loading state
    payBtn.disabled = true;
    btnText.classList.add('hidden');
    loader.classList.remove('hidden');
    
    const payload = {
        user_id: USER_ID,
        course_id: document.getElementById('course-id').value,
        amount: parseFloat(document.getElementById('amount').value),
        currency: document.getElementById('currency').value,
        payment_method_id: document.getElementById('payment-method').value
    };
    
    const idempotencyKey = uuidv4();
    
    try {
        const response = await fetch(`${API_BASE}/payments/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Idempotency-Key': idempotencyKey
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (response.ok || response.status === 201) {
            showAlert(`Payment successful! ID: ${data.id.substring(0,8)}...`, 'success');
        } else if (response.status === 402) {
            showAlert(`Payment declined: ${data.detail.message || 'Insufficient funds'}`, 'error');
        } else {
            showAlert(data.detail || 'Payment processing error', 'error');
        }
        
        // Refresh history immediately
        fetchHistory();
        
    } catch (error) {
        showAlert('Network error or server unreachable', 'error');
        console.error(error);
    } finally {
        // Reset loading state
        payBtn.disabled = false;
        btnText.classList.remove('hidden');
        loader.classList.add('hidden');
    }
});

// Refresh button listener
refreshBtn.addEventListener('click', () => {
    refreshBtn.style.transform = 'rotate(180deg)';
    setTimeout(() => refreshBtn.style.transform = 'none', 300);
    fetchHistory();
});

// Initial load
fetchHistory();
