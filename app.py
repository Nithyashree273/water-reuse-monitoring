from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)

ALERT_THRESHOLD = 450

# Default starting values
current_data = {
    "total_used": 0,
    "collected": 0,
    "reused": 0
}

def calculate_data(total_used, collected, reused):
    saving_percentage = round((reused / total_used) * 100, 1) if total_used > 0 else 0
    alert = total_used > ALERT_THRESHOLD
    return {
        "total_used": total_used,
        "collected": collected,
        "reused": reused,
        "saving_percentage": saving_percentage,
        "alert": alert,
        "alert_message": f"⚠️ High water usage! {total_used}L exceeds limit of {ALERT_THRESHOLD}L." if alert else "",
        "timestamp": time.strftime("%H:%M:%S")
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/water-data")
def water_data():
    data = calculate_data(
        current_data["total_used"],
        current_data["collected"],
        current_data["reused"]
    )
    return jsonify(data)

@app.route("/api/update", methods=["POST"])
def update_data():
    body = request.get_json()
    current_data["total_used"] = int(body.get("total_used", 0))
    current_data["collected"]  = int(body.get("collected", 0))
    current_data["reused"]     = int(body.get("reused", 0))
    return jsonify({"status": "updated"})

if __name__ == "__main__":
    app.run(debug=True)