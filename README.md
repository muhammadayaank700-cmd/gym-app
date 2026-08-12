# 🏋️‍♂️ Gym Tracker

**[View Live Demo](https://reps-u9vs.onrender.com)**

A full-stack web application that allows users to create accounts, log in securely, and track their daily weightlifting progress. Built with Python, Flask, and a PostgreSQL database.

## 🚀 Features
* **User Authentication:** Secure registration and login system with password hashing (`werkzeug.security`).
* **Session Management:** Private routing ensuring users can only view and edit their own workout data.
* **CRUD Operations:** Users can Create, Read, Update, and Delete their workout logs.
* **Responsive UI:** Styled cleanly to work across desktop and mobile devices.
* **Cloud Database:** Integrated with Neon serverless PostgreSQL for robust data storage.

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Database:** PostgreSQL (NeonDB), `psycopg2`
* **Frontend:** HTML5, CSS3, Jinja2 Templates
* **Deployment:** Render, Gunicorn
* **Security:** Environment variables (`python-dotenv`), Password Hashing

## 💻 Local Setup & Installation

To run this project locally on your machine:


**1. Clone the repository**
```bash
git clone [https://github.com/muhammadayaank700-cmd/gym-app.git](https://github.com/muhammadayaank700-cmd/gym-app.git)
cd gym-app
```
**2. Install dependencies**
```bash
pip install -r requirements.txt
```
**3. Set up environment variables**
Create a .env file in the root directory and add your credentials:

FLASK_SECRET_KEY="your_secret_key_here"
DATABASE_URL="your_postgresql_connection_string"

**4. Run the application**
```bash
python app.py
```
The application will be available at http://127.0.0.1:5000/.







