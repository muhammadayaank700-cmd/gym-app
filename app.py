from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "the gym app is being created :s"

if __name__ == "__main__":
    app.run(debug=True)
