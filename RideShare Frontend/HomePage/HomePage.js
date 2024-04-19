// Assuming you already have login.js which handles login validation
// Redirect to home page upon successful login
function redirectToHome() {
    // Simulate a login check
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === 'qwerty' && password === '12345678') {
        // Replace 'location.href' with the path to your HomePage.html
        window.location.href = 'HomePage.html';
    } else {
        alert('Invalid credentials, please try again.');
    }
}

// Call this function when the login form is submitted
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    redirectToHome();
});

document.addEventListener('DOMContentLoaded', (event) => {
    // This function will handle the login validation
    function validateLogin(username, password) {
        if (username === 'qwerty' && password === '12345678') {
            window.location.href = 'HomePage.html'; // Redirect to the home page
        } else {
            alert('Invalid username or password');
        }
    }

    // Assuming you have input fields for username and password and a button to login
    const loginButton = document.getElementById('login-button');
    if (loginButton) {
        loginButton.addEventListener('click', () => {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            validateLogin(username, password);
        });
    }
});

