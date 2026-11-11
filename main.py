
import os
import resend
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for

load_dotenv()

my_email = os.getenv("MY_EMAIL")
resend.api_key = os.getenv("RESEND_API_KEY")

app = Flask(__name__)

if not my_email or not resend.api_key:
    app.logger.warning("MY_EMAIL or RESEND_API_KEY is not set: the contact form cannot send email.")


@app.route("/")
def home():
    return render_template("portfolio.html")


@app.route("/about")
def about():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form

        # Spam prevention: hidden field only bots fill in
        if data.get("website"):
            return redirect(url_for("contact", sent=1))

        name = data.get("name", "").strip()[:100]
        email = data.get("email", "").strip()[:254]
        phone = data.get("phone", "").strip()[:30]
        message = data.get("message", "").strip()[:5000]

        if not name or not message or "@" not in email:
            return render_template("contact.html", msg_sent=False, error=True), 400

        try:
            resend.Emails.send({
                "from": "Brygetee Portfolio <contact@mail.brygetee.com>",
                "to": [my_email],
                "reply_to": email,
                "subject": f"Contact form submission from: {name}",
                "text": f"{message}\n\n{name}\n{email}\n{phone}"
            })

            return redirect(url_for("contact", sent=1))

        except Exception:
            app.logger.exception("Email failed")
            return render_template("contact.html", msg_sent=False, error=True), 500

    return render_template("contact.html", msg_sent=request.args.get("sent") == "1")


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1", port=int(os.getenv("PORT", 4009)))
