import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

my_email = os.getenv("MY_EMAIL")
my_password = os.getenv("MY_PASSWORD")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("index.html")

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        data = request.form

        msg = EmailMessage()
        msg["Subject"] = f"Contact form submission from: {data['name']}"
        msg["From"] = my_email
        msg["To"] = my_email
        msg["Reply-To"] = data["email"]
        msg.set_content(
            f"{data['message']}\n\n{data['name']}\n{data['email']}\n{data.get('phone', '')}"
        )

        try:
            with smtplib.SMTP("smtp.gmail.com",587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=my_password)
                connection.send_message(msg)
            return render_template("contact.html", msg_sent=True)
        except Exception as e:
            app.logger.error(f"Email failed {e}")
            return render_template("contact.html", msg_sent=False, error=True)
    return render_template("contact.html", msg_sent=False)

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

if __name__ == '__main__':
    app.run(debug=True, port=4009)


# emojis: https://emojicombos.com/heart

# TODO 1: ABOUT PAGE: 1. change background, add favicon, change the dark pink color, change order of links
#Todo 2: correct contact page
#Todo 4: textpink &dark pink are the same variable


