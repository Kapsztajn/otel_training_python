DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS rooms;

CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100)
);

CREATE TABLE rooms (
    room_id VARCHAR(50) PRIMARY KEY,
    room_no VARCHAR(50) NOT NULL,
    floor INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    building VARCHAR(100) NOT NULL
);

CREATE TABLE reservations (
    reservation_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(user_id),
    room_id VARCHAR(50) REFERENCES rooms(room_id)
);