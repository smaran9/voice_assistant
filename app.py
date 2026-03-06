from flask import Flask, render_template, jsonify
# switch to new modular packages instead of legacy assistant/
from voice import listen, speak
from commands import process_command

app = Flask(__name__)


# -------------------------------
# UI HOME PAGE
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# LISTEN ROUTE (Orb Click)
# -------------------------------
active = False   # global state

@app.route("/listen")
def listen_route():

    global active

    try:
        command = listen()
        print("You said:", command)

        # Wake word detect
        if "mitra" in command and not active:
            active = True
            reply = "Hi, I am Mitra. How can I help you?"
            speak(reply)
            return jsonify({"response": reply})

        # If assistant not active
        if not active:
            return jsonify({"response": "Say Mitra to wake me up"})

        # Sleep command
        if "sleep" in command:
            active = False
            reply = "Going to sleep"
            speak(reply)
            return jsonify({"response": reply})
        if "stop" in command or "exit" in command or "goodbye" in command or "bye" in command:
            active = False
            reply = "goodbye"
            speak(reply)
            return jsonify({"response": reply})

        # Normal processing
        # New process_command returns our structured dict
        result = process_command(command)

        if isinstance(result, dict):
            message = result.get("response") or result.get("message") or "Done"
        else:
            message = str(result)

        speak(message)
        return jsonify({"response": message})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"response": "Assistant error"})


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
