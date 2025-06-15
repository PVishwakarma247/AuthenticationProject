# 🔐 Flask Authentication System (MySQL)

A secure user authentication system built using **Flask** and **MySQL**. It supports user registration, login, session handling, and password hashing. Email functionality is included using **Flask-Mail**, and sensitive configuration is managed through environment variables.

---

## ✅ Features

- 📝 **User Registration** – Create accounts with name, email, and password.
- 🔐 **User Login** – Login with secure credential validation.
- 🔄 **Session Management** – Persistent user sessions with Flask.
- 🛡️ **Password Hashing** – Secure password storage using `werkzeug.security`.
- 📧 **Email Notifications** – Send email using `Flask-Mail`.
- ⚙️ **MySQL Database Integration** – Store and retrieve user data.
- 🔑 **Environment Variable Support** – Use `.env` to manage secrets securely.

---

## 📦 Requirements

- Python 3.7+
- Flask
- mysql-connector-python
- Flask-Mail
- Werkzeug
- python-dotenv

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PVishwakarma/AuthenticationProject.git

2. install dependencies:
   ```bash
   pip install -r requirement.txt

3. configure .env file:
   ```bash
   EMAIL=email@gnail.com
   EMAIL_PASS=password
   KEY=secret_key