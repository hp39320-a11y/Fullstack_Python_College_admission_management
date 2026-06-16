document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registrationForm');
    const submitBtn = document.getElementById('submitBtn');
    const toastContainer = document.getElementById('toastContainer');

    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icon = type === 'success' ? '✓' : '✕';

        toast.innerHTML = `
            <span class="toast-icon">${icon}</span>
            <span class="toast-message">${message}</span>
        `;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(20px)';
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    }

    form.addEventListener('submit', () => {
        // ❌ DO NOT use preventDefault()

        // UI loading effect only
        if (submitBtn) {
            submitBtn.classList.add('loading');
        }

        showToast('Submitting registration...', 'success');
    });
});
document.addEventListener("DOMContentLoaded", function () {
    let steps = document.querySelectorAll(".form-step");
    let stepIndicators = document.querySelectorAll(".step");
    let nextBtns = document.querySelectorAll(".next");
    let prevBtns = document.querySelectorAll(".prev");
    let currentStep = 0;

    function showStep(index) {
        steps.forEach((step, i) => {
            step.classList.remove("active");
            if (i === index) {
                step.classList.add("active");
            }
        });
        stepIndicators.forEach((indicator, i) => {
            indicator.classList.remove("active");
            if (i <= index) {
                indicator.classList.add("active");
            }
        });
    }

    nextBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentStep < steps.length - 1) {
                currentStep++;
                showStep(currentStep);
            }
        });
    });

    prevBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentStep > 0) {
                currentStep--;
                showStep(currentStep);
            }
        });
    });

    showStep(currentStep);
});