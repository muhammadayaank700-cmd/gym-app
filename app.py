import psycopg2
import os
from dotenv import load_dotenv
from flask import session
from werkzeug.security import generate_password_hash , check_password_hash
from flask import Flask , render_template , request , redirect , url_for
from datetime import date 
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
DB_URL = os.getenv("DATABASE_URL")




def init_db():
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS workout CASCADE")   # Deletes the old singular table
    cursor.execute("DROP TABLE IF EXISTS workouts CASCADE")  # Deletes the plural table
    cursor.execute("DROP TABLE IF EXISTS users CASCADE")

   
    
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL , password_hash TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS workouts(id SERIAL PRIMARY KEY,name TEXT NOT NULL,weight TEXT NOT NULL,date TEXT NOT NULL, user_id INTEGER REFERENCES users(id))")
    conn.commit()
    conn.close()

init_db()
@app.route('/' , methods = ["GET" , "POST"])
def home():
    
    if "user_id" not in session:
        return redirect("/login")

    
    
    if request.method == "POST":
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        workout = request.form.get("workout_name")
        weight = request.form.get("weight")
        current_date = date.today().strftime("%Y-%m-%d")

        user_id = session["user_id"]

        cursor.execute("INSERT INTO workouts (name, weight,date,user_id) VALUES (%s , %s,%s,%s)",(workout,weight,current_date,user_id))
        conn.commit()
        conn.close()
        return redirect("/")

    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT id , name , weight , date FROM workouts WHERE user_id = %s",(session["user_id"],))
    rows = cursor.fetchall()
    conn.close()

    formatted_workouts = [{"id":row[0] , "name":row[1] , "weight":row[2] , "date":row[3]} for row in rows]


    return render_template("index.html", savedworkout = formatted_workouts , username = session.get("username"))

@app.route("/delete/<int:workout_id>")
def delete(workout_id):
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM workouts WHERE id = %s",(workout_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

@app.route('/update/<int:workout_id>/' , methods = ["GET" , "POST"])
def update(workout_id):
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    if request.method == "POST":
        new_name = request.form.get("workout_name")
        new_weight = request.form.get("weight")
        new_date = request.form.get("date")

        cursor.execute("UPDATE workouts SET name = %s , weight = %s , date = %s WHERE id = %s",(new_name,new_weight,new_date,workout_id))
        conn.commit()
        conn.close()

        return redirect(url_for("home"))
    
    cursor.execute("SELECT id , name , weight , date FROM workouts WHERE id = %s",(workout_id,))
    row = cursor.fetchone()
    conn.close()

    workout_to_edit = {"id":row[0] , "name" :row[1] , "weight": row[2] , "date" : row[3]}

    return render_template("edit.html", workout=workout_to_edit)


@app.route("/login", methods = ["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT id , password_hash FROM users WHERE username = %s",(username,))
        user = cursor.fetchone()
        
        #if username in database
        if user and check_password_hash(user[1],password):
            session["user_id"] = user[0]
            session["username"]= username

            conn.close()
            return redirect("/")
        else:
            error = "Invalid username or password"
        
        conn.close()

    return render_template("login.html",error=error)

     


@app.route("/register", methods = ["GET","POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s",(username,))
        existing_user = cursor.fetchone()

        #checking if user exists
        if existing_user:
            error = " oops username already taken,choose something else"
        else:
            hashed_pw = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username ,password_hash) VALUES(%s , %s)",(username,hashed_pw))
            conn.commit()
            conn.close()

            return redirect("/")

        conn.close()

        #get request
    return render_template("register.html",error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
