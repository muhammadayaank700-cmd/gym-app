from flask import Flask , render_template , request

app = Flask(__name__)

@app.route('/' , methods = ["GET" , "POST"])
def home():
    if request.method == "POST":
        workout = request.form.get("workout_name")
        weight = request.form.get("weight")

        print(f"databse simulation: saving {workout} and the weight {weight}")


    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
