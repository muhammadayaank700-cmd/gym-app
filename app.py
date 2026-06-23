import sqlite3
from flask import Flask , render_template , request , redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS workouts(id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT NOT NULL , weight TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()
@app.route('/' , methods = ["GET" , "POST"])
def home():
    

    
    
    if request.method == "POST":
        conn = sqlite3.connect("gym.db")
        cursor = conn.cursor()
        workout = request.form.get("workout_name")
        weight = request.form.get("weight")

        cursor.execute("INSERT INTO workouts (name, weight) VALUES (? , ?)",(workout,weight))
        conn.commit()
        conn.close()
        return redirect("/")

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name , weight FROM workouts")
    rows = cursor.fetchall()
    conn.close()

    formatted_workouts = [{"name":row[0] , "weight":row[1]} for row in rows]


    return render_template("index.html", savedworkout = formatted_workouts)
    
if __name__ == "__main__":
    app.run(debug=True)
