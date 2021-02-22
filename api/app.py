from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return 'Hello world flask'

@app.route("/api")
def hello_api():
    return 'API topzera com pythone e docker'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")