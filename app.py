from flask import Flask, render_template, request, jsonify
import threading
import time
import random

app = Flask(__name__)

data = {
    "fresh_water": 1000,
    "waste_water": 400,
    "recovered_water": 300,
    "reused_water": 250
}

def auto_update():
    while True:
        data["fresh_water"] += random.randint(1, 10)
        data["waste_water"] += random.randint(1, 5)
        data["recovered_water"] += random.randint(1, 4)

        # Reused water is 80% of recovered water
        data["reused_water"] = int(data["recovered_water"] * 0.8)

        time.sleep(10)

threading.Thread(target=auto_update, daemon=True).start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    efficiency = round(
        (data["recovered_water"] / data["waste_water"]) * 100, 2
    ) if data["waste_water"] > 0 else 0

    return jsonify({
        **data,
        "efficiency": efficiency
    })

@app.route('/update', methods=['POST'])
def update():
    data["fresh_water"] = int(request.form['fresh_water'])
    data["waste_water"] = int(request.form['waste_water'])
    data["recovered_water"] = int(request.form['recovered_water'])
    data["reused_water"] = int(request.form['reused_water'])

    return "Data Updated Successfully"

if __name__ == '__main__':
    app.run(debug=True)