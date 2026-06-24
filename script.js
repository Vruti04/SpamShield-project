document.addEventListener('DOMContentLoaded', () => {
    const detectBtn = document.getElementById('detect-btn');
    const clearBtn = document.getElementById('clear-btn');
    const emailText = document.getElementById('email-text');
    const resultSection = document.getElementById('result-section');
    const statusIcon = document.getElementById('status-icon');
    const statusTitle = document.getElementById('status-title');
    const statusDesc = document.getElementById('status-desc');
    const confidenceVal = document.getElementById('confidence-val');
    const meterFill = document.getElementById('meter-fill');

    detectBtn.addEventListener('click', async () => {
        const message = emailText.value.trim();

        if (!message) {
            alert('Please enter some text to analyze.');
            return;
        }

        // UI Loading state
        detectBtn.classList.add('loading');
        detectBtn.disabled = true;
        resultSection.classList.add('hidden');

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            showResult(data);
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to connect to the server. Make sure the Flask app is running.');
        } finally {
            detectBtn.classList.remove('loading');
            detectBtn.disabled = false;
        }
    });

    clearBtn.addEventListener('click', () => {
        emailText.value = '';
        resultSection.classList.add('hidden');
        emailText.focus();
    });

    function showResult(data) {
        resultSection.classList.remove('hidden');
        resultSection.classList.remove('spam', 'ham');
        
        const isSpam = data.is_spam;
        const confidence = data.confidence.toFixed(1);

        if (isSpam) {
            resultSection.classList.add('spam');
            statusIcon.innerText = '🚨';
            statusTitle.innerText = 'Spam Detected';
            statusDesc.innerText = 'This message shows high patterns of malicious or promotional spam.';
        } else {
            resultSection.classList.add('ham');
            statusIcon.innerText = '✅';
            statusTitle.innerText = 'Genuine Message';
            statusDesc.innerText = 'This message appears safe and professionally structured.';
        }

        confidenceVal.innerText = `${confidence}%`;
        
        // Trigger reflow for animation
        meterFill.style.width = '0%';
        setTimeout(() => {
            meterFill.style.width = `${confidence}%`;
        }, 50);

        // Scroll to result
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
