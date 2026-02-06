from flask import Flask, jsonify, render_template
import serial, threading, time

app = Flask(__name__)

ser = serial.Serial("COM8", 9600, timeout=1)

latest = {
    "flame": 0,
    "gas": 0,
    "vibration": 0,
    "pressure": 1,
    "oxygen": 0,
    "depress": 0
}

def read_serial():
    global latest
    while True:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            parts = line.split(",")

            if len(parts) != 6:
                continue

            latest = {
                "flame": int(parts[0]),
                "gas": int(parts[1]),
                "vibration": int(parts[2]),
                "pressure": int(parts[3]),
                "oxygen": int(parts[4]),
                "depress": int(parts[5])
            }

        except Exception as e:
            print("Serial error:", e)
            time.sleep(0.2)

threading.Thread(target=read_serial, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify(latest)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)

