document.getElementById('login-form').onsubmit = function(event) {
    event.preventDefault(); // Prevent the form from submitting via the browser
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    console.log('Logging in as client:', username, password);
    // Implement your login logic here
};

function loginAsOwner() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    console.log('Logging in as owner:', username, password);
    // Implement your owner login logic here
}

function registerNewUser() {
    console.log('Redirecting to registration page...');
    // Redirect to registration page logic
}
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
