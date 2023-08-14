from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "secret_key"  # Change this to a strong secret key

# Function to start a new game
def start_new_game():
    session["target_number"] = random.randint(1, 100)
    session["attempts"] = 0

# Function to provide a hint based on the difference between the guess and the target
def get_hint(guess, target):
    difference = abs(guess - target)
    if difference > 20:
        return "Very cold"
    elif difference > 10:
        return "Cold"
    elif difference > 5:
        return "Warm"
    elif difference > 1:
        return "Hot"
    else:
        return "Very hot (You're very close!)"

# Route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        guess = int(request.form["guess"])
        target = session["target_number"]

        session["attempts"] += 1
        hint = get_hint(guess, target)

        if guess == target:
            return render_template("guess.html", message="Congratulations! You guessed the number.", success=True)
        elif guess < target:
            return render_template("guess.html", message=f"Try again! The number is higher. ({hint})", success=False, hint=hint)
        else:
            return render_template("guess.html", message=f"Try again! The number is lower. ({hint})", success=False, hint=hint)
    else:
        start_new_game()
        return render_template("guess.html", message="Guess a number between 1 and 100.", success=None)

if __name__ == "__main__":
    app.run(debug=True)
