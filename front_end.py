import streamlit as st
import requests
import json

# Configuration for the API server endpoint
API_BASE_URL = "http://127.0.0.1:6012"

def api_post(endpoint, data):
    response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data)
    return response

def api_put(endpoint, data):
    response = requests.put(f"{API_BASE_URL}/{endpoint}", json=data)
    return response

st.title('CityLink Rideshare Hub')

# User Authentication
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            login_response = api_post("login_check", {"user_id": username, "user_password": password})
            if login_response.status_code == 200:
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = username
                st.success("Logged in successfully")
            else:
                st.error("Login failed, please try again.")

    with st.expander("Not registered yet? Sign up here"):
        with st.form("signup_form", clear_on_submit=True):
            new_username = st.text_input("Choose User ID")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email_id = st.text_input("Email")
            contact = st.text_input("Contact")
            new_password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Sign up")
            
            if submit_button:
                signup_response = api_post("register_user", {
                    "user_id": new_username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email_id": email_id,
                    "contact": contact,
                    "user_password": new_password
                })
                if signup_response.status_code == 200:
                    st.success("Registered successfully")
                else:
                    st.error("Registration failed, please try again.")

if st.session_state['logged_in']:
    user_id = st.session_state['user_id']
    st.sidebar.success(f"Logged in as {user_id}")
    
    with st.sidebar:
        fetch_rides_button = st.button("Fetch My Rides")
        add_ride_button = st.button("Add a Ride")
        manage_reservations_button = st.button("My Reservations")
        finish_ride_button = st.button("Finish a Ride")
        reset_password_button = st.button("Reset Password")
        logout_button = st.button("Logout")

    if fetch_rides_button:
        # Implement functionality to fetch rides
        rides_response = api_post("fetch_rides", {"user_id": user_id})
        if rides_response.status_code == 200:
            rides_data = rides_response.json()
            st.write("My Rides:")
            st.dataframe(rides_data)
        else:
            st.error("Failed to fetch rides.")

    if add_ride_button:
        # Implement functionality to add a ride
        with st.form("add_ride_form"):
            departure_city = st.text_input("Departure City")
            arrival_city = st.text_input("Arrival City")
            currency = st.text_input("Currency")
            departure_date = st.date_input("Departure Date")
            departure_time = st.time_input("Departure Time")
            arrival_date = st.date_input("Arrival Date")
            arrival_time = st.time_input("Arrival Time")
            vehicle_type = st.text_input("Vehicle Type")
            vehicle_number = st.text_input("Vehicle Number")
            pickup_loc = st.text_input("Pickup Location")
            dropoff_loc = st.text_input("Dropoff Location")
            available_seats = st.number_input("Available Seats", min_value=1)
            price = st.number_input("Price", min_value=0.0, format='%f')
            special_amenities = st.text_input("Special Amenities")
            submit_button = st.form_submit_button("Add Ride")

            if submit_button:
                add_ride_response = api_post("add_rides", {
                    "user_id": user_id,
                    "departure_city": departure_city,
                    "arrival_city": arrival_city,
                    "currency": currency,
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
                    "special_amenities": special_amenities
                })
                if add_ride_response.status_code == 200:
                    st.success("Ride added successfully")
                else:
                    st.error("Failed to add ride.")

    if manage_reservations_button:
        # Implement functionality to manage reservations
        reservations_response = api_post("reservations", {"user_id": user_id})
        if reservations_response.status_code == 200:
            reservations_data = reservations_response.json()
            st.write("My Reservations:")
            st.dataframe(reservations_data)
        else:
            st.error("Failed to fetch reservations.")

    if finish_ride_button:
        # Implement functionality to finish a ride
        with st.form("finish_ride_form"):
            ride_id = st.number_input("Ride ID", min_value=1)
            submit_button = st.form_submit_button("Finish Ride")

            if submit_button:
                finish_ride_response = api_put("close_ride", {
                    "ride_id": ride_id,
                    "active": False  # Set the ride to inactive
                })
                if finish_ride_response.status_code == 200:
                    st.success("Ride finished successfully")
                else:
                    st.error("Failed to finish ride.")

    if reset_password_button:
        with st.form("reset_password_form", clear_on_submit=True):
            new_password = st.text_input("New Password", type="password")
            submit_button = st.form_submit_button("Reset Password")
            
            if submit_button:
                reset_response = api_put("forgot_password", {
                    "user_id": user_id,
                    "new_password": new_password
                })
                if reset_response.status_code == 200:
                    st.success("Password reset successfully")
                else:
                    st.error("Failed to reset password, please try again.")
    
    if logout_button:
        st.session_state['logged_in'] = False
        st.success("Logged out successfully")
