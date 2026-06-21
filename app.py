from flask import Flask , render_template , request

app = Flask(__name__)

workouts = [] #creating temporary database using list

@app.route('/' , methods = ["GET" , "POST"])
def home():
    if request.method == "POST":
        workout = request.form.get("workout_name")
        weight = request.form.get("weight")
        
        workouts.append({"name":workout , "weight": weight})

    return render_template("index.html", savedworkout = workouts)

if __name__ == "__main__":
    app.run(debug=True)
