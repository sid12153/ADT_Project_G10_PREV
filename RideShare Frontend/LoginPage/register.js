document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting via the browser

    // Gather all data from form fields
    const formData = {
        user_id: document.getElementById('username').value, // Make sure to have a username field or similar
        first_name: document.getElementById('first-name').value,
        last_name: document.getElementById('last-name').value,
        email_id: document.getElementById('email').value,
        contact: document.getElementById('contact-number').value,
        user_password: document.getElementById('password').value
    };

    fetch('http://localhost:8000/register_user', { // Update this URL based on your FastAPI server address
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "Success") {
            console.log('Registration successful', data);
            window.location.href = '/path_to_success_page.html'; // Redirect user on success
        } else {
            alert('Registration failed: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});


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
