
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

if __name__ == '__main__':
    app.run(debug=True, port=4009)


# emojis: https://emojicombos.com/heart
# TODO 1: Make tabs :before, :after the content element
