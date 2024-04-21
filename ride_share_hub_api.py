from typing import Union, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import psycopg2
from psycopg2 import OperationalError
from datetime import datetime

app = FastAPI()

def postgres_connection():
    try:
        # Connecting to database
        conn = psycopg2.connect(database = "adt_ride_share_database", 
                user = "postgres", 
                host= '127.0.0.1',
                password = "root",
                port = 5432)
        print("PostgreSQL connection established")
    except OperationalError:
        raise Exception("Error connecting to PostgreSQL database")
        
    return conn

def get_city_id(city_detail, cur):
    city_list = city_detail.split(',')
    city, state, country = city_list[0].strip(), city_list[1].strip(), city_list[2].strip()

    cur.execute("Select city_id from cities where city=%s and state=%s and country=%s", (city, state, country))
    rows = cur.fetchone()

    city_id_res = rows[0]

    return city_id_res

def get_currency_id(currency_detail, cur):
    cur.execute("Select currency_id from currencies where currency=%s;", (currency_detail,))
    rows = cur.fetchone()

    currency_id_res = rows[0]

    return currency_id_res


# Json Request Body
class Login_Request_Body(BaseModel):
    user_id: str
    user_password: str


class Signup_Request_Body(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email_id: EmailStr
    contact: str
    user_password: str

class Reset_Password_Request_Body(BaseModel):
    user_id: str
    new_password: str

class Fetch_Rides_Request_Body(BaseModel):
    user_id: str


class Add_Ride_Request_Body(BaseModel):
    user_id: str
    departure_city: str
    arrival_city: str
    currency: str
    departure_date: str
    departure_time: str
    arrival_date: str
    arrival_time: str
    vehicle_type: str
    vehicle_number: str
    vehicle_image: Optional[str] = None
    pickup_loc: str
    dropoff_loc:str
    available_seats: int
    price: float
    special_amenities: str

class Update_Ride_Request_Body(BaseModel):
    ride_id: int
    departure_city: Optional[str] = None
    arrival_city: Optional[str] = None
    currency: Optional[str] = None
    departure_date: Optional[str] = None
    departure_time: Optional[str] = None
    arrival_date: Optional[str] = None
    arrival_time: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_number: Optional[str] = None
    vehicle_image: Optional[str] = None
    pickup_loc: Optional[str] = None
    dropoff_loc: Optional[str] = None
    available_seats: Optional[int] = None
    price: Optional[float] = None
    special_amenities: Optional[str] = None

class Fetch_Passenger_Rides_Request_Body(BaseModel):
    departure_city: Optional[str] = None
    arrival_city: Optional[str] = None
    departure_date: Optional[str] = None
    arrival_date: Optional[str] = None
    available_seats: Optional[int] = None

class Reserve_Ride_Request_Body(BaseModel):
    ride_id: int
    passenger_id: str
    number_of_seats_reserved: int
    price: float

class Fetch_Reservation_Request_Body(BaseModel):
    user_id: str

class Update_Reservation_Request_Body(BaseModel):
    booking_id: int
    payment_status: str

class Finish_Ride_Request_Body(BaseModel):
    ride_id: int
    active: bool

@app.post("/login_check", status_code=200)
async def login_user(login_details: Login_Request_Body):

    conn = postgres_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Executing the SQL query
    cur.execute("Select * from users where user_id=%s and user_password=%s;", (login_details.user_id, login_details.user_password))
    rows = cur.fetchall()
    conn.commit()
    conn.close()

    if rows:
        response = {"status":"Success",
                    "message":"User exists"}
        return response # procceed to the next page
    else:
        raise HTTPException(status_code=404, detail="Login failed due to incorrect user ID or password")
    

@app.post("/register_user", status_code=200)
async def register_user(signup_details: Signup_Request_Body):

    conn = postgres_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # check if user already exists
    cur.execute("Select * from users where user_id=%s;", (signup_details.user_id,))
    rows = cur.fetchall()
    if rows:
        raise HTTPException(status_code=409, detail="User already exists")
    

    # Executing the SQL insert query for the user
    insert_query = """INSERT INTO users(user_id,first_name,last_name,email_id,contact,user_password) VALUES(%s,%s,%s,%s,%s,%s) RETURNING user_id;"""
    cur.execute(insert_query, (signup_details.user_id, signup_details.first_name, signup_details.last_name,
                                signup_details.email_id, signup_details.contact, signup_details.user_password))
    
    rows = cur.fetchone()
    conn.commit()
    conn.close()

    if rows:
        returned_user_id = rows[0]
        print("Registration is successfull for user:{}".format(returned_user_id))
        response = {"status":"Success",
                    "message":"User registered successfully"}
        return response # procceed to the next page
    else:
        raise HTTPException(status_code=404, detail="User registration failed. Please try again!")
    
@app.put("/forgot_password", status_code=200)
async def reset_password(password_details: Reset_Password_Request_Body):

    conn = postgres_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    print("reseting the password")
    # reset password for user
    update_query = """UPDATE users SET user_password=%s WHERE user_id=%s RETURNING user_id;"""

    # Executing the SQL update query for the user
    cur.execute(update_query, (password_details.new_password, password_details.user_id))
    rows = cur.fetchone()
    conn.commit()
    conn.close()

    if rows:
        returned_user_id = rows[0]
        print("Password reset is successfull for user:{}".format(returned_user_id))
        response = {"status":"Success",
                    "message":"Password reset is successfull"}
        return response # procceed to the next page
    else:
        raise HTTPException(status_code=404, detail="Failed to reset the password. Please try again!")
    

@app.post("/fetch_rides", status_code=200)
async def rides(rider_details: Fetch_Rides_Request_Body):
    conn = postgres_connection()
    cur = conn.cursor()
    rider_query = """
    SELECT ride_id, c1.city as departure_city, c1.state as departure_state, c1.country as departure_country,
    c2.city as arrival_city, c2.state as arrival_state, c2.country as arrival_country, departure_date, departure_time, 
    arrival_date, arrival_time, vehicle_type, vehicle_number, pickup_loc, dropoff_loc, 
    total_seats, reserved_seats, available_seats, price, cs.currency, special_amenities
    FROM Rides rs 
    JOIN Cities c1 ON rs.departure_city_id=c1.city_id
    JOIN Cities c2 ON rs.arrival_city_id=c2.city_id
    JOIN Currencies cs ON rs.currency_id=cs.currency_id
    WHERE user_id=%s AND active=true
    """
    cur.execute(rider_query, (rider_details.user_id,))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    
    # Define custom column names here
    column_names = [
        "Ride ID", "Departure City", "Departure State", "Departure Country",
        "Arrival City", "Arrival State", "Arrival Country", "Departure Date", 
        "Departure Time", "Arrival Date", "Arrival Time", "Vehicle Type", 
        "Vehicle Number", "Pickup Location", "Dropoff Location", 
        "Total Seats", "Reserved Seats", "Available Seats", "Price", 
        "Currency", "Special Amenities"
    ]
    
    # Convert the rows to dictionaries with custom column names
    rides_data = [dict(zip(column_names, row)) for row in rows]
    return rides_data

    # if rows:
    #     for row in rows:
    #         print(row)
    #     response = {"status":"Success",
    #                 "message":"Rides fetched"}
    #     return response # procceed to the next page
    # else:
    #     raise HTTPException(status_code=500, detail="Failed to fetch the rides for the user:{}".format(rider_details.user_id))


@app.post("/add_rides", status_code=200)
async def add_ride(rider_details: Add_Ride_Request_Body):

    conn = postgres_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Executing the SQL query

    # retrieving departure and arrival city ids
    departure_city_id = get_city_id(rider_details.departure_city)
    arrival_city_id = get_city_id(rider_details.arrival_city)

    # retrieving the currency id
    currency_id = get_currency_id(rider_details.currency)


    # Executing the SQL insert query for the user
    insert_query = """INSERT INTO rides(user_id, departure_city_id, arrival_city_id, currency_id, departure_date, departure_time, 
    arrival_date, arrival_time, vehicle_type, vehicle_number, vehicle_image, pickup_loc, dropoff_loc, total_seats, reserved_seats, 
    available_seats, price, special_amenities, active) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING ride_id;"""
    cur.execute(insert_query, (rider_details.user_id, departure_city_id, arrival_city_id, currency_id, rider_details.departure_date, 
                               rider_details.departure_time, rider_details.arrival_date, rider_details.arrival_time, rider_details.vehicle_type, rider_details.vehicle_number,
                               rider_details.vehicle_image, rider_details.pickup_loc, rider_details.dropoff_loc, rider_details.available_seats, 0,
                               rider_details.available_seats, rider_details.price, rider_details.special_amenities, True))

    rows = cur.fetchone()
    conn.commit()
    conn.close()

    if rows:
        returned_ride_id = rows[0]
        print("Ride added successfull for user:{} with ride ID:{}".format(rider_details.user_id, returned_ride_id))
        response = {"status":"Success",
                    "message":"Ride added successfully"}
        return response # procceed to the next page
    else:
        raise HTTPException(status_code=404, detail="Failed to add ride. Please try again!")



@app.put("/update_rides", status_code=200)
async def update_ride(ride_update_details: Update_Ride_Request_Body):
    conn = postgres_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    update_set = ""
    value_set = []

    ride_update_details_dict = ride_update_details.dict()
    print(ride_update_details_dict)

    for key,value in ride_update_details_dict.items():
        if value is not None and key != 'ride_id':
            if key == "departure_city":
                departure_city_id = get_city_id(value, cur)
                update_set = update_set + "departure_city_id=%s,"
                value_set.append(departure_city_id)

            elif key == "arrival_city":
                arrival_city_id = get_city_id(value, cur)
                update_set = update_set + "arrival_city_id=%s,"
                value_set.append(arrival_city_id)

            elif key == "currency":
                currency_id = get_currency_id(value, cur)
                update_set = update_set + "currency_id=%s,"
                value_set.append(currency_id)
            
            else:
                update_set = update_set + "{}=%s,".format(key)
                value_set.append(value)

    update_query = "UPDATE rides SET " + update_set.rstrip(',') +  " WHERE ride_id=%s RETURNING ride_id;"

    value_set.append(ride_update_details.ride_id)
    final_values = tuple(value_set)

    print(value_set)
    print(final_values)
    # Executing the SQL update query for the user
    cur.execute(update_query, final_values)
    rows = cur.fetchone()
    conn.commit()
    conn.close()

    if rows:
        returned_ride_id = rows[0]
        print("Ride updated successfull for ride ID:{}".format(returned_ride_id))
        response = {"status":"Success",
                    "message":"Ride update is successfull"}
        return response # procceed to the next page
    else:
        raise HTTPException(status_code=404, detail="Failed to update ride details. Please try again!")

# APIs for PASSENGER PAGE
@app.post("/fetch_passenger_rides", status_code=200)
async def passenger_rides(passenger_details: Fetch_Passenger_Rides_Request_Body):

    conn = postgres_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Executing the SQL query
    passenger_query = """Select rs.ride_id, c1.city as departure_city, c1.state as departure_state, c1.country as departure_country,
    c2.city as arrival_city, c2.state as arrival_state, c2.country as arrival_country, rs.departure_date, rs.departure_time, rs.arrival_date,
    rs.arrival_time, rs.vehicle_type, rs.vehicle_number, rs.vehicle_image, rs.pickup_loc, rs.dropoff_loc, rs.total_seats, rs.reserved_seats, rs.available_seats,
    rs.price, cs.currency as price_currency, rs.special_amenities
    from Rides rs join Cities c1 on rs.departure_city_id=c1.city_id
    join Cities c2 on rs.arrival_city_id=c2.city_id
    join Currencies cs on rs.currency_id=cs.currency_id"""

    condition_set = " where "
    value_set = []

    passenger_details_dict = passenger_details.dict()

    for key,value in passenger_details_dict.items():
        if value is not None:
            if key == "departure_city":
                departure_city_id = get_city_id(value, cur)
                condition_set = condition_set + "c1.city_id=%s and "
                value_set.append(departure_city_id)

            elif key == "arrival_city":
                arrival_city_id = get_city_id(value, cur)
                condition_set = condition_set + "c2.city_id=%s and "
                value_set.append(arrival_city_id)

            elif key == "available_seats":
                condition_set = condition_set + "rs.{}>=%s and ".format(key)
                value_set.append(value)

            else:
                condition_set = condition_set + "rs.{}=%s and ".format(key)
                value_set.append(value)


    passenger_search_query = passenger_query + condition_set +  "active=true;"
    final_values = tuple(value_set)

    # Executing the SQL update query for the user
    cur.execute(passenger_search_query, final_values)
    rows = cur.fetchall()
    conn.commit()
    conn.close()

    return rows

@app.post("/reserve_rides", status_code=200)
async def reserve_ride(reservation_details: Reserve_Ride_Request_Body):

    conn = postgres_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    total_billed_amount = reservation_details.number_of_seats_reserved * reservation_details.price
    # Executing the SQL insert query for reserving ride
    insert_query = """INSERT INTO Bookings(ride_id, passenger_id, number_of_seats_reserved, booking_date, booking_time, billed_amount,  payment_status) 
    VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING booking_id;"""
    cur.execute(insert_query, (reservation_details.ride_id, reservation_details.passenger_id, reservation_details.number_of_seats_reserved, 
                               datetime.date(datetime.now()), datetime.time(datetime.now()), total_billed_amount, 'Booked'))

    rows = cur.fetchone()

    if rows:
        returned_booking_id = rows[0]
        print("Ride reserved successfull with booking ID:{}".format(returned_booking_id))
        # Update the available seats for the ride accordingly
        # first fetch the ride details
        search_query = """Select total_seats, reserved_seats, available_seats from rides where ride_id=%s"""

        cur.execute(search_query, (reservation_details.ride_id,))
        ride_rows = cur.fetchone()

        total_seats = ride_rows[0]
        reserved_seats = ride_rows[1]
        available_seats = ride_rows[2]

        updated_reserved_seats = reserved_seats + reservation_details.number_of_seats_reserved
        updated_available_seats = available_seats - reservation_details.number_of_seats_reserved

        if (total_seats != (reserved_seats + available_seats)) or (total_seats != (updated_reserved_seats + updated_available_seats)):
            print("Error in updating ride seats count. Therefore deleting the booking.")
            delete_booking_query = """Delete from bookings where booking_id=%s"""
            cur.execute(delete_booking_query, (returned_booking_id,))
            conn.commit()
            conn.close()
            raise HTTPException(status_code=404, detail="Failed to reserve the ride due to seats count mismatch. Please try again!")
        else:
            ride_update_query = """Update rides SET total_seats=%s, reserved_seats=%s, available_seats=%s where ride_id=%s RETURNING ride_id;"""
            cur.execute(ride_update_query, (total_seats, updated_reserved_seats, updated_available_seats, reservation_details.ride_id))
            ride_row = cur.fetchone()
            if ride_row:
                conn.commit()
                conn.close()
                print("Seat counts updated successfully for the ride with ID:{}".format(ride_row[0]))
                response = {"status":"Success",
                            "message":"Ride reservation is successfull"}
                return response # procceed to the next page
            
            else:
                print("Failed to update the seats count for ride ID {} as per the booking ID:{}. Therefore, deleting the respective booking.".format(reservation_details.ride_id,returned_booking_id))
                delete_booking_query = """Delete from bookings where booking_id=%s"""
                cur.execute(delete_booking_query, (returned_booking_id,))
                conn.commit()
                conn.close()
                raise HTTPException(status_code=404, detail="Failed to reserve the ride due to seats count mismatch. Please try again!")
    else:
        raise HTTPException(status_code=404, detail="Failed to reserve the ride. Please try again!")


@app.put("/update_reservations", status_code=200)
async def update_reservation(reservation_details: Update_Reservation_Request_Body):
    conn = postgres_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # update reservation
    update_query = """UPDATE bookings SET payment_status=%s WHERE booking_id=%s RETURNING booking_id;"""

    # Executing the SQL update query for the user
    cur.execute(update_query, (reservation_details.payment_status, reservation_details.booking_id))
    rows = cur.fetchone()
    conn.commit()
    conn.close()

    if rows:
        returned_booking_id = rows[0]
        print("Booking updated successfully for ID:{}".format(returned_booking_id))
        response = {"status":"Success",
                    "message":"Booking update is successfull"}
        return response # procceed to the next page
    else:
        raise HTTPException(status_code=404, detail="Failed to update the booking. Please try again!")
    
@app.get("/get_cities", status_code=200)
async def get_cities():
    conn = postgres_connection()
    cur = conn.cursor()
    cur.execute("SELECT city FROM Cities;")
    cities = cur.fetchall()
    conn.close()
    # Unpack the city names from the query result
    city_names = [city[0] for city in cities]
    return city_names

@app.get("/get_currencies", status_code=200)
async def get_currencies():
    conn = postgres_connection()
    cur = conn.cursor()
    cur.execute("SELECT currency FROM Currencies;")
    currencies = cur.fetchall()
    conn.close()
    # Unpack the currency names from the query result
    currency_names = [currency[0] for currency in currencies]
    return currency_names

@app.post("/reservations", status_code=200)
async def passenger_reservations(user_details: Fetch_Reservation_Request_Body):
    conn = postgres_connection()
    cur = conn.cursor()
    bookings_search_query = """
    SELECT bks.booking_id, bks.number_of_seats_reserved, 
    bks.booking_date, bks.booking_time, bks.billed_amount, bks.payment_status, 
    rs.departure_date, rs.departure_time, rs.arrival_date, rs.arrival_time, 
    rs.pickup_loc, rs.dropoff_loc, rs.vehicle_type, rs.vehicle_number 
    FROM Bookings bks 
    JOIN Rides rs ON bks.ride_id = rs.ride_id
    WHERE passenger_id = %s
    """
    cur.execute(bookings_search_query, (user_details.user_id,))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    
    # Define custom column names here
    column_names = [
        "Booking ID", "Seats Reserved", "Booking Date", "Booking Time",
        "Billed Amount", "Payment Status", "Departure Date", "Departure Time",
        "Arrival Date", "Arrival Time", "Pickup Location", "Dropoff Location",
        "Vehicle Type", "Vehicle Number"
    ]
    
    # Convert the rows to dictionaries with custom column names
    reservations_data = [dict(zip(column_names, row)) for row in rows]
    return reservations_data


@app.put("/close_ride", status_code=200)
async def Finish_ride(ride_details: Finish_Ride_Request_Body):
    conn = postgres_connection()
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # update reservation
    update_query = """UPDATE rides SET active=%s WHERE ride_id=%s RETURNING ride_id;"""

    # Executing the SQL update query for the user
    cur.execute(update_query, (ride_details.active, ride_details.ride_id))
    rows = cur.fetchone()
    conn.commit()
    conn.close()

    if rows:
        returned_ride_id = rows[0]
        print("Ride closed for ID:{}".format(returned_ride_id))
        response = {"status":"Success",
                    "message":"Successfully closed ride"}
        return response # procceed to the next page
    else:
        raise HTTPException(status_code=404, detail="Failed to close the ride. Please try again!")
    
# conn = postgres_connection()
# # Open a cursor to perform database operations
# cur = conn.cursor()
# departure_city_id = get_city_id('Bloomington, IN, USA', cur)
# print(departure_city_id)

# conn = postgres_connection()
# # Open a cursor to perform database operations
# cur = conn.cursor()
# # Executing the SQL query
# rider_query = """Select * from rides where ride_id=1"""


# cur.execute(rider_query, ('1',))
# rows = cur.fetchall()
# conn.commit()
# conn.close()

# for row in rows:
#     print(row[14])
#     print(row[15])
#     print(row[16])
#     print("+++++++++++++++++++++")