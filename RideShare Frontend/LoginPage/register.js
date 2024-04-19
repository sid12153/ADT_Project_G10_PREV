document.getElementById('registration-form').onsubmit = function(event) {
    event.preventDefault();
    alert('Registration Complete!');
};

// Initialize the form by hiding all sections except the first
document.querySelectorAll('.form-section').forEach(function(section, index) {
    if (index !== 0) section.style.display = 'none';
});

// Add event listeners for 'Continue' buttons
document.querySelectorAll('.continue-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
        // Logic to show next section
        var nextSection = this.dataset.nextSection;
        if (nextSection) {
            showNext(nextSection);
        }
    });
});

// Arrays for US states and specified countries
const usStates = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
];
const countries = ["USA", "UK", "India", "UAE"];

// Function to add options to select dropdown
function addOptions(selectId, optionsArray) {
    const select = document.getElementById(selectId);
    // Ensure the select element exists
    if (select) {
        optionsArray.forEach(option => {
            let optionElement = document.createElement("option");
            optionElement.value = option;
            optionElement.textContent = option;
            select.appendChild(optionElement);
        });
    }
}

// Populate dropdowns on window load
window.onload = function() {
    addOptions("issuing-country", countries);
    addOptions("issuing-authority", usStates);
};

function showNext(sectionId) {
    var currentSection = document.querySelector('.form-section:not([style*="display: none"])');
    var inputs = currentSection.querySelectorAll('input, select');
    for (var input of inputs) {
        if (!input.checkValidity()) {
            alert('Please fill out all required fields.');
            return;
        }
        if (input.type === "email" && input.id === "confirm-email" && input.value !== document.getElementById('email').value) {
            alert('Emails do not match.');
            return;
        }
        if (input.type === "password" && input.id === "confirm-password" && input.value !== document.getElementById('password').value) {
            alert('Passwords do not match.');
            return;
        }
    }

    // If the current section is valid, hide it and show the next one
    currentSection.style.display = 'none';
    var nextSection = document.getElementById(sectionId);
    if (nextSection) {
        nextSection.style.display = 'block';
    } else {
        alert('Next section not found.');
    }
}
