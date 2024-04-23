import streamlit as st
import requests
import datetime
import json
from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page
from PIL import Image

# def set_title_color(color):
#     st.markdown(
#         f'<h1 style="color:{color};">CityLink Rideshare Hub</h1>', 
#         unsafe_allow_html=True
#     )

# # Set the title color
# set_title_color('#0a9396')

# Set page config to wide layout
# st.set_page_config(layout="wide")
# # Set the background image
# bg_img = '''
# <style>
# [data-testid="stAppViewContainer"] {
# background-image: url('https://images.unsplash.com/photo-1528459801416-a9e53bbf4e17');
# background-size: cover;
# background-repeat: no-repeat;
# }
# </style>
# '''
# st.markdown(bg_img, unsafe_allow_html=True)

# URL of your FastAPI application
API_URL = "http://127.0.0.1:8000"

# def load_lottiefile(filepath: str):
#    with open(filepath, "r") as file:
#        return json.load(file)

# Assuming your Lottie animation JSON file is named 'animation.json'
# lottie_animation = load_lottiefile("Animation - 1713738452764.json")

# def display_ride_block(ride):
#     # Calculate duration
#     duration = datetime.datetime.strptime(ride['Arrival Time'], '%H:%M:%S') - datetime.datetime.strptime(ride['Departure Time'], '%H:%M:%S')

#     # Create the layout for ride information
#     col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
#     with col1:
#         st.write(ride['Vehicle Type'])  # Placeholder for the bus icon
#         st.write(ride['Departure Time'])
    
#     with col2:
#         st.write(f"{duration} hrs")  # Duration placeholder
    
#     with col3:
#         st.write(f"From {ride['Departure City']} to {ride['Arrival City']}")
    
#     with col4:
#         st.write(f"${ride['Price']}")  # Price placeholder
    
#     with col5:
#         if st.button("Edit", key=f"edit_{ride['ride_id']}"):
#             # Functionality to edit the ride goes here
#             pass
#         if st.button("Close", key=f"close_{ride['ride_id']}"):
#             # Functionality to close the ride goes here
#             pass


# Initialize session state for user and role management
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = ''
if 'role' not in st.session_state:
    st.session_state['role'] = None

if 'add_form_submitted' not in st.session_state:
    st.session_state.add_form_submitted = False

def add_form_submitted():
    st.session_state.add_form_submitted = True
def add_form_reset():
    st.session_state.add_form_submitted = False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = ''
    st.session_state['role'] = None
    st.rerun()

def get_cities():
    response = requests.get(f"{API_URL}/get_cities")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch cities.")
        return []

def get_currencies():
    response = requests.get(f"{API_URL}/get_currencies")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch currencies.")
        return []

# APIs for riders page
def fetch_bookings(user_id):
    response = requests.post(f"{API_URL}/reservations", json={"user_id": user_id})
    if response.ok:
        bookings = response.json()
        print("Fetched bookings:", bookings)  # Debugging line to see what is returned
        return bookings
    else:
        st.error("Failed to fetch bookings. Server responded with an error.")
        return []

def add_ride(ride_details):
    response = requests.post(f"{API_URL}/add_ride", json=ride_details)
    try:
        response_data = response.json()
        return response_data
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        st.error("Failed to decode JSON from response.")
        return None

def update_ride(ride_update_data):
    try:
        response = requests.put(f"{API_URL}/update_rides", json=ride_update_data)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("status") == "Success":
                return response_data
            else:
                st.error(f"Failed to update ride: {response_data.get('message')}")
        else:
            st.error(f"Failed to update ride. Server responded with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to update ride due to a network error: {str(e)}")
    return None



def close_ride(ride_id):
    response = requests.put(f"{API_URL}/close_ride", json={"ride_id": ride_id, "active": False})
    return response.json()

def get_ride_details(ride_id):
    response = requests.post(f"{API_URL}/get_ride_details", json={"ride_id": ride_id})
    return response.json()

# APIs for passengers page
def fetch_available_rides(filters):
    response = requests.post(f"{API_URL}/fetch_passenger_rides", json=filters)
    return response.json()

def book_ride(booking_details):
    response = requests.post(f"{API_URL}/reserve_rides", json=booking_details)
    return response.json()

def fetch_bookings(user_id):
    response = requests.post(f"{API_URL}/reservations", json={"user_id": user_id})
    return response.json()

# Home page functionalities
def login_user(user_id, user_password):
    response = requests.post(f"{API_URL}/login_check", json={
        "user_id": user_id,
        "user_password": user_password
    })
    return response.json()

def register_user(user_id, first_name, last_name, email_id, contact, user_password):
    response = requests.post(f"{API_URL}/register_user", json={
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "email_id": email_id,
        "contact": contact,
        "user_password": user_password
    })
    return response.json()

def reset_password(user_id, new_password):
    response = requests.put(f"{API_URL}/forgot_password", json={
        "user_id": user_id,
        "new_password": new_password
    })
    return response.json()

# Role selection in sidebar
def select_role():
    if st.session_state['logged_in']:
        roles = ["Select a role", "Rider", "Passenger"]
        choice = st.sidebar.selectbox("Select your role", roles, index=roles.index(st.session_state['role']) if st.session_state['role'] else 0)
        if choice != "Select a role" and choice != st.session_state['role']:
            st.session_state['role'] = choice
            st.rerun()

# Displaying appropriate dashboard based on role
def show_dashboard():
    if st.session_state['role'] == "Rider":
        show_rider_dashboard()
    elif st.session_state['role'] == "Passenger":
        show_passenger_dashboard()

if 'show_add_ride_form' not in st.session_state:
    st.session_state.show_add_ride_form = False

def toggle_add_ride_form():
    st.session_state.show_add_ride_form = not st.session_state.show_add_ride_form

if 'update_ride_data' not in st.session_state:
    st.session_state.update_ride_data = None
    st.session_state.show_update_form = False

def toggle_update_ride_form(ride_id=None):
    if ride_id is not None:
        ride_details_response = get_ride_details(ride_id)
        if ride_details_response:
            st.session_state.update_ride_data = ride_details_response[0]  # Assuming the response includes the ride details
            st.session_state.show_update_form = True
            st.session_state.current_ride_id = ride_id
        else:
            st.error("Failed to fetch ride details.")
    else:
        st.session_state.show_update_form = not st.session_state.show_update_form
        st.session_state.update_ride_data = None
        st.session_state.current_ride_id = None

def show_rider_dashboard():
    st.title(f"Rider Dashboard")

    # Button to toggle adding a ride
    if st.button("Add New Ride"):
        toggle_add_ride_form()

    if st.session_state.show_add_ride_form:
        cities = get_cities()  # Assuming this function fetches cities properly
        currencies = get_currencies()  # Assuming a similar function exists for currencies
        
        with st.form("add_ride_form"):
            departure_city = st.selectbox("Departure City", options=cities)
            arrival_city = st.selectbox("Arrival City", options=cities)
            departure_date = st.date_input("Departure Date")
            departure_time = st.time_input("Departure Time")
            arrival_date = st.date_input("Arrival Date")
            arrival_time = st.time_input("Arrival Time")
            vehicle_type = st.text_input("Vehicle Type")
            vehicle_number = st.text_input("Vehicle Number")
            pickup_loc = st.text_input("Pickup Location")
            dropoff_loc = st.text_input("Dropoff Location")
            available_seats = st.number_input("Available Seats", min_value=1)
            price = st.number_input("Price", min_value=0.0, format="%.2f")
            currency = st.selectbox("Currency", options=['USD', 'EUR', 'GBP'])  # Example currencies
            special_amenities = st.text_input("Special Amenities")

            submit_button = st.form_submit_button("Submit Ride Details")
            if submit_button:
                ride_details = {
                    "user_id": st.session_state['user_id'],  # This should be fetched from the session or a logged-in user
                    "departure_city": departure_city,
                    "arrival_city": arrival_city,
                    "departure_date": departure_date.strftime("%Y-%m-%d"),
                    "departure_time": departure_time.strftime("%H:%M:%S"),
                    "arrival_date": arrival_date.strftime("%Y-%m-%d"),
                    "arrival_time": arrival_time.strftime("%H:%M:%S"),
                    "vehicle_type": vehicle_type,
                    "vehicle_number": vehicle_number,
                    "pickup_loc": pickup_loc,
                    "dropoff_loc": dropoff_loc,
                    "available_seats": available_seats,
                    "price": price,
                    "currency": currency,
                    "special_amenities": special_amenities
                }
                response = add_ride(ride_details)
                if response.get("status") == "Success":
                    st.success("Ride added successfully!")
                    toggle_add_ride_form()  # Hide form after submission
                else:
                    st.error("Failed to add ride.")                
                
                add_form_reset()

    # Display existing rides
    # rides = fetch_rides(st.session_state['user_id'])
    # for ride in rides:
    #     st.subheader(f"Ride from {ride['departure_city']} to {ride['arrival_city']} on {ride['departure_date']}")
    #     if st.button(f"Close Ride {ride['ride_id']}", key=f"close{ride['ride_id']}"):
    #         close_ride(ride['ride_id'])
    #         st.success("Ride closed successfully.")
     # Display existing rides and options for each ride
    rides = fetch_rides(st.session_state['user_id'])
    if rides:
        for ride in rides:
            ride_info = f"Ride ID: {ride['Ride ID']} - From {ride['Departure City']} to {ride['Arrival City']} on {ride['Departure Date']}"
            with st.expander(ride_info):
                st.write(f"Departure Time: {ride['Departure Time']}")
                st.write(f"Arrival Time: {ride['Arrival Time']}")
                st.write(f"Vehicle Type: {ride['Vehicle Type']}")
                st.write(f"Available Seats: {ride['Available Seats']}")
                st.write(f"Price: ${ride['Price']}")
                if st.button(f"Close Ride {ride['Ride ID']}", key=f"close{ride['Ride ID']}"):
                    close_ride(ride['Ride ID'])
                    st.success("Ride closed successfully.")
                if st.button(f"Update Ride {ride['Ride ID']}", key=f"update{ride['Ride ID']}"):
                    toggle_update_ride_form(ride['Ride ID'])
    else:
        st.write("No rides yet. Add one!")
    
    if st.session_state.show_update_form:
        update_ride_form()


def update_ride_form():
    cities = get_cities()  # Fetch the list of cities again
    currency_list = get_currencies()  # Fetch the list of currencies if needed

    with st.form("update_ride_form"):
        ride_details = st.session_state.update_ride_data

        # Use selectbox for city inputs
        departure_city = st.selectbox("Departure City", options=cities, index=cities.index(ride_details['Departure City']) if ride_details['Departure City'] in cities else 0)
        arrival_city = st.selectbox("Arrival City", options=cities, index=cities.index(ride_details['Arrival City']) if ride_details['Arrival City'] in cities else 0)
        
        departure_date = st.date_input("Departure Date", value=datetime.datetime.strptime(ride_details['Departure Date'], "%Y-%m-%d"))
        departure_time = st.time_input("Departure Time", value=datetime.datetime.strptime(ride_details['Departure Time'], "%H:%M:%S"))
        arrival_date = st.date_input("Arrival Date", value=datetime.datetime.strptime(ride_details['Arrival Date'], "%Y-%m-%d"))
        arrival_time = st.time_input("Arrival Time", value=datetime.datetime.strptime(ride_details['Arrival Time'], "%H:%M:%S"))
        vehicle_type = st.text_input("Vehicle Type", value=ride_details['Vehicle Type'])
        vehicle_number = st.text_input("Vehicle Number", value=ride_details['Vehicle Number'])
        pickup_loc = st.text_input("Pickup Location", value=ride_details['Pickup Location'])
        dropoff_loc = st.text_input("Dropoff Location", value=ride_details['Dropoff Location'])
        available_seats = st.number_input("Available Seats", min_value=1, value=int(ride_details['Available Seats']))
        price = st.number_input("Price", min_value=0.0, format="%.2f", value=float(ride_details['Price']))
        currency = st.selectbox("Currency", options=currency_list, index=currency_list.index(ride_details['Currency']) if ride_details['Currency'] in currency_list else 0)
        special_amenities = st.text_input("Special Amenities", value=ride_details['Special Amenities'])

        submit_button = st.form_submit_button("Submit Updated Details")
        if submit_button:
            ride_update_data = {
                "ride_id": st.session_state.current_ride_id,
                "departure_city": departure_city,
                "arrival_city": arrival_city,
                "departure_date": departure_date.strftime("%Y-%m-%d"),
                "departure_time": departure_time.strftime("%H:%M:%S"),
                "arrival_date": arrival_date.strftime("%Y-%m-%d"),
                "arrival_time": arrival_time.strftime("%H:%M:%S"),
                "vehicle_type": vehicle_type,
                "vehicle_number": vehicle_number,
                "pickup_loc": pickup_loc,
                "dropoff_loc": dropoff_loc,
                "available_seats": available_seats,
                "price": price,
                "currency": currency,
                "special_amenities": special_amenities
            }
            update_response = update_ride(ride_update_data)
            
            if update_response and update_response.get("status") == "Success":
                st.success("Ride updated successfully!")
                st.session_state.show_update_form = False  # Close the form after successful update
            else:
                error_message = update_response.get("message", "Unknown error occurred") if update_response else "Failed to get a valid response from server"
                st.error(f"Failed to update ride: {error_message}")

def show_passenger_dashboard():
    cities = get_cities()
    st.title("Passenger Dashboard")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        departure_city = st.selectbox("Departure City", cities)
    with col2:
        arrival_city = st.selectbox("Arrival City", cities)
    with col3:
        departure_date = st.date_input("Departure Date")
    with col4:
        available_seats = st.number_input("Seats To Reserve", min_value=1)

    if st.button("Search Rides"):
        filters = {
            "departure_city": departure_city,
            "arrival_city": arrival_city,
            "departure_date": departure_date.strftime("%Y-%m-%d"),
            "available_seats": available_seats
        }
        rides = fetch_available_rides(filters)
        if not rides:
            st.write("No rides available.")
        else:
            for ride in rides:
                ride_info = f"Ride ID: {ride['Ride ID']} - From {ride['Departure City']} to {ride['Arrival City']} on {ride['Departure Date']}"
                with st.expander(ride_info):
                    st.write(f"Departure Time: {ride['Departure Time']}")
                    st.write(f"Arrival Time: {ride['Arrival Time']}")
                    st.write(f"Vehicle Type: {ride['Vehicle Type']}")
                    st.write(f"Available Seats: {ride['Available Seats']}")
                    st.write(f"Price: ${ride['Price']}")
                    if st.button("Book Ride", key=f"book{ride['Ride ID']}"):
                        st.session_state['booking_ride_id'] = ride['Ride ID']
                        st.session_state['booking_ride_details'] = ride

    if 'booking_ride_id' in st.session_state:
        st.write("### Book Your Ride")
        with st.form(f"book_ride_form_{st.session_state['booking_ride_id']}"):
            st.write(f"Booking Ride ID: {st.session_state['booking_ride_id']}")
            to_reserve_seats = st.number_input("Number of seats to reserve", min_value=1, max_value=st.session_state['booking_ride_details']['Available Seats'])
            if st.form_submit_button("Complete Reservation"):
                booking_details = {
                    "ride_id": st.session_state['booking_ride_id'],
                    "passenger_id": st.session_state['user_id'],
                    "number_of_seats_reserved": to_reserve_seats,
                    "price": st.session_state['booking_ride_details']['Price']
                }
                book_response = book_ride(booking_details)
                if book_response.get("status") == "Success":
                    st.success("Ride booked successfully.")
                else:
                    st.error(f"Booking failed: {book_response.get('message', 'Unknown error')}")
                del st.session_state['booking_ride_id']  # Clean up session state after booking

    if st.button("View My Bookings"):
        bookings = fetch_bookings(st.session_state['user_id'])
        if not bookings:
            st.write("No Bookings Yet.")
        else:
            for booking in bookings:
                booking_info = f"Booking ID {booking['Booking ID']} - {booking['Seats Reserved']} seats on {booking['Booking Date']}"
                with st.expander(booking_info):
                    st.write(f"Departure Date: {booking['Departure Date']}, Time: {booking['Departure Time']}")
                    st.write(f"Pickup Location: {booking['Pickup Location']}")
                    st.write(f"Dropoff Location: {booking['Dropoff Location']}")
                    st.write(f"Billed Amount: {booking['Billed Amount']}")
                    st.write(f"Payment Status: {booking['Payment Status']}")



# User management pages
def show_login_page():
    st.title('CityLink Rideshare Hub')
    col1, col2 = st.columns([1, 1])
    with col1:
        st.text("Hello")
        # st_lottie(lottie_animation, height=300, key="animation",)  # Set the height as needed
    with col2:
        user_id = st.text_input("User ID")
        user_password = st.text_input("Password", type="password")
        if st.button("Login"):
            response = login_user(user_id, user_password)
            if response.get("status") == "Success":
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user_id
                st.session_state['role'] = "Select a role"
                st.sidebar.success("Logged in successfully.")
                st.rerun()
            else:
                st.error(response.get("message"))

def show_registration_page():
    st.title("CityLink Rideshare Hub")
    col1, col2 = st.columns([1, 1])
    with col1:
        st_lottie(lottie_animation, height=300, key="animation",)  # Set the height as needed
    with col2:
        user_id = st.text_input("User ID")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email_id = st.text_input("Email")
        contact = st.text_input("Contact")
        user_password = st.text_input("Password", type="password")
        if st.button("Register"):
            response = register_user(user_id, first_name, last_name, email_id, contact, user_password)
            if response.get("status") == "Success":
                st.success("Registered successfully. Please login.")
            else:
                st.error(response.get("message"))

def show_forgot_password_page():
    st.title("CityLink Rideshare Hub")
    col1, col2 = st.columns([1, 1])
    with col1:
        st_lottie(lottie_animation, height=300, key="animation",)  # Set the height as needed
    with col2:
        user_id = st.text_input("User ID")
        new_password = st.text_input("New Password", type="password")
        if st.button("Reset Password"):
            response = reset_password(user_id, new_password)
            if response.get("status") == "Success":
                st.success("Password reset successfully.")
            else:
                st.error(response.get("message"))

# Main application flow
if st.session_state['logged_in']:
    st.sidebar.success(f"Logged in as {st.session_state['user_id']}")
    select_role()
    show_dashboard()
    if st.sidebar.button("Logout"):
        logout()
else:
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a section", ["Login", "Sign Up", "Forgot Password"])
    # page = st.sidebar.radio("Navigation", ["Login", "Sign Up", "Forgot Password"])
    if page == "Login":
        show_login_page()
    elif page == "Sign Up":
        show_registration_page()
    elif page == "Forgot Password":
        show_forgot_password_page()
