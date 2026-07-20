import psycopg2
from flask import Flask , render_template , request , redirect , url_for
from datetime import date 
app = Flask(__name__)

def init_db():
    conn = psycopg2.connect("postgresql://neondb_owner:npg_rFMEqJk3gae9@ep-crimson-voice-zai9b3hf.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require")
    cursor = conn.cursor()

   
    
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL , password_hash TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS workout(id SERIAL PRIMARY KEY,name TEXT NOT NULL,weight TEXT NOT NULL,date TEXT NOT NULL, user_id INTEGER REFERENCES users(id))")
    conn.commit()
    conn.close()

init_db()
@app.route('/' , methods = ["GET" , "POST"])
def home():
    

    
    
    if request.method == "POST":
        conn = psycopg2.connect("postgresql://neondb_owner:npg_rFMEqJk3gae9@ep-crimson-voice-zai9b3hf.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require")
        cursor = conn.cursor()
        workout = request.form.get("workout_name")
        weight = request.form.get("weight")
        current_date = date.today().strftime("%Y-%m-%d")

        cursor.execute("INSERT INTO workouts (name, weight,date) VALUES (%s , %s,%s)",(workout,weight,current_date))
        conn.commit()
        conn.close()
        return redirect("/")

    conn = psycopg2.connect("postgresql://neondb_owner:npg_rFMEqJk3gae9@ep-crimson-voice-zai9b3hf.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require")
    cursor = conn.cursor()
    cursor.execute("SELECT id , name , weight , date FROM workouts")
    rows = cursor.fetchall()
    conn.close()

    formatted_workouts = [{"id":row[0] , "name":row[1] , "weight":row[2] , "date":row[3]} for row in rows]


    return render_template("index.html", savedworkout = formatted_workouts)

@app.route("/delete/<int:workout_id>")
def delete(workout_id):
    conn = psycopg2.connect("postgresql://neondb_owner:npg_rFMEqJk3gae9@ep-crimson-voice-zai9b3hf.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM workouts WHERE id = %s",(workout_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

@app.route('/update/<int:workout_id>/' , methods = ["GET" , "POST"])
def update(workout_id):
    conn = psycopg2.connect("postgresql://neondb_owner:npg_rFMEqJk3gae9@ep-crimson-voice-zai9b3hf.c-2.eu-west-2.aws.neon.tech/neondb?sslmode=require")
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


if __name__ == "__main__":
    app.run(debug=True)
