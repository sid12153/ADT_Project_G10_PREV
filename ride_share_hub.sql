-- Script for ADT RideShare hub project

-- Creating database with full name

CREATE DATABASE adt_ride_share_database;

-- Connecting to database 
\c adt_ride_share_database

-- Relation schemas and instances: authored by Manikanta Kodandapani Naidu

CREATE TABLE Users(user_id varchar(50), 
                    first_name varchar(50) NOT NULL,
                    last_name varchar(50) NOT NULL,
                    email_id varchar(50) NOT NULL,
                    contact varchar(15) NOT NULL,
                    user_password varchar(50) NOT NULL,
                    primary key (user_id));

CREATE TABLE Cities(city_id SERIAL,
                    city varchar(50) NOT NULL,
                    state varchar(5) NOT NULL,
                    country varchar(20) NOT NULL,
                    primary key (city_id));

CREATE TABLE Currencies(currency_id SERIAL,
                    currency varchar(10) NOT NULL,
                    primary key (currency_id));


CREATE TABLE Rides(ride_id SERIAL,
                    user_id varchar(50) NOT NULL,
                    departure_city_id int NOT NULL,
                    arrival_city_id int NOT NULL,
                    currency_id int NOT NULL,
                    departure_date date NOT NULL,
                    departure_time  time NOT NULL,
                    arrival_date date NOT NULL,
                    arrival_time  time NOT NULL,
                    vehicle_type varchar(50) NOT NULL,
                    vehicle_number varchar(20) NOT NULL,
                    vehicle_image bytea NULL,
                    pickup_loc varchar(100) NOT NULL,
                    dropoff_loc varchar(100) NOT NULL,
                    total_seats int NOT NULL,
                    reserved_seats int NOT NULL,
                    available_seats int NOT NULL,
                    price numeric NOT NULL,
                    special_amenities varchar(200) NULL,
                    active boolean NOT NULL,
                    primary key (ride_id),
                    foreign key (user_id) references Users(user_id) on delete cascade,
                    foreign key (departure_city_id) references Cities(city_id) on delete cascade,
                    foreign key (arrival_city_id) references Cities(city_id) on delete cascade,
                    foreign key (currency_id) references Currencies(currency_id) on delete cascade);


CREATE TABLE Bookings(booking_id SERIAL,
                        ride_id int NOT NULL,
                        passenger_id varchar(50) NOT NULL,
                        number_of_seats_reserved int NOT NULL,
                        booking_date date NOT NULL,
                        booking_time time NOT NULL,
                        billed_amount numeric NOT NULL,
                        payment_status char(50) NULL,
                        primary key (booking_id),
                        foreign key (ride_id) references Rides(ride_id) on delete cascade,
                        foreign key (passenger_id) references Users(user_id) on delete cascade);

-- DATA INSERTION : Authored by Siddharth Gosawi and Monisha Patro
-- Entries of data for Users Table
INSERT INTO Users (user_id, first_name, last_name, email_id, contact, user_password) 
VALUES 
('1', 'Manikanta', 'Kodandapani', 'k11@iu.edu', '9301234567', 'password123'),
('2', 'Siddharth', 'Gosawi', 'sgosawi@iu.edu', '9401234567', 'abc123'),
('3', 'Monisha', 'Patro', 'monpatro@iu.edu', '9303331234', 'password@1234'),
('4', 'William', 'Wordsworth', 'daffodils@gmail.com', '9988776655', 'NEWPASSWORD'),
('5', 'Swarn', 'Gaba', 'sgaba@iu.edu', '8304567845', 'password');

-- Entries of data for Cities
INSERT INTO Cities (city, state, country) 
VALUES 
('Chicago', 'IL', 'USA'),
('Indianapolis', 'IN', 'USA'),
('Bloomington', 'IN', 'USA'),
('Edinburgh', 'IN', 'USA'),
('Louisville', 'KY', 'USA');

-- Entries of data for Currencies
INSERT INTO Currencies (currency) 
VALUES 
('USD'),
('INR'),
('EUR'),
('GBP'),
('JPY'),
('CAD'),
('AUD'),
('CNY'),
('CHF'),
('RUB'),
('BRL');

-- Entries of data for Rides
INSERT INTO Rides (user_id, departure_city_id, arrival_city_id, currency_id, departure_date, departure_time, arrival_date, arrival_time, vehicle_type, vehicle_number, pickup_loc, dropoff_loc, total_seats, reserved_seats, available_seats, price, special_amenities, active) 
VALUES 
('1', 3, 2, 1, '2024-04-07', '08:00', '2024-05-07', '09:00', 'SUV', 'ABC123', 'IMU', 'City Center', 6, 1, 5, 20.00, 'Wi-Fi', true),
('2', 2, 1, 2, '2024-04-08', '10:00', '2024-05-08', '13:00', 'Economy', 'DEF456', 'Railway Station', 'Trump Tower', 4, 0, 4, 10.00, 'AC', true),
('3', 1, 3, 1, '2024-04-09', '12:00', '2024-05-09', '16:00', 'Sedan', 'GHI789', 'Navy Pier', 'Luddy', 4, 0, 4, 15.00, NULL, true),
('4', 3, 1, 3, '2024-04-10', '14:00', '2024-05-10', '18:00', 'SUV', 'JKL012', 'McNutt', 'Airport', 6, 2, 4, 20.00, 'Child seat', true),
('5', 5, 2, 2, '2024-04-11', '16:00', '2024-05-11', '20:00', 'Economy', 'MNO345', 'KFC', 'Airport', 4, 1, 3, 10.00, 'Pet-friendly', true),
('1', 3, 2, 1, '2024-04-12', '08:30', '2024-05-12', '09:30', 'SUV', 'PQR678', 'Luddy', 'Downtown', 6, 0, 6, 20.00, 'AC, Wi-Fi', true),
('2', 2, 3, 2, '2024-04-13', '11:00', '2024-05-13', '12:00', 'Economy', 'STU901', 'Railway Station', 'IMU', 4, 0, 4, 10.00, 'Pet-friendly, Music system', true),
('3', 3, 4, 1, '2024-04-14', '13:00', '2024-05-14', '17:00', 'Sedan', 'VWX234', 'College Mall', 'Burlington', 4, 0, 4, 15.00, NULL, true),
('4', 3, 2, 3, '2024-04-15', '15:30', '2024-05-15', '16:30', 'Sedan', 'YZA567', 'Wells Library', 'Mariott Hotel', 4, 2, 2, 15.00, 'Child seat, AC', true),
('5', 2, 5, 2, '2024-04-16', '17:00', '2024-05-16', '19:00', 'Sedan', 'BCD890', 'Airport', 'JW Mariott', 4, 1, 3, 15.00, 'AC', true);

-- Entries of data for Bookings
INSERT INTO Bookings (ride_id, passenger_id, number_of_seats_reserved, booking_date, booking_time, billed_amount, payment_status) 
VALUES 
(1, '2', 2, '2024-04-06', '15:30', 40.00, 'Booked'),  
(1, '3', 3, '2024-04-06', '16:00', 60.00, 'Paid'),  
(1, '4', 2, '2024-04-06', '15:30', 40.00, 'Booked'),  
(1, '5', 3, '2024-04-06', '16:00', 60.00, 'Paid'),
(2, '1', 3, '2024-04-07', '10:00', 30.00, 'Paid'),  
(2, '5', 1, '2024-04-07', '10:30', 10.00, 'Booked'),  
(7, '2', 2, '2024-04-07', '10:00', 20.00, 'Paid'),  
(7, '4', 2, '2024-04-07', '10:30', 20.00, 'Booked'),
(3, '4', 2, '2024-04-08', '12:00', 30.00, 'Paid'),  
(3, '2', 2, '2024-04-08', '12:30', 30.00, 'Paid'),  
(8, '5', 3, '2024-04-08', '12:00', 45.00, 'Booked'),  
(8, '1', 1, '2024-04-08', '12:30', 15.00, 'Paid'),
(4, '1', 2, '2024-04-08', '12:00', 40.00, 'Paid'),  
(4, '2', 2, '2024-04-08', '12:30', 40.00, 'Paid'),  
(9, '5', 1, '2024-04-08', '12:00', 15.00, 'Booked'),  
(9, '3', 1, '2024-04-08', '12:30', 15.00, 'Paid'),
(5, '2', 2, '2024-04-08', '12:00', 20.00, 'Paid'),  
(5, '1', 1, '2024-04-08', '12:30', 10.00, 'Booked'),  
(10, '4', 2, '2024-04-08', '12:00', 30.00, 'Paid'),  
(10, '3', 1, '2024-04-08', '12:30', 15.00, 'Paid');  


-- USER VIEWS: Authored by Manikanta and Siddharth

--1. Dashboard for users logged in as Rider  - done
Select rs.ride_id, c1.city as departure_city, c1.state as departure_state, c1.country as departure_country,
c2.city as arrival_city, c2.state as arrival_state, c2.country as arrival_country, rs.departure_date, rs.departure_time, rs.arrival_date,
rs.arrival_time, rs.vehicle_type, rs.vehicle_number, rs.vehicle_image, rs.pickup_loc, rs.dropoff_loc, rs.total_seats, rs.reserved_seats, rs.available_seats,
rs.price, cs.currency as price_currency, rs.special_amenities
from Rides rs join Cities c1 on rs.departure_city_id=c1.city_id
join Cities c2 on rs.arrival_city_id=c2.city_id
join Currencies cs on rs.currency_id=cs.currency_id
where user_id='1' and active=true

--2. Dashboard for users logged in as passenger - done
Select rs.ride_id, c1.city as departure_city, c1.state as departure_state, c1.country as departure_country,
c2.city as arrival_city, c2.state as arrival_state, c2.country as arrival_country, rs.departure_date, rs.departure_time, rs.arrival_date,
rs.arrival_time, rs.vehicle_type, rs.vehicle_number, rs.vehicle_image, rs.pickup_loc, rs.dropoff_loc, rs.total_seats, rs.reserved_seats, rs.available_seats,
rs.price, cs.currency as price_currency, rs.special_amenities
from Rides rs join Cities c1 on rs.departure_city_id=c1.city_id
join Cities c2 on rs.arrival_city_id=c2.city_id
join Currencies cs on rs.currency_id=cs.currency_id
where c1.city='Bloomington' and c1.state='IN' and c2.city='Indianapolis' and c2.state='IN' and active=true

--3. Dashboard for bookings made by the user
Select bks.booking_id, bks.number_of_seats_reserved, bks.booking_date, bks.booking_time, bks.billed_amount,
bks.payment_status, rs.departure_date, rs.departure_time, rs.arrival_date, rs.arrival_time, rs.pickup_loc, rs.dropoff_loc,
rs.vehicle_type, rs.vehicle_number 
from Bookings bks JOIN Rides rs on bks.ride_id=rs.ride_id
where passenger_id='1'


-- UPDATES ON RIDES AND BOOKINGS: Authored by Monisha Patro - done
--1. Update ride details - This is sample update query. Updates can be performed on other fields as well. We will be incorporating in the python script.
UPDATE Rides
SET pickup_loc = 'Luddy', total_seats=5, available_seats=4
WHERE ride_id=1;

--2.Update booking details - This is sample update query. Updates can be performed on other fields as well. We will be incorporating in the python script.
UPDATE Bookings
SET number_of_seats_reserved = 2
WHERE ride_id=5 and passenger_id='1';