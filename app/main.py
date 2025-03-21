from flask import Flask, render_template, request

app = Flask(__name__)  # Removed extra indentation

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")

    if not (name and email):
        return "Name and email are required!", 400

    return render_template('success.html', name=name)

# Fixed the typo in __name__ and __main__
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
