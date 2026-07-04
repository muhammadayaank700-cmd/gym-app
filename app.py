import sqlite3
from flask import Flask , render_template , request , redirect , url_for

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
    cursor.execute("SELECT id , name , weight FROM workouts")
    rows = cursor.fetchall()
    conn.close()

    formatted_workouts = [{"id":row[0] , "name":row[1] , "weight":row[2]} for row in rows]


    return render_template("index.html", savedworkout = formatted_workouts)

@app.route("/delete/<int:workout_id>")
def delete(workout_id):
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM workouts WHERE id = ?",(workout_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

@app.route('/update/<int:workout_id>/' , methods = ["GET" , "POST"])
def update(workout_id):
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    if request.method == "POST":
        new_name = request.form.get("workout_name")
        new_weight = request.form.get("weight")

        cursor.execute("UPDATE workouts SET name = ? , weight = ? WHERE id =?",(new_name,new_weight,workout_id))
        conn.commit()
        conn.close()

        return redirect(url_for("home"))
    
    cursor.execute("SELECT id , name , weight FROM workouts WHERE id = ?",(workout_id,))
    row = cursor.fetchone()
    conn.close()

    workout_to_edit = {"id":row[0] , "name" :row[1] , "weight": row[2]}

    return render_template("edit.html", workout=workout_to_edit)


if __name__ == "__main__":
    app.run(debug=True)
