document.addEventListener('DOMContentLoaded', () => {
    
    // Highlight selected options in the quiz
    const optionLabels = document.querySelectorAll('.option-label');
    
    optionLabels.forEach(label => {
        const input = label.querySelector('input');
        if (!input) return;
        
        // Listen for changes
        input.addEventListener('change', (e) => {
            const name = e.target.name;
            const isRadio = e.target.type === 'radio';
            
            if (isRadio) {
                // Remove 'selected' class from all labels in this group
                document.querySelectorAll(`input[name="${name}"]`).forEach(r => {
                    r.closest('.option-label').classList.remove('selected');
                });
            }
            
            // Toggle 'selected' class
            if (e.target.checked) {
                label.classList.add('selected');
            } else {
                label.classList.remove('selected');
            }
        });
    });

    // Simple form submission animation
    const quizForm = document.getElementById('quizForm');
    const submitBtn = document.getElementById('submitBtn');

    if (quizForm && submitBtn) {
        quizForm.addEventListener('submit', (e) => {
            // Prevent double submissions visually
            submitBtn.innerHTML = '<span style="display:inline-block; animation: pulse 1s infinite;">Submitting...</span>';
            submitBtn.style.opacity = '0.8';
            submitBtn.style.pointerEvents = 'none';
        });
    }

    // Timer Logic
    const timerCard = document.getElementById('timerCard');
    const timeDisplay = document.getElementById('timeDisplay');
    
    if (timerCard && timeDisplay) {
        let timeRemaining = parseInt(timerCard.getAttribute('data-time'), 10);
        
        const updateTimer = () => {
            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                timeDisplay.textContent = "00:00";
                if (quizForm) {
                    quizForm.submit(); // Auto-submit when time is up
                }
                return;
            }
            
            const minutes = Math.floor(timeRemaining / 60);
            const seconds = timeRemaining % 60;
            timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            timeRemaining--;
        };
        
        updateTimer(); // Initial call
        const timerInterval = setInterval(updateTimer, 1000);
    }

    // Flash Message Auto-dismiss (Toast Notifications)
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach((msg, index) => {
        setTimeout(() => {
            msg.classList.add('fade-out');
            setTimeout(() => {
                msg.remove();
            }, 500); // Wait for CSS transition
        }, 3000 + (index * 500)); // Stagger dismissal
    });
});
