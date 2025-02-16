# Flask Authentication System

This is a simple authentication system built using Python and Flask. It provides user registration, login, Database, and session management functionalities.

## Features

- **User Registration**: Users can create an account by providing a username, email, and password.
- **User Login**: Registered users can log in using their credentials.
- **Session Management**: Users remain logged in across sessions using Flask-Login.
- **Password Hashing**: Passwords are securely hashed using `werkzeug.security` before being stored in the database.

## Requirements

- Python 3.7+
- Flask
- Flask-Login
- pymongo
- werkzeug.security

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PVishwakarma/AuthenticationProject.git