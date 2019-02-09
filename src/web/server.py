from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello! I'm draw_to_code application =)"