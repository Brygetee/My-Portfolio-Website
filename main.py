import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for

load_dotenv()

my_email = os.getenv("MY_EMAIL")
my_password = os.getenv("MY_PASSWORD")

app = Flask(__name__)

if not my_email or not my_password:
    app.logger.warning("MY_EMAIL or MY_PASSWORD is not set: the contact form cannot send email.")


@app.route("/")
def home():
    return redirect(url_for("portfolio"))


@app.route("/about")
def about():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form

        # spam prevention: hidden field only bots fill in, prevents spam emailing
        if data.get("website"):
            return redirect(url_for("contact", sent=1))

        name = data.get("name", "").strip()[:100]
        email = data.get("email", "").strip()[:254]
        phone = data.get("phone", "").strip()[:30]
        message = data.get("message", "").strip()[:5000]

        if not name or not message or "@" not in email:
            return render_template("contact.html", msg_sent=False, error=True), 400

        try:
            msg = EmailMessage()
            msg["Subject"] = f"Contact form submission from: {name}"
            msg["From"] = my_email
            msg["To"] = my_email
            msg["Reply-To"] = email
            msg.set_content(f"{message}\n\n{name}\n{email}\n{phone}")

            # timeout so it doesn't hang
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as connection:
                connection.starttls()
                connection.login(user=my_email, password=my_password)
                connection.send_message(msg)
            return redirect(url_for("contact", sent=1))
        except Exception:
            app.logger.exception("Email failed")
            return render_template("contact.html", msg_sent=False, error=True), 500

    return render_template("contact.html", msg_sent=request.args.get("sent") == "1")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1", port=int(os.getenv("PORT", 4009)))


