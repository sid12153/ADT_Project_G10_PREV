document.addEventListener('DOMContentLoaded', function() {
    // Function to populate select dropdown
    function populateSelect(selectId, options) {
        const select = document.getElementById(selectId);
        select.innerHTML = ''; // Clear previous options
        options.forEach(option => {
            let opt = document.createElement('option');
            opt.value = option.city; // Assuming the API sends back objects with city property
            opt.innerHTML = `${option.city}, ${option.state}, ${option.country}`; // Display format
            select.appendChild(opt);
        });
    }

    // Fetch cities from the backend
    function fetchCities() {
        fetch('http://localhost:8000/get_cities', {  // Endpoint to fetch cities
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            populateSelect('departure-city', data.departureCities);
            populateSelect('arrival-city', data.arrivalCities);
        })
        .catch(error => console.error('Error fetching cities:', error));
    }

    // Function to handle form submission
    document.getElementById('search-ride-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const departureCity = document.getElementById('departure-city').value;
        const arrivalCity = document.getElementById('arrival-city').value;
        const date = document.getElementById('date').value;
        const seatsRequired = document.getElementById('seats-required').value;

        // Fetch rides based on user inputs
        fetch(`http://localhost:8000/search_rides?departureCity=${encodeURIComponent(departureCity)}&arrivalCity=${encodeURIComponent(arrivalCity)}&date=${date}&seatsRequired=${seatsRequired}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(rides => {
            displayRides(rides);
        })
        .catch(error => console.error('Error searching rides:', error));
    });

    // Function to display rides
    function displayRides(rides) {
        const ridesList = document.getElementById('rides-list');
        ridesList.innerHTML = ''; // Clear previous results

        if (rides.length === 0) {
            ridesList.innerHTML = '<p>No rides available for the selected criteria.</p>';
            return;
        }

        rides.forEach(ride => {
            const div = document.createElement('div');
            div.className = 'ride';
            div.innerHTML = `
                <h3>${ride.vehicle_type} from ${ride.departure_city} to ${ride.arrival_city}</h3>
                <p>Date: ${ride.departure_date}, Time: ${ride.departure_time} - ${ride.arrival_time}</p>
                <p>Seats Available: ${ride.available_seats}, Price: ${ride.price} ${ride.currency}</p>
                <p>Special Amenities: ${ride.special_amenities || 'None'}</p>
            `;
            ridesList.appendChild(div);
        });
    }

    fetchCities();  // Initial fetch of cities for dropdowns
});
